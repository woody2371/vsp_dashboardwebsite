#!/usr/bin/python
# -*- coding: utf-8 -*-

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini')

def sendEmail(message):
    #Send an email
    #
    #message is an object created by the createMsg function
    ###
    try:
        username = cfg['EMAIL']['username']
        password = cfg['EMAIL']['password']
        server = smtplib.SMTP(cfg['EMAIL']['server'], cfg['EMAIL']['port'])  
        server.ehlo()
        server.login(username, password)  
        server.sendmail(message["From"], message["To"], message.as_string())  
    except Exception as e:
        print(f"Encountered an error while sending an email: {e}")
    finally:
        server.quit()

def createMsgGeneric(subject, fromEmail, toEmail, content):
    #Creates an email, intending to be passed to sendEmail
    #Generic - have to format your own message and pass it as content
    #
    ###
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = fromEmail
    message["To"] = toEmail
    message.attach(MIMEText(content))
    return message