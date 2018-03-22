import win32com.client as win32
import psutil
import os
import subprocess
from nps_factory_db import Creator
import abc

class Mail(metaclass=abc.ABCMeta):
    """
    Define the interface of objects the factory method creates.
    """

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

        def __init__(self, lista_email):
            self.lista_mail_to_send  = lista_email
            self.cur = None

        def send_mail(self):
            pass