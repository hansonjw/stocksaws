import base64
from io import BytesIO
# import matplotlib.pyplot as plt
import matplotlib
from matplotlib.figure import Figure
import datetime
import pandas as pd
import numpy as np


class colorDictObj:

    def __init__(self, cycDf):
        self._cycDf = cycDf
        self.colorDict = {}
        self.colorsShort = ['#B2EBF2', '#80DEEA', '#4DD0E1', '#26C6DA', '#00BCD4', '#00ACC1', '#0097A7', '#00838F', '#006064', '#84FFFF', '#18FFFF']
        self.colorsMed = ['#B9F6CA', '#A5D6A7', '#81C784', '#66BB6A', '#4CAF50', '#43A047', '#388E3C', '#2E7D32', '#1B5E20']
        self.colorsLong = ['#F8BBD0', '#F06292', '#C2185B', '#880E4F']
        self.setColorDict()

    def setColorDict(self):

        s = self.colorsShort
        m = self.colorsMed
        l = self.colorsLong

        cyclesShort = self._cycDf.query('duration<=250')['title'].tolist()
        for cyc in cyclesShort:
            self.colorDict[cyc] = s.pop()

        cyclesMed = self._cycDf.query('duration>250 & duration<1000')['title'].tolist()
        for cyc in cyclesMed:
            self.colorDict[cyc] = m.pop()
        
        cyclesLong = self._cycDf.query('duration>1000')['title'].tolist()
        for cyc in cyclesLong:
            self.colorDict[cyc] = l.pop()
        return

    def getColorDict(self):
        return self.colorDict


def todayPlot(d, annLow=False, annHigh=False, annGr=False):
    fig = Figure(figsize=(10,6))
    # fig = Figure()
    chart = fig.subplots()

    x1 = d.index
    y1 = d.values
    chart.plot(x1, y1, color='#2874A6', marker='', linewidth=1)
    
    chart.set_xlabel('Date')
    highDate = d.index[0]

    # Annotate Chart
    today_val = d[-1]
    start_val = d[0]
    min_val = d.min()
    today_date = d.index[-1]
    start_date = d.index[0]
    min_date = d.idxmin()
    dateF = today_date.to_pydatetime().strftime("%b %d, %Y")
    dateS = start_date.to_pydatetime().strftime("%b %d, %Y")
    dateM = min_date.to_pydatetime().strftime("%b %d, %Y")
    annCagr = ""

    if annGr:
        y2 = [1]
        dgr = (y1[-1]/y1[0])**(1/len(y1)) - 1
        for x in x1[1:]:
            y2.append(y2[-1]*(1+dgr))
        chart.plot(x1, y2, color='grey', marker='', linewidth=.5)
        annCagr = f"\nCAGR: {round(dgr*365*100, 2)}%"


    if annLow:
        strToday = f"{dateF}:\n {round(today_val*100-100, 1)}%"
        strStart = f"{dateS}:\n {round(start_val*100)}%"
        strMin = f"{dateM}:\n {round(min_val*100-100, 1)}%"
        chart.plot([today_date, start_date, min_date],[today_val, start_val, min_val], marker="o", linestyle="None", color='#DC7633')
        chart.text(min_date, min_val, strMin, color='#DC7633')
        chart.text(x1[-1], y1[-1], strToday, color='#DC7633')
        chart.text(x1[0], y1[0], strStart, color='#DC7633')
        chart.set_title(f"S&P 500 - Since all time high on {highDate.to_pydatetime().strftime('%b %d, %Y')}")
    else:
        strToday = f"{dateF}: {round(today_val, 1)}" + annCagr
        strStart = f"{dateS}: {round(start_val)}"
        chart.plot([today_date, start_date],[today_val, start_val], marker="o", linestyle="None", color='#DC7633')
        chart.text(x1[-1], y1[-1], strToday, color='#DC7633')
        chart.text(x1[0], y1[0], strStart, color='#DC7633')
        chart.set_title(f"S&P 500 - Last 10 years")

    if annHigh:
        maxVal = d.max()
        maxDate = d.idxmax()
        maxDateStr = maxDate.to_pydatetime().strftime("%b %d, %Y")
        strMax = f"{maxDateStr}:\n {round(maxVal, 1)}"
        chart.plot(maxDate, maxVal, marker="o", linestyle="None", color='#DC7633')
        chart.text(maxDate, maxVal, strMax, color='#DC7633')


    # turn off top and right side frame borders
    chart.spines["right"].set_visible(False)
    chart.spines["top"].set_visible(False)
    
    # return image/png file
    buf = BytesIO()
    fig.savefig(buf, format="png")
    return base64.b64encode(buf.getbuffer()).decode("ascii")


