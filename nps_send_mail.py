import win32com.client as win32
import psutil
import os
import subprocess


# Drafting and sending email notification to senders. You can add other senders' email in the list
def send_notification():
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0x0)
    mail.To = 'roberto.garofalo@consulenti.fastweb.it'
    mail.Subject = 'Sent through Python'
    mail.body = 'This email alert is auto generated. Please do not respond.'
    mail.send



# Open Outlook.exe. Path may vary according to system config
# Please check the path to .exe file and update below

def open_outlook():
    try:
        subprocess.call(['C:\\Program Files\\Microsoft Office\\Office14\\Outlook.exe'])
        #os.system("C:\Program Files\Microsoft Office\Office15\Outlook.exe");
    except:
        print("Outlook didn't open successfully")


# Checking if outlook is already opened. If not, open Outlook.exe and send email
for item in psutil.pids():
    p = psutil.Process(item)
    if p.name() == "OUTLOOK.EXE":
        flag = 1
        break
    else:
        flag = 0

if (flag == 1):
    send_notification()
else:
    open_outlook()
    send_notification()