import sys, base64, os, json, email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from style.colors import style
from style.banners import *

from modules.server import logFile
cache_file = "cache/cache.token"
logFile()
log_file = logFile.log_file

def storeData(sender_email, receiver_email, password):
    password_bytes  = password.encode('ascii')
    base64_bytes    = base64.b64encode(password_bytes)
    base64_password = base64_bytes.decode('ascii')
    data = {
        "credentials":{
            "sender_email": sender_email,
            "password": base64_password,
            'receiver_email': receiver_email
        }
    }
    with open(cache_file, 'w') as write_file:
        json.dump(data, write_file)


def getJsonData():
      with open(cache_file, 'r') as read_file:
            data = read_file.read()
            obj = json.loads(data)

            getJsonData.sender_mail = str(obj['credentials']['sender_email'])
            getJsonData.receiver_mail = str(obj['credentials']['receiver_email'])
            getJsonData.password = str(obj['credentials']['password'])

            base64_bytes    = getJsonData.password.encode('ascii')
            password_bytes  = base64.b64decode(base64_bytes)
            getJsonData.password = password_bytes.decode('ascii')

def sendMail(sender_email, receiver_email, password):
    subject = "FlaskLocator Log File"
    body = "Thank you for using FlaskLocator here is your latest log file:"
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message['Bcc'] = receiver_email

    message.attach(MIMEText(body, "plain"))

    with open(log_file, 'rb') as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename = {log_file}")
    message.attach(part)
    text = message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

def mailer():
    if os.path.isfile(cache_file):
        get_creds_json = input(style.GREEN("\n[+]") + style.RESET(" Do you want to get credentials saved in {} [y/n]: ").format(cache_file))
        if get_creds_json.lower() == "y":
            getJsonData()

            print(style.GREEN("\n[+]") + style.RESET(" Using the following Credentials:"))
            print(style.GREEN(" [-]") + style.RESET(" Sender Email: {}").format(getJsonData.sender_mail))
            print(style.GREEN(" [-]") + style.RESET(" Sender Email Password: {}").format(getJsonData.password))
            print(style.GREEN(" [-]") + style.RESET(" Receiver Email {}").format(getJsonData.receiver_mail))
            print(style.GREEN("\n[+]") + style.RESET(" Sending email to {}").format(getJsonData.receiver_mail))
            sendMail(getJsonData.sender_mail, getJsonData.receiver_mail, getJsonData.password)
            print(style.GREEN("[+]") + style.RESET(" Email sent to {}").format(getJsonData.receiver_mail))

        else:
            sender_mail = input(style.GREEN("\n[+]") + style.RESET(" Enter sender email: "))
            receiver_mail = input(style.GREEN("[+]") + style.RESET(" Enter receiver email: "))
            password = input(style.GREEN("[+]") + style.RESET(" Enter password sender email: "))
            save_data = input(style.GREEN("\n[+]") + style.RESET(" Do you want to save your credentials to log in automatically the next time [y/n]: "))
            if save_data == "y" or save_data == "Y":
                storeData(sender_mail, receiver_mail, password)
            print(style.GREEN("[+]") + style.RESET(" Sending email to {}").format(receiver_mail))
            sendMail(sender_mail, receiver_mail, password)
            print(style.GREEN("[+]") + style.RESET(" Email sent to {}").format(receiver_mail))
