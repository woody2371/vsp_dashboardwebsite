#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime
import fbdataprocessing.processcsv as fbdata
import os.path, time

app = Flask(__name__)

@app.route('/WA')
def pickBySalesWA():
    fbdata.loadDicts("WA")
    lastUpdated = time.ctime(os.path.getmtime('static/dbexport/WAexport.csv'))
    return render_template('template.html', stateName="WA", pickDict=fbdata.filtersoDict('pickitemstatusId',['10','11'],True), commitDict=fbdata.committedDict("30"), backorderDict=fbdata.filterproductDict('pickitemstatusId',['5'],True), totalqty=0, date=datetime.today(), productdict=fbdata.fullProductDict(), lastUpdated=lastUpdated)

@app.route('/QLD')
def pickBySalesQLD():
    fbdata.loadDicts("QLD")
    lastUpdated = time.ctime(os.path.getmtime('static/dbexport/QLDexport.csv'))
    return render_template('template.html', stateName="QLD", pickDict=fbdata.filtersoDict('pickitemstatusId',['10','11','30'],True), commitDict=fbdata.committedDict("40"), backorderDict=fbdata.filterproductDict('pickitemstatusId',['5'],True), totalqty=0, date=datetime.today(), productdict=fbdata.fullProductDict(), lastUpdated=lastUpdated)

@app.route('/SILVER')
def pickBySalesSILVER():
    fbdata.loadDicts("SILVER")
    lastUpdated = time.ctime(os.path.getmtime('static/dbexport/export.csv'))
    return render_template('template.html', stateName="Silverwater", pickDict=fbdata.filtersoDict('pickitemstatusId',['10','11'],True), commitDict=fbdata.committedDict(), backorderDict=fbdata.filterproductDict('pickitemstatusId',['5'],True), totalqty=0, date=datetime.today(), productdict=fbdata.fullProductDict(), lastUpdated=lastUpdated)

@app.route('/SP')
def pickBySalesSP():
    fbdata.loadDicts("SP")
    lastUpdated = time.ctime(os.path.getmtime('static/dbexport/export.csv'))
    return render_template('template.html', stateName="St Peters", pickDict=fbdata.filtersoDict('pickitemstatusId',['10','11'],True), commitDict=fbdata.committedDict(), backorderDict=fbdata.filterproductDict('pickitemstatusId',['5'],True), totalqty=0, date=datetime.today(), productdict=fbdata.fullProductDict(), lastUpdated=lastUpdated)

@app.route('/VIC')
def pickBySalesVIC():
    fbdata.loadDicts("VIC")
    lastUpdated = time.ctime(os.path.getmtime('static/dbexport/export.csv'))
    return render_template('template.html', stateName="VIC", pickDict=fbdata.filtersoDict('pickitemstatusId',['10','11'],True), commitDict=fbdata.committedDict(), backorderDict=fbdata.filterproductDict('pickitemstatusId',['5'],True), totalqty=0, date=datetime.today(), productdict=fbdata.fullProductDict(), lastUpdated=lastUpdated)

@app.route('/delete_row', methods=['GET'])
def delete_row():
    row = request.args.get('row')
    date = request.args.get('dateUntil')
    fbdata.ignoreRow(row,date)
    return 'foo'

@app.route('/ignored_orders')
def ignored_orders():
    return render_template('template_ignored.html', ignoreDict=fbdata.loadIgnoreDict())

@app.route('/dell')
def dell():
    lastUpdated = time.ctime(os.path.getmtime(fbdata.latestDellFile()))
    return render_template('template_dell.html', orderDict=fbdata.loadDellPODict(), deliveredDict=fbdata.loadDellDeliveredDict(), lastUpdated=lastUpdated)