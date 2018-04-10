import mysql.connector
import psycopg2
import pymysql
from nps_zip_module import zip_dir

from datetime import datetime, timedelta

"""
Define an interface for creating an object, but let subclasses decide
which class to instantiate. Factory Method lets a class defer
instantiation to subclasses.
"""

import abc


class Creator(metaclass=abc.ABCMeta):
    """
    Declare the factory method, which returns an object of type Product.
    Creator may also define a default implementation of the factory
    method that returns a default ConcreteProduct object.
    Call the factory method to create a Product object.
    """

    def __init__(self):
        self.product = self._factory_method()

    @abc.abstractmethod
    def _factory_method(self):
        pass

    """
    Non mi sembra utile
    def some_operation(self):
        self.product.interface()
    """


class ConcreteCreatorMySQL(Creator):
    """
    Override the factory method to return an instance of a
    ConcreteProduct1.
    """

    def _factory_method(self):
        return ConcreteDatabaseMySQL()


class ConcreteCreatorPostSQL(Creator):
    """
    Override the factory method to return an instance of a
    ConcreteProduct2.
    """

    def _factory_method(self):
        return ConcreteDatabasePostSQL()


class Database(metaclass=abc.ABCMeta):
    """
    Define the interface of objects the factory method creates.
    """

    @abc.abstractmethod
    def connection(self,
                   host,  # your host
                   user,  # username
                   passwd,  # password
                   db):
        pass

    @abc.abstractmethod
    def get_columns(self):
        pass

    @abc.abstractmethod
    def select(self, statement):
        pass

    @abc.abstractmethod
    def delete(self, statement):
        pass

    @abc.abstractmethod
    def update(self, statement):
        pass


class ConcreteDatabaseMySQL(Database):
    """
    Implement the Product interface.
    """

    def __init__(self):
        self.db_con = None
        self.cur = None

    def connection(self,
                   host="db801rco.intranet.fw",  # your host
                   user="rogarofalo",  # username
                   passwd="R0garof4lo",  # password
                   db="nps"):
        self.db_con = pymysql.connect(host,  # your host
                                      user,  # username
                                      passwd,  # password
                                      db)  # name of the database
        mysql.connector.connect()
        self.cur = self.db_con.cursor()

    def select(self, statement):
        self.cur.execute(statement)
        return self.cur.fetchall()

    def get_columns(self):
        return self.cur.description

    def delete(self, statement):
        pass

    def update(self, statement):
        pass


class ConcreteDatabasePostSQL(Database):
    """
    Implement the Product interface.
    """
    def __init__(self):
        self.db_con = None
        self.cur = None

    def connection(self,
                   host="db801rco.intranet.fw",  # your host
                   user="rogarofalo",  # username
                   passwd="R0garof4lo",  # password
                   db="nps"):
        self.db_con = psycopg2.connect(host,  # your host
                                       user=user,  # username
                                       password=passwd,  # password
                                       database=db)  # name of the database

    def select(self, statement):
        self.cur = self.db_con.cursor()
        self.cur.execute(statement)
        return self.cur.fetchall()

    def get_columns(self):
        return self.cur.description

    def delete(self, statement):
        pass

    def update(self, statement):
        pass


class Report(metaclass=abc.ABCMeta):
    """
    Define the interface of objects the factory method creates.
    """

    @abc.abstractmethod
    def produce_reports_csv(self, dao):
        pass


class ConcreteBaseReportNPS(Report):
    """
    Implement the Report interface.
    """

    def __init__(self, directory_log, interval_days=0):
        self.directory = directory_log
        self.report_conf = dict()
        self.file_name_start = 'F_report_assistenza_tecnica_'
        self.days_to_subtract = interval_days
        self. list_file = []
        self.time_label = ''
        now = datetime.today() - timedelta(days=self.days_to_subtract)

        report_conf = {
            'CANCELLAZIONI': 'SELECT distinct * FROM nps.assistenza_tecnica_report where date(data_insert_rco) = current_date() - INTERVAL X DAY'.replace(
                'X', str(self.days_to_subtract)),
            'COMPLETO': 'SELECT distinct * FROM nps.ASSISTENZA_TECNICA_STAGE where date(data_insert_rco) = current_date() - INTERVAL X DAY'.replace(
                'X', str(self.days_to_subtract)),
            'CONSOLIDATO': 'SELECT distinct * FROM nps.ASSISTENZA_TECNICA where date(data_insert_rco) = current_date() - INTERVAL X DAY'.replace(
                'X', str(self.days_to_subtract))}
        self.report_items = report_conf.items()

    def produce_reports_csv(self, dao):
        import csv
        now = datetime.today() - timedelta(days=self.days_to_subtract)
        self.time_label = now.strftime("%d-%m-%Y")

        for report_conf in self.report_items:
            report_file = '{}\{}_{}_{!s}.{}'.format(self.directory, self.file_name_start, report_conf[0],
                                                    self.time_label,
                                                    'csv')
            self.list_file.append(report_file)
            # Select data from table using SQL query.
            result = dao.select(report_conf[1])

            # Getting Field Header names
            column_names = [i[0] for i in dao.get_columns()]
            fp = open(report_file, 'w+')
            my_file = csv.writer(fp, lineterminator='\n', delimiter=';', )  # use lineterminator for windows
            my_file.writerow(column_names)
            my_file.writerows(result)
            fp.close()

    def produce_zip_report(self, nome_zip: str):
        zip_dir(nome_zip, self.directory, self.time_label )


class ConcreteBaseReportConfigurator(Creator):
    """
    Override the factory method to return an instance of a
    ConcreteProduct1.
    """

    def _factory_method(self):
        return ConcreteBaseReportNPS()


def main():
    concrete_creator = ConcreteDatabaseMySQL()
    concrete_creator.connection(host="db801rco.intranet.fw",  # your host
                                user="rogarofalo",  # username
                                passwd="R0garof4lo",  # password
                                db="nps")


if __name__ == "__main__":
    main()
