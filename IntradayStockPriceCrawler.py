# This is the web crawler to get intraday stock price from Google Finance

import requests
import pandas as pd
from io import StringIO
from datetime import datetime

def StockPriceCrawler(ticker, interval = 60, periods = 5, unit = 'd'):
    '''

    :param ticker: The symbol of the stock on Google Finance
    :param interval: The interval in seconds; default is 1 min
    :param periods: the number of the periods
    :param unit:    d for day (default)
                    M for month
                    Y for year
    :return: stock price dataframe
    '''

    url = 'https://www.google.com/finance/getprices?q=NIFTY&x=NSE&i=60&p=6M&f=d,c,o,h,l&df=cpct&auto=1'
    #url = 'http://www.google.com/finance/getprices?q={0}&x=NSE&i={1}&p={2}{3}&f=d,o,h,l,c,v&df=cpct&auto=1'.format(
    #    str(ticker).upper(), str(interval), str(periods), str(unit))
    flag = 0
    timeStamp = 0

    try:
        r = requests.get(url)

        df = pd.read_csv(StringIO(r.text[143:]), sep=',', header=None)
        df.columns = ['Seq', 'Open', 'High', 'Low', 'Close', 'Volume']

        for i in range(len(df)):
            if df.Seq[i].startswith('a'):
                timeStamp = df.Seq[i][1:]
                flag = 0
                df.loc[i, 'Date'] = datetime.fromtimestamp(timestamp=int(timeStamp))
            else:
                df.loc[i, 'Date'] = datetime.fromtimestamp(timestamp=int(timeStamp) + flag * interval)

            flag += 1

        stockData = df.set_index('Date')[['Open', 'High', 'Low', 'Close', 'Volume']]

        return stockData

    except ConnectionError:
        print('Connection error, try again!')


if __name__ == '__main__':
    df = StockPriceCrawler(ticker='goog', interval=60, periods=2, unit='Y')
    df.to_csv('goog_1min_5y.csv')