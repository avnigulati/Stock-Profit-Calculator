from flask import Flask, request, render_template
import alpha_vantage
from alpha_vantage.timeseries import TimeSeries
import datetime
import requests
import json
import time
import pytz
from pytz import reference


app = Flask(__name__)


@app.route('/')
def hello_world():

   return render_template('my-form.html')


@app.route('/', methods=['POST'])
def my_form_post():
    symbol = request.form['text']
    processed_text = symbol.upper()

    data = finance_info(symbol)
    print ("data \n", data)
    r = json.dumps(data)
    items= json.loads(r)
    # if data['current_date'] != "":
    return render_template('finance_info.html', items= items)
    # elif data['current_date']== '':
    #     return render_template('no_symbol.html', items= items)




def finance_info(symbol):

    todaysDate = str(datetime.datetime.now())
    print_Date = time.strftime("%c")
    print ("todays date", todaysDate)
    tickerSymbol = symbol.upper()

    #json format data
    final_data= {'current_date': "",
                 'symbol': "",
                 'long_name': "",
                 'change_val': ""
                 }

    ts = TimeSeries(key='OM90W7F7APJ3AOCJ')

    longCompanyName = fetch_symbol(tickerSymbol)
    print ("type ", type(longCompanyName))
    print ("long Company name", longCompanyName)
    if longCompanyName is not None:

        data,meta_data = ts.get_daily_adjusted(tickerSymbol)

        lastRefreshed = meta_data['3. Last Refreshed']
        timeZone = meta_data['5. Time Zone']
        now = datetime.datetime.now()
        localtime = reference.LocalTimezone()
        localtime.tzname(now)
        print(-time.timezone / 3600)
        dateTime = todaysDate + " " + "GMT"

        date_split = lastRefreshed.split()
        print("todaysDate :", date_split[0])

        # lastDataSet = data[todaysDate]
        #lastDataSet = data[if len(date)
        
        lastDataSet = data[date_split[0]]

        openingStockPrice = lastDataSet['1. open']

        currentStockPrice = lastDataSet['5. adjusted close']

        stock_change = float(currentStockPrice) - float(openingStockPrice)
        print_Date = now.strftime("%a, %d-%b-%Y %I:%M:%S, " + localtime.tzname(now))

        final_data['current_date']= print_Date
        print(dateTime)
        final_data['long_name']= longCompanyName
        final_data['symbol']= tickerSymbol

        print("{} ({})".format(longCompanyName, tickerSymbol))
        print ("final data \n", final_data)

        if stock_change < 0:
            percentChange = stock_change / float(openingStockPrice) * float(100)
            print("{} {} ({}%)".format(currentStockPrice, round(stock_change, 2), round(percentChange, 2)))
            vals = str(currentStockPrice) +" "+ str(round(stock_change, 2))+ " ("+ str(round(percentChange, 2)) + "%)"
            final_data["change_val"] = vals
        else:
            percentChange = stock_change / float(openingStockPrice) * float(100)
            print("{} +{} (+{}%)".format(currentStockPrice, round(stock_change, 2), round(percentChange, 2)))
            vals = str(currentStockPrice) + " +" + str(round(stock_change, 2)) + " (+" + str(round(percentChange, 2)) + "%)"
            final_data["change_val"] = vals
    else:
        final_data['long_name']= "Could not find Symbol "+ str(symbol)
           # final_data['symbol']= str(symbol)
        print('Could not find Symbol {}'.format(tickerSymbol))

    return final_data

def fetch_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)
    output = requests.get(url).json()
    #print ("result ", result)
    for symb in output['ResultSet']['Result']:
        if symb['symbol'] == symbol:
            return symb['name']



if __name__ == '__main__':
    app.run()
