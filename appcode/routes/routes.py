import functools
from flask import render_template, Blueprint, redirect
import yfinance as yf
import datetime
from appcode.routes.charts.chartFuncs import todayPlot, histPlot, barAnnual, lineDebt
import urllib.request, json
ticker = yf.Ticker('^GSPC')
import pandas as pd

# trying something...
import ssl

bp = Blueprint('routes', __name__, url_prefix='')

@bp.route('/today', methods=(['GET']))
def today():
    
    # Get raw data from yfinance
    raw = ticker.history(period="10y").Close.asfreq('D', method='bfill')
    d = raw/raw[0]

    # First chart...
    # Plot last 10 years of data from current date, e
    end = datetime.date.today() + datetime.timedelta(days=1)
    start = datetime.date.today() - datetime.timedelta(days=365*10)
    chart1 = todayPlot(d.asfreq('D'), annLow=False, annHigh=True, annGr=True)

    # Second chart...
    # find start date of current cycle (max value between ep, and e), reslice data, and re-normalize
    maxDate = raw.idxmax()
    chart2 = todayPlot(raw[maxDate:end] / raw[maxDate], annLow=True, annHigh=False, annGr=False)

    # get chart text and create list for template
    data = [chart1, chart2]

    return render_template('today.html', data=data)


@bp.route('/history', methods=(['GET']))
def history():
    # yFinance, get raw data
    raw = ticker.history(period="max")

    # call plot functions and pass to data aray
    data=[barAnnual(raw), histPlot(raw, growth=True, log=False), histPlot(raw, growth=True, log=True)]

    # pass data arraw for rendering, data needs to be .png file pointers
    return render_template('history.html', data=data)


@bp.route('/debt', methods=(['GET']))
def debt():
    ssl._create_default_https_context = ssl._create_unverified_context
    url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_outstanding?sort=-record_date&format=json&page[number]=1&page[size]=10000"
    response = urllib.request.urlopen(url)
    print(response.status)
    feddata = response.read()
    dict = json.loads(feddata)
    
    fiscal_year = []
    debt = []
    for d in dict["data"]:
        # print(type(float(d["debt_outstanding_amt"])), type(d["record_fiscal_year"]))
        debt.append(float(d["debt_outstanding_amt"]))
        fiscal_year.append(int(d["record_fiscal_year"]))
    
    debtData = pd.DataFrame({'year':fiscal_year, 'debt':debt})
    
    data = [ lineDebt(debtData) ]
    return render_template('debt.html', data=data)