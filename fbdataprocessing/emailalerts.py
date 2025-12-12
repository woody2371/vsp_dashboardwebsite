#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import csv
import smtplib
import processcsv as fbdata
import configparser

cfg = configparser.ConfigParser()
cfg.read('config.ini')


fbdata.loadDicts("WA")

table1_init = "<p class=MsoNormal><b>Previous orders:<o:p></o:p></b></p> <table class=MsoTableGrid border=1 cellspacing=0 cellpadding=0 style='border-collapse:collapse;border:none'>"
table2_init = "<p class=MsoNormal><b>New orders from today:<o:p></o:p></b></p> <table class=MsoTableGrid border=1 cellspacing=0 cellpadding=0 style='border-collapse:collapse;border:none'>"
#Header string. Args are: Company, SOnum, Days
table_header = "<tr><td width=208 valign=top style='width:155.8pt;border:solid windowtext 1.0pt;background:#D9E2F3;padding:0cm 5.4pt 0cm 5.4pt'><p class=MsoNormal><b><span style='color:black'>{}</span><o:p></o:p></b></p></td><td width=208 valign=top style='width:155.85pt;border:solid windowtext 1.0pt;border-left:none;background:#D9E2F3;padding:0cm 5.4pt 0cm 5.4pt'><p class=MsoNormal><b><span style='color:black'>{}</span><o:p></o:p></b></p></td><td width=208 valign=top style='width:155.85pt;border:solid windowtext 1.0pt;border-left:none;background:#D9E2F3;padding:0cm 5.4pt 0cm 5.4pt'><p class=MsoNormal><span style='color:black'>Last checked <b>{}</b> days ago</span><o:p></o:p></p></td></tr>\n"
#Row string. Args are: Product, Qty
table_row = "<tr><td width=208 valign=top style='width:155.8pt;border:solid windowtext 1.0pt;border-top:none;padding:0cm 5.4pt 0cm 5.4pt'><p class=MsoNormal><o:p>&nbsp;</o:p></p></td><td width=208 valign=top style='width:155.85pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0cm 5.4pt 0cm 5.4pt'><p class=MsoNormal>{}<o:p></o:p></p></td><td width=208 valign=top style='width:155.85pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0cm 5.4pt 0cm 5.4pt'><p class=MsoNormal>{}<o:p></o:p></p></td></tr>\n"

salesmanDict = {'vincep': 'vince', 'vincel': 'vincel', 'glennh': 'glennh', 'tom': 'tom', 'andrew':'andrewh'}
#salesmanDict = {'vincep': 'tom', 'vincel': 'tom', 'glennh': 'tom', 'ryang': 'tom', 'andrewh': 'tom', 'tom': 'tom'}

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
        print(e)
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

def createMsg(salesman,email):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Committed Sales for {}".format(salesman)
    message["From"] = 'tom@vspsolutions.com.au'
    message["To"] = '{}@vspsolutions.com.au'.format(email)
    
    committed = fbdata.committedBySalesman(salesman)
    daysold = "0"
    table1 = table1_init
    table2 = table2_init
    if len(committed) <= 1:
        return "Do not send"
    for line in committed:
        if str(committed[line][0]['dateLastModified']).split(" ")[0] == (str(datetime.today())).split(" ")[0]:
            daysold = "Today"
        else:
            daysold = ((str(datetime.today() - committed[line][0]['dateLastModified']))).split(',')[0]
        if committed[line][0]['num'] in soDeliveryList:
            table1 += table_header.format(committed[line][0]['billToName'], committed[line][0]['num'], daysold)
            for row in committed[line]:
                table1 += table_row.format(row['productNum'], row['qty'])
        else:
            table2 += table_header.format(committed[line][0]['billToName'], committed[line][0]['num'], daysold)
            soDeliveryList.append(committed[line][0]['num'])
            for row in committed[line]:
                table2 += table_row.format(row['productNum'], row['qty'])
    table1 += "</table>"
    table2 += "</table>"
    msg = table2 + table1
    part1 = MIMEText(msg, "html")
    message.attach(part1)
    return message

def updateEmailCSV(soList):
    with open(cfg['EMAIL']['emailpath']+"emailDeliveryList.csv", mode='w', newline='') as emailcsv:
        csv_writer = csv.writer(emailcsv)
        csv_writer.writerow(soList)

def loadEmailCSV():
    returnList = []
    with open(cfg['EMAIL']['emailpath']+"emailDeliveryList.csv", mode='r', newline='') as emailcsv:
        csv_reader = csv.reader(emailcsv)
        for row in csv_reader:
            for column in row:
                returnList.append(column)
    return returnList

soDeliveryList = loadEmailCSV()

for key in salesmanDict:
    print("Creating {}'s email".format(key))
    msg = createMsg(key,salesmanDict[key])
    if msg == "Do not send":
        print("No sales orders for {}".format(key))
        continue
    else:
        sendEmail(msg)
    print("Finished {}'s email".format(key))

updateEmailCSV(soDeliveryList)




