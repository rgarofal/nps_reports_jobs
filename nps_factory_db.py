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
    def _factory_method(self, type_report="NONE"):
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
        self.list_file = []
        self.time_label = ''
        self.zip_file_name = None
        now = datetime.today() - timedelta(days=self.days_to_subtract)

        report_conf = {
            'CANCELLAZIONI': 'SELECT distinct * FROM nps.assistenza_tecnica_report where date(data_insert_rco) = current_date() - INTERVAL X DAY'.replace(
                'X', str(self.days_to_subtract)),
            'COMPLETO': 'SELECT distinct * FROM nps.ASSISTENZA_TECNICA_STAGE where date(data_insert_rco) = current_date() - INTERVAL X DAY'.replace(
                'X', str(self.days_to_subtract)),
            'CONSOLIDATO': 'SELECT distinct * FROM nps.ASSISTENZA_TECNICA where date(data_insert_rco) = current_date() - INTERVAL X DAY'.replace(
                'X', str(self.days_to_subtract)),
            'REP_CONSOLIDATO': 'SELECT distinct * FROM nps.REPORT_NPS_ASSTEC where date(data_insert_rco) = current_date() - INTERVAL X DAY'.replace(
                'X', str(self.days_to_subtract))
        }
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
        nome_zip_file = '{}\{}_{!s}.{}'.format(self.directory, nome_zip, self.time_label,
                                               'zip')
        # filtro_file = '{}{!s}.{}'.format('*', self.time_label, 'csv')
        filtro_file = '{!s}{!s}.{}'.format(self.file_name_start + '*', self.time_label, 'csv')
        self.zip_file_name = nome_zip_file
        zip_dir(nome_zip_file, self.directory, filtro_file)

    def get_file_name_zip(self):
        return self.zip_file_name


class ConcreteBaseReportNPS_OCS_TECH(Report):
    """
    Implement the Report interface.
    """

    def __init__(self, directory_log, interval_days=0):
        self.directory = directory_log
        self.report_conf = dict()
        self.file_name_start = 'F_report_single_contact_ass_tecnica_'
        self.days_to_subtract = interval_days
        self.list_file = []
        self.time_label = ''
        self.zip_file_name = None
        now = datetime.today() - timedelta(days=self.days_to_subtract)

        report_conf = {
            'CANCELLAZIONI': 'SELECT distinct * FROM nps.assistenza_tecnica_ocs_report where date(data_insert_rco) = current_date() - INTERVAL X DAY'.replace(
                'X', str(self.days_to_subtract)),
            'COMPLETO': 'SELECT distinct * FROM nps.ASSISTENZA_TECNICA_OCS_STAGE where date(data_insert_rco) = current_date() - INTERVAL X DAY'.replace(
                'X', str(self.days_to_subtract)),
            'CONSOLIDATO': 'SELECT distinct * FROM nps.ASSISTENZA_TECNICA_OCS where date(data_insert_rco) = current_date() - INTERVAL X DAY'.replace(
                'X', str(self.days_to_subtract)),
            'REP_CONSOLIDATO': 'SELECT distinct * FROM nps.REPORT_NPS_ASSTEC_OCS where date(data_insert_rco) = current_date() - INTERVAL X DAY'.replace(
                'X', str(self.days_to_subtract))
        }
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
        nome_zip_file = '{}\{}_{!s}.{}'.format(self.directory, nome_zip, self.time_label,
                                               'zip')
        # filtro_file = '{}{!s}.{}'.format('*', self.time_label, 'csv')
        filtro_file = '{!s}{!s}.{}'.format(self.file_name_start + '*', self.time_label, 'csv')
        self.zip_file_name = nome_zip_file
        zip_dir(nome_zip_file, self.directory, filtro_file)

    def get_file_name_zip(self):
        return self.zip_file_name


class ConcreteBaseReportNPS_OCS_AMM(Report):
    """
    Implement the Report interface.
    """

    def __init__(self, directory_log, interval_days=0):
        self.directory = directory_log
        self.report_conf = dict()
        self.file_name_start = 'F_report_single_contact_amministrativa_'
        self.days_to_subtract = interval_days
        self.list_file = []
        self.time_label = ''
        self.zip_file_name = None
        now = datetime.today() - timedelta(days=self.days_to_subtract)

        report_conf = {
            'CANCELLAZIONI': 'SELECT distinct * FROM nps.amministrativa_ocs_report where date(data_insert_rco) = current_date() - INTERVAL X DAY'.replace(
                'X', str(self.days_to_subtract)),
            'COMPLETO': 'SELECT distinct * FROM nps.AMMINISTRATIVA_OCS_STAGE where date(data_insert_rco) = current_date() - INTERVAL X DAY'.replace(
                'X', str(self.days_to_subtract)),
            'CONSOLIDATO': 'SELECT distinct * FROM nps.AMMINISTRATIVA_OCS where date(data_insert_rco) = current_date() - INTERVAL X DAY'.replace(
                'X', str(self.days_to_subtract)),
            'REP_CONSOLIDATO': 'SELECT distinct * FROM nps.REPORT_NPS_AMM_OCS where date(data_insert_rco) = current_date() - INTERVAL X DAY'.replace(
                'X', str(self.days_to_subtract))
        }
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
        nome_zip_file = '{}\{}_{!s}.{}'.format(self.directory, nome_zip, self.time_label,
                                               'zip')
        # filtro_file = '{}{!s}.{}'.format('*', self.time_label, 'csv')
        filtro_file = '{!s}{!s}.{}'.format(self.file_name_start + '*', self.time_label, 'csv')
        self.zip_file_name = nome_zip_file
        zip_dir(nome_zip_file, self.directory, filtro_file)

    def get_file_name_zip(self):
        return self.zip_file_name


class ConcreteBaseReportConfigurator(Creator):
    """
    Override the factory method to return an instance of a
    ConcreteProduct1.
    """

    def _factory_method(self, type_report):
        if type_report == "NPS_TECH":
            return ConcreteBaseReportNPS()
        if type_report == "NPS_OCS_TECH":
            return ConcreteBaseReportNPS_OCS_TECH()
        if type_report == "NPS_OCS_AMM":
            return ConcreteBaseReportNPS_OCS_AMM()
        if type_report == "NONE":
            print("Warning type of concrete report not set")
            return None


def main():
    concrete_creator = ConcreteDatabaseMySQL()
    concrete_creator.connection(host="db801rco.intranet.fw",  # your host
                                user="rogarofalo",  # username
                                passwd="R0garof4lo",  # password
                                db="nps")


if __name__ == "__main__":
    main()
