import mysql.connector
from nps_factory_db import ConcreteDatabaseMySQL
from nps_factory_db import ConcreteBaseReportNPS
import argparse

import csv
from datetime import datetime, timedelta


def help_msg():
    """ help to describe the script"""
    help_str = """
               """
    return help_str


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=help_msg())
    parser.add_argument('-d', '--directory_report',
                        default='C:\\Users\\rogarofalo\\Documents\\WorkingEnv\\NPS_ASSISTENZA_TECNICA\\Working_AssistenzaTecnica\\REPORT_GIORNALIERI',
                        help='Directory dove risiedono i report ', required=False)

    args = parser.parse_args()

    directory = args.directory_report
    print(directory)

    days_to_subtract = 0
    report = ConcreteBaseReportNPS(directory, 0)
    dao = ConcreteDatabaseMySQL()
    dao.connection()
    report.produce_reports_csv(dao)
    lista_mail = ['giovanni.laforgia@fastweb.it', 'roberto.garofalo@consulenti.fastweb.it', 'giovanni.galgano@fastweb.it', 'roberto.garofalo@spindox.it', 'vincenzo.fioretti@fastweb.it', 'clara.scardicchio@fastweb.it', 'alessio.garbetta@fastweb.it']
    import textwrap
    file_1 = directory + '\\file_A'
    file_2 =  directory + '\\file_A'
    file_3 =  directory + '\\file_A'
    decorator = """\
                Ciao a tutti

                Come richiesto mando i seguenti report per la data odierna :

                 1) base dati campione completo (report (1))
                 2) base dati consolidato       (report (2))
                 3) base dati cancellazioni     (report (3))


                A disposizione

                Roberto
               """

    message = textwrap.dedent(decorator.format(file_1, file_2, file_3))