def histPlot(din, growth=False, log=False):
    
    # munge data
    newDateRange = pd.date_range('1/1/1950', din.index[-1]) 
    d = din.Close.reindex(newDateRange, method='bfill')/din.Close[0]

    # create basic Plot
    fig = Figure(figsize=(10,6))
    chart = fig.subplots()
    x1 = d.index
    y1 = d.values
    chart.plot(x1, y1, color='#2874A6', marker='', linewidth=0.5)

    # formatting for the chart
    chart.set_xlabel('Year-Week')
    chart.grid(True, linestyle='-', zorder=0, linewidth=0.1, color='#3498DB')
    chart.tick_params(labelcolor='black')
    chart.set_title("S&P 500 Historical Prices")

    # Annotate starting and ending datapoints and strings...
    dateS = x1[0].to_pydatetime().strftime("%b %d, %Y")
    dateE = x1[-1].to_pydatetime().strftime("%b %d, %Y")
    start_val = y1[0]
    end_val = y1[-1]
    strStart = f" {dateS}: {round(start_val)}"
    strEnd = f" {dateE}: {round(end_val)}"
    chart.plot([x1[0], x1[-1]],[start_val, end_val], marker="o", linestyle="None", color='#DC7633')

    # If growth flag is True, growth curves will be plotted
    if growth == True:
        
        # Calculate growth curves
        dgr = ((d[-1]/d[0]) ** (1/len(d)))
        dgrHi = ((dgr - 1)*365*100+.5)/(365*100) + 1
        dgrLo = ((dgr - 1)*365*100-.5)/(365*100) + 1
        
        y2, y3, y4 = [1], [1], [1]
        for n in range(len(x1)-1):
            y2.append(y2[-1]*(dgr))
            y3.append(y3[-1]*(dgrHi))
            y4.append(y4[-1]*(dgrLo))

        # add growth curves to plot
        chart.plot(x1, y2, color='#E67E22', marker='', linewidth=1.0)
        chart.plot(x1, y3, color='#F8C471', marker='', linewidth=0.5)
        chart.plot(x1, y4, color='#F8C471', marker='', linewidth=0.5)

        # Annotate growth curve with rate and ending value...
        cagr = 365 * (dgr-1)
        # strEnd = f" {dateE}: {round(end_val)}\n (CAGR: {round(cagr*100, 2)}%)"
        strEnd = f"CAGR: {round(cagr*100, 2)}%"

        chart.text(x1[-1], y3[-1], f"{round(cagr*100+0.5, 2)}% (+0.5%)", color='#DC7633')
        chart.text(x1[-2], y4[-2], f"{round(cagr*100-0.5, 2)}% (-0.5%)", color='#DC7633')

    # Options for log scale
    if log == True:
        chart.set_yscale('log')
        chart.set_title("S&P 500 Historical Prices (Log Scale)")

    chart.text(x1[0], y1[0], strStart, color='#DC7633')
    chart.text(x1[-1], y1[-1]+5, strEnd, color='#DC7633')

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    return base64.b64encode(buf.getbuffer()).decode("ascii")


def lineDebt(d):
    # munge data
    d.sort_values(by=['year'], inplace=True)
    d.debtTr = d.debt/10**12

    dFilter = d.query('year>=1900')

    # chart basics
    fig = Figure(figsize=(10,6))
    chart = fig.subplots()
    x1 = d.year
    y1 = d.debtTr
    chart.stackplot(x1, y1, color='#2874A6')

    # Annotate chart
    chart.set(xlim=(1900, 2025), xticks=np.arange(1900, 2025, 10), ylim=(0, 40), yticks=np.arange(0, 40, 5))
    chart.set_title("Historical U.S. Federal Debt, $T   (source: https://fiscaldata.treasury.gov/")
    strEnd = f"${round(y1.iloc[-1], 1)}T"
    chart.text(x1.iloc[-1]-10, y1.iloc[-1], strEnd, color='#DC7633')
    
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")

    # Embed the result in the html output.
    return base64.b64encode(buf.getbuffer()).decode("ascii")


def deltaGrowthPlot(d):
    # Chart 3!!
    fig = Figure(figsize=(10,6))
    chart = fig.subplots()
    x1 = d.wkLowDate
    y1 = d.deltaGrowthHigh
    x2 = d.wkLowDate
    y2 = d.deltaGrowthLow

    chart.plot(x1, y1, color='blue', marker='', linewidth=0.5)
    chart.plot(x2, y2, color='orange', marker='', linewidth=0.5)

    # formatting for the chart
    chart.set_xlabel('Year-Week')
    chart.grid(True, linestyle='-', zorder=0, linewidth=0.1, color='#3498DB')
    chart.tick_params(labelcolor='black')
    chart.set_title("")

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    return base64.b64encode(buf.getbuffer()).decode("ascii")


