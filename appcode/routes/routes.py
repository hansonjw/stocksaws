import functools
from flask import render_template, Blueprint, redirect
import yfinance as yf
import datetime
from appcode.routes.charts.chartFuncs import todayPlot
ticker = yf.Ticker('^GSPC')

bp = Blueprint('routes', __name__, url_prefix='')

@bp.route('/today', methods=(['GET']))
def today():

    # First chart...
    # Plot last 10 years of data from current date, e
    end = datetime.date.today() + datetime.timedelta(days=1)
    start = datetime.date.today() - datetime.timedelta(days=365*10)

    # Get raw data from yfinance
    raw = ticker.history(period="10y").Close
    d = raw/raw[0]

    chart1 = todayPlot(d, annLow=False, annHigh=True)

    # Second chart...

    # find start date of current cycle (max value between ep, and e), reslice data, and re-normalize
    maxDate = raw.idxmax()
    chart2 = todayPlot(raw[maxDate:end] / raw[maxDate])

    # get chart text and create list for template
    data = [chart1, chart2]

    return render_template('today.html', data=data)