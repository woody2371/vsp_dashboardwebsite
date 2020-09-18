#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime
import fbdataprocessing.processcsv as fbdata
import os.path, time

app = Flask(__name__)

@app.route('/')
def index():
    fbdata.loadDicts()
    lastUpdated = time.ctime(os.path.getmtime('C:\Dashboard\Dashboard Website\static\dbexport\export.csv'))
    return render_template('template.html', pickDict=fbdata.filterproductDict('pickitemstatusId',['10','11'],True), commitDict=fbdata.committedDict(), backorderDict=fbdata.filterproductDict('pickitemstatusId',['5'],True), totalqty=0, date=datetime.today(), sodict=fbdata.fullSoDict(), lastUpdated=lastUpdated)

@app.route('/pickBySales')
def pickBySales():
    fbdata.loadDicts()
    lastUpdated = time.ctime(os.path.getmtime('C:\Dashboard\Dashboard Website\static\dbexport\export.csv'))
    return render_template('template_pickBySales.html', pickDict=fbdata.filtersoDict('pickitemstatusId',['10','11'],True), commitDict=fbdata.committedDict(), backorderDict=fbdata.filterproductDict('pickitemstatusId',['5'],True), totalqty=0, date=datetime.today(), productdict=fbdata.fullProductDict(), lastUpdated=lastUpdated)

@app.route('/delete_row', methods=['GET'])
def delete_row():
    row = request.args.get('row')
    date = request.args.get('dateUntil')
    fbdata.ignoreRow(row,date)
    return 'foo'

@app.route('/ignored_orders')
def ignored_orders():
    return render_template('template_ignored.html', ignoreDict=fbdata.loadIgnoreDict())
