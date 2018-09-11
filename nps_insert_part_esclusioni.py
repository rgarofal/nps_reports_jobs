from __future__ import print_function

import mysql.connector
import argparse


def help_msg():
    """ help to describe the script"""
    help_str = """
               """
    return help_str


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=help_msg())
    parser.add_argument('-d', '--directory_report',
                        default='C:\\Users\\rogarofalo\\Documents\\REPORT_INSERT',
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
    print("Tabella selezionata = ", table)
    print("Colonne = ", colonne)

    host_n = "db801rco.intranet.fw"  # your host
    user_n = "rogarofalo"  # username
    passwd_n = "R0garof4lo"  # password
    db_n = "nps"
    flusso_str = {1: 'FLUX_1', 2: 'FLUX_2', 3: 'FLUX_4', 4: 'FLUX_4', 5: 'FLUX_5', 6: 'FLUX_6', 7: 'FLUX_7',
                  8: 'FLUX_8'}
    cnx = mysql.connector.connect(host=host_n, user=user_n, password=passwd_n, database=db_n)
    cursor = cnx.cursor()

    for k in range(1, 8):
        for i in range(1, 1000000):
            data = '(%s, "%s")' % (i, flusso_str[k])
            print(data)
            # print(statement)
            # dao.insert(statement)
            statement_finale = 'INSERT INTO part_trial (ACC_ID, FLUSSO) VALUES ' + data
            print(statement_finale)
            # cursor.execute(statement, data)
            cursor.execute(statement_finale)
    cnx.commit()

    cursor.close()
    cnx.close()
