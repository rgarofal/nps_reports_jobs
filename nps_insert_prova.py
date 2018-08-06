from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector
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

    parser.add_argument('-t', '--table',
                        default='trb2',
                        help='tabella su cui fare insert',
                        required=False)
    parser.add_argument('-c', '--colonne',
                        default='id, fname, lname, hired,separated,job_code, store_id',
                        help='colonne tabella su cui fare insert',
                        required=False)
    args = parser.parse_args()

    directory = args.directory_report
    table = args.table
    colonne = args.colonne
    print("Directory report = ", directory)
    print("Tabella selezionata = ", table )
    print("Colonne = ", colonne)

    # import textwrap
    #
    # PARTE COMUNE PER i REPORT
    #
    decorator = """\
                   Ciao a tutti

                   Come richiesto vi invio i reports in formato zip 

                   A disposizione

                   Roberto
                  """
    message = decorator
    days_to_subtract = 0
    now = datetime.today() - timedelta(days=days_to_subtract)
    time_label = now.strftime("%d-%m-%Y")

    host_n = "db801rco.intranet.fw"  # your host
    user_n = "rogarofalo"  # username
    passwd_n = "R0garof4lo" # password
    db_n = "nps"

    cnx = mysql.connector.connect(host=host_n,user=user_n, password= passwd_n, database=db_n)
    cursor = cnx.cursor()

    #dao = ConcreteDatabaseMySQL()
    #dao.connection()
# insert into trb2 (id, fname, lname, hired,separated,job_code, store_id) values (2,'pippo3', 'pluto3', date(now() - interval 2 year), date(now()), 12, 13);
    for i in range(1,4000):
        for yy in range (1, 4):
            for num in range(1,1000):
                #statement = 'insert into {1} ({2}) values ({3}, ''username_{4}'', ''surname_{5}'', date(now() - interval {6} year),date(now()), 12, 13)',format(table,colonne ,i, num, num, yy)
                statement =("INSERT INTO trb2 "
                 "(id, fname, lname, hired, separated, job_code, store_id) "
                 "VALUES ( %s, %s, %s, %s, %s, %s, %s );")
                data  =  '(%s, username_%s, surname_%s, date(now() - interval %s year),date(now()), 12, 13)' %(i, num, num, yy)
                print(data)
                print(statement)
                #dao.insert(statement)
                statement_finale = 'INSERT INTO trb2 (id, fname, lname, hired, separated, job_code, store_id) VALUES %s' & (data)
                print(statement_finale)
                #cursor.execute(statement, data)
                cursor.execute(statement_finale)
    cnx.commit()

    cursor.close()
    cnx.close()
