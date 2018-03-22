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