def allCycles(df, cycDf, colorObj):

    colors = colorObj.getColorDict()

    # chart and figure 1
    fig = Figure(figsize=(10,6))
    chart = fig.subplots()
    for col in df.drop('current', axis=1):
        chart.plot(df[col], marker='', linewidth=0.5, alpha=0.5, color=colors[col])
    chart.plot(df.current, color='black', linewidth=1.0)

    # set chart display options
    chart.legend(loc='lower right', labels=df.keys(), fontsize='xx-small')
    chart.set_xlabel('Days since Peak')
    chart.set_title("Stock Market Declines Since 1950")
    chart.axis(xmin=0, xmax=3000)
    chart.axis(ymin=.4, ymax=1)

    # Set background colors
    chart.axvspan(0, 300, facecolor='lightblue', alpha=0.2)
    chart.axvspan(300, 1000, facecolor='lightgreen', alpha=0.2)
    chart.axvspan(1000, 3000, facecolor='pink', alpha=0.2)

    # Save fig/chart to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    return base64.b64encode(buf.getbuffer()).decode("ascii")


def shortCycles(df, cycDf, colorObj):

    colors = colorObj.getColorDict()
    cyclesShort = cycDf.query('duration<=250')['title'].tolist()

    fig = Figure(figsize=(10,6))
    chart = fig.subplots()
    for cyc in cyclesShort:
        min=df[cyc].min()
        minDate = df[cyc].idxmin()
        chart.plot(minDate, min, marker='o', color=colors[cyc])
        chart.plot(df[cyc], marker='', linewidth=1.0, alpha=1, color=colors[cyc], label='_nolegend_')
        chart.text(minDate, min, f"-{round(100*(1-min))}%", color = colors[cyc])
    chart.plot(df.current, color='black', linewidth=1.0)

    c = df.current[df.current.notnull()]
    chart.plot(c.index[-1], c[c.index[-1]], marker='o', color='black', label='_nolegend_')
    chart.text(c.index[-1], c[c.index[-1]], f"-{round(100*(1-c[c.index[-1]]) )}%", color='black')

    cyclesShort.append('Current')

    # set chart display options
    chart.legend(loc='lower right', labels=cyclesShort, fontsize='xx-small')
    chart.set_xlabel('Days since Peak')
    chart.set_title("Short Term Stock Market Cycles")
    chart.axis(xmin=0, xmax=300)
    chart.axis(ymin=.6, ymax=1)

    # set background color
    chart.axvspan(0, 300, facecolor='lightblue', alpha=0.2)


    # Save fig/chart to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
   
    return base64.b64encode(buf.getbuffer()).decode("ascii")


def medCycles(df, cycDf, colorObj):

    colors = colorObj.getColorDict()
    cyclesMed = cycDf.query('duration>250 & duration<1000')['title'].tolist()

    fig = Figure(figsize=(10,6))
    chart = fig.subplots()
    for cyc in cyclesMed:
        min=df[cyc].min()
        minDate = df[cyc].idxmin()
        chart.plot(minDate, min, marker='o', color=colors[cyc])
        chart.plot(df[cyc], marker='', linewidth=1.0, alpha=1, color=colors[cyc], label='_nolegend_')
        chart.text(minDate, min, f"-{round(100*(1-min))}%", color = colors[cyc])
    chart.plot(df.current, color='black', linewidth=1.0)

    c = df.current[df.current.notnull()]
    chart.plot(c.index[-1], c[c.index[-1]], marker='o', color='black', label='_nolegend_')
    chart.text(c.index[-1], c[c.index[-1]], f"-{round(100*(1-c[c.index[-1]]) )}%", color='black')

    cyclesMed.append('Current')

    # set chart display options
    chart.legend(loc='lower right', labels=cyclesMed, fontsize='xx-small')
    chart.set_xlabel('Days since Peak')
    chart.set_title("Medium Term Stock Market Cycles")
    chart.axis(xmin=0, xmax=1000)
    chart.axis(ymin=.4, ymax=1)

    # set background color
    chart.axvspan(0, 1000, facecolor='lightgreen', alpha=0.2)

    # Save fig/chart to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    return base64.b64encode(buf.getbuffer()).decode("ascii")


