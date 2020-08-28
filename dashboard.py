#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime
import fbdataprocessing.processcsv as fbdata

app = Flask(__name__)

@app.route('/')
def index():
    fbdata.loadDicts()
    return render_template('template.html', pickDict=fbdata.filterproductDict('pickitemstatusId',['10','11'],True), commitDict=fbdata.committedDict(), backorderDict=fbdata.filterproductDict('pickitemstatusId',['5'],True), totalqty=0, date=datetime.today(), sodict=fbdata.fullSoDict())