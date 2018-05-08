import win32com.client as win32
import psutil
import os
import subprocess
from os import PathLike
from typing import Union

from nps_factory_db import Creator
import abc

class Mail(metaclass=abc.ABCMeta):
    """
    Define the interface of objects the factory method creates.
    """

    @abc.abstractmethod
    def set_message(self, message, subject, zip_file):
        pass
    @abc.abstractmethod
    def send_mail(self):
        pass


class ConcreteCreatorMailer (Creator):
    """
    Override the factory method to return an instance of a
    ConcreteProduct1.
    """

    def _factory_method(self):
        return ConcreteCreatorMailerNPS()

class ConcreteCreatorMailerNPS(Mail):
        """
        Implement the Product interface.
        """

        def __init__(self, lista_email: list):
            self.lista_mail_to_send  = ';'.join(lista_email)
            self.cur = None
            self.subject = None
            self.message = None
            self.mail = None

        def set_message(self, message: str, subject: str):
            self.message = message
            self.subject = subject
            outlook = win32.Dispatch('outlook.application')
            self.mail = outlook.CreateItem(0x0)
            self.mail.To = self.lista_mail_to_send
            self.mail.Subject = subject
            self.mail.HtmlBody = message
            #self.mail.Display(True)

        def set_attachment(self, zip_name: Union[str, PathLike]):
            self.mail.Attachments.Add(zip_name)

        def send_mail(self):
            self.mail.send