def longCycles(df, cycDf, colorObj):

    colors = colorObj.getColorDict()
    cyclesLong = cycDf.query('duration>1000')['title'].tolist()

    fig = Figure(figsize=(10,6))
    chart = fig.subplots()
    for cyc in cyclesLong:
        min=df[cyc].min()
        minDate = df[cyc].idxmin()
        chart.plot(minDate, min, marker='o', color=colors[cyc])
        chart.plot(df[cyc], marker='', linewidth=1.0, alpha=1, color=colors[cyc], label='_nolegend_')
        chart.text(minDate, min, f"-{round(100*(1-min))}%", color = colors[cyc])
    chart.plot(df.current, color='black', linewidth=1.0)

    c = df.current[df.current.notnull()]
    chart.plot(c.index[-1], c[c.index[-1]], marker='o', color='black', label='_nolegend_')
    chart.text(c.index[-1], c[c.index[-1]], f"-{round(100*(1-c[c.index[-1]]) )}%", color='black')

    cyclesLong.append('Current')

    # set chart display options
    chart.legend(loc='lower right', labels=cyclesLong, fontsize='xx-small')
    chart.set_xlabel('Days since Peak')
    chart.set_title("Long Term Stock Market Cycles")
    chart.axis(xmin=0, xmax=3000)

    # set background color
    chart.axvspan(0, 3000, facecolor='pink', alpha=0.2)

    # Save fig/chart to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    return base64.b64encode(buf.getbuffer()).decode("ascii")


def barAnnual(din):

    # munge data
    today_val = din.iloc[-1].Close/din.iloc[0].Close
    newDateRange = pd.date_range('1/1/1950', din.index[-1]) 
    d = (din.reindex(newDateRange, method='bfill').Close/din.Close[0]).resample("AS").asfreq().to_frame()
    nxt = d.iloc[1:].Close.tolist()
    nxt.append(today_val)
    d['nextYear'] = nxt
    d['annReturn'] = round(((d.nextYear/d.Close)-1)*100,2)
    d['year'] = pd.DatetimeIndex(d.index).year

    #plot bar chart
    x1 = d.year
    y1 = d.annReturn
    fig = matplotlib.figure.Figure(figsize=(10,6))
    chart = fig.subplots()

    chart.grid(True, linestyle='-', zorder=0, linewidth=0.1, color='#3498DB')
    chart.bar(x1, y1, color="#2874A6", zorder=3)

    # formatting for the chart
    chart.set_xlabel('Year')
    chart.set_ylabel('Annual Return (%)')
    chart.set_title("S&P 500 Annual Returns")
    
    # annotate chart, add % and 'ytd' to last data point
    lastBar = chart.bar(x1, y1, zorder=4)[-1]
    lastBar.set_color("#64DD17")
    barWidth = lastBar.get_width()
    strB = f"YTD {lastBar.get_height()}%"
    chart.annotate(strB, xy=(lastBar.get_x(), lastBar.get_height()+1), fontsize=10)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    return base64.b64encode(buf.getbuffer()).decode("ascii")


def growthRates(df):
    fig = Figure(figsize=(10,6))
    chart = fig.subplots()
    x2 = df.index
    y2 = df['10 CAGR']
    x4 = df.index
    y4 = df['20 CAGR']
    x5 = df.index
    y5 = df['30 CAGR']
    x6 = df.index
    y6 = df['1950 CAGR']

    l = ['10 years', '20 years', '30 years', 'Current Since 1950']

    chart.plot(x2, y2, color='#85C1E9', marker='', linewidth=1.0)
    chart.plot(x4, y4, color='#2E86C1', marker='', linewidth=1.0)
    chart.plot(x5, y5, color='#1B4F72', marker='', linewidth=1.0)
    chart.plot(x6, y6, color='#E67E22', marker='', linewidth=1.0)

    # formatting for the chart
    chart.set_xlabel('Date')
    chart.grid(True, linestyle='-', zorder=0, linewidth=0.1, color='#3498DB')
    chart.tick_params(labelcolor='black')
    chart.legend(loc='lower right', labels=l, fontsize='medium')
    chart.set_title("Current CAGR, trailing periods")
    chart.set_ylabel('CAGR (%)', color="#2E86C1")

    # annotate last datapoint with mean of plot
    strM10 = f"Avg {round(df['10 CAGR'].mean(), 2)}%"
    strM20 = f"Avg {round(df['20 CAGR'].mean(), 2)}%"
    strM30 = f"Avg {round(df['30 CAGR'].mean(), 2)}%"
    str1950 = f"{round(df['1950 CAGR'].mean(), 2)}%"

    chart.text(x2[-1], y2[-1], strM10)
    chart.text(x4[-1], y4[-1], strM20)
    chart.text(x5[-1], y5[-1], strM30)
    chart.text(x6[0], y6[0]+0.5, str1950)

    # add color bands and set y axis limits
    chart.axhspan(-10, 0, facecolor='pink', alpha=0.2)
    chart.axhspan(0, 5, facecolor='lightgreen', alpha=0.2)
    chart.axhspan(5, 20, facecolor='lightgreen', alpha=0.3)
    x = fig.gca()
    x.set_ylim([-10, 20])
    chart.axhline(0, color='black', linewidth=1.0)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    return base64.b64encode(buf.getbuffer()).decode("ascii")