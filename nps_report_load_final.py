import mysql.connector
from nps_factory_db import ConcreteDatabaseMySQL
from nps_factory_db import ConcreteBaseReportNPS
from nps_factory_db import ConcreteBaseReportNPS_OCS_AMM
from nps_factory_db import ConcreteBaseReportNPS_OCS_TECH
from nps_mail_reports import ConcreteCreatorMailerNPS
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


    # REPORT ASSISTENZA TECNICA
    report = ConcreteBaseReportNPS(directory, 0)
    dao = ConcreteDatabaseMySQL()
    dao.connection()
    report.produce_reports_csv(dao)
    report.produce_zip_report('report_NPS_assistenza_tecnica.zip')
    lista_mail = ['giovanni.laforgia@fastweb.it', 'roberto.garofalo@consulenti.fastweb.it', 'giovanni.galgano@fastweb.it', 'roberto.garofalo@spindox.it', 'vincenzo.fioretti@fastweb.it', 'alessio.garbetta@fastweb.it']
    # lista_mail = ['roberto.garofalo@consulenti.fastweb.it','roberto.garofalo@spindox.it']


    subject = '{}{!s}{}'.format('Liste NPS_assistenza_tecnica ', time_label, ' -Caricamento coerente ')

    # message = textwrap.dedent(decorator.format(file_1, file_2, file_3))
    mail = ConcreteCreatorMailerNPS(lista_mail)
    mail.set_message(message, subject)
    nome_file_zip = report.get_file_name_zip()
    mail.set_attachment(nome_file_zip)
    mail.send_mail()

    # REPORT ASSISTENZA SINGLE CONTACT TECNICA
    report = ConcreteBaseReportNPS_OCS_TECH(directory, 0)
    dao = ConcreteDatabaseMySQL()
    dao.connection()
    report.produce_reports_csv(dao)
    report.produce_zip_report('report_NPS_OCS_assistenza_tecnica.zip')
    lista_mail = ['giovanni.laforgia@fastweb.it', 'roberto.garofalo@consulenti.fastweb.it', 'giovanni.galgano@fastweb.it', 'roberto.garofalo@spindox.it', 'vincenzo.fioretti@fastweb.it', 'alessio.garbetta@fastweb.it']
    # lista_mail = ['roberto.garofalo@consulenti.fastweb.it', 'roberto.garofalo@spindox.it']

    subject = '{}{!s}{}'.format('Liste NPS_Single Contact assistenza_tecnica ', time_label, ' -Caricamento coerente ')

    # message = textwrap.dedent(decorator.format(file_1, file_2, file_3))
    mail = ConcreteCreatorMailerNPS(lista_mail)
    mail.set_message(message, subject)
    nome_file_zip = report.get_file_name_zip()
    mail.set_attachment(nome_file_zip)
    mail.send_mail()


    # REPORT AMMINISTRATIVA SINGLE CONTACT
    report = ConcreteBaseReportNPS_OCS_AMM(directory, 0)
    dao = ConcreteDatabaseMySQL()
    dao.connection()
    report.produce_reports_csv(dao)
    report.produce_zip_report('report_NPS_OCS_amministrativa.zip')
    lista_mail = ['giovanni.laforgia@fastweb.it', 'roberto.garofalo@consulenti.fastweb.it', 'giovanni.galgano@fastweb.it', 'roberto.garofalo@spindox.it', 'arduino.panaro@fastweb.it', 'romana.mastrandrea@fastweb.it']
    # lista_mail = ['roberto.garofalo@consulenti.fastweb.it','roberto.garofalo@spindox.it']

    subject = '{}{!s}{}'.format('Liste NPS_Single Contact Amministrativa ', time_label, ' -Caricamento coerente ')

    # message = textwrap.dedent(decorator.format(file_1, file_2, file_3))
    mail = ConcreteCreatorMailerNPS(lista_mail)
    mail.set_message(message, subject)
    nome_file_zip = report.get_file_name_zip()
    mail.set_attachment(nome_file_zip)
    mail.send_mail()