import requests
from .InvestingResult import InvestingResult
import json
import time
from bs4 import BeautifulSoup
import pandas as pd


investing_url = 'https://www.investing.com'
search_url = 'https://api.investing.com/api/search/v2/search?q='

def search_keyword(keyword):
    returned_json = []
    url = search_url + keyword
    headers = {
    'Accept':'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Access-Control-Allow-Origin': 'https://www.investing.com'  # This is another valid field
    }
    returned = []
    response = connect(url, headers)
    if response is None:
        return returned
    
    data = response.json()['quotes']
    for stock in data:
        investing_result = InvestingResult(stock['id'], stock['url'], stock['description'], stock['symbol'], stock['exchange'], stock['flag'], stock['type'])
        returned.append(investing_result)
        returned_json = json.dumps([stock.__dict__ for stock in returned])
    return returned_json

def get_raw_data(id, period):
    
    i, p = get_interval_period(period)
    data, error = None, None
    headers = {
    'Accept':'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Access-Control-Allow-Credentials': 'true',  # This is another valid field
    'Access-Control-Allow-Origin':'https://www.investing.com'
    }
    link = f'https://api.investing.com/api/financialdata/{id}/historical/chart/?interval={i}&period={p}&pointscount=160'
    print(link)
    response = connect(link, headers)
    print('after print')
    if response is None:
        error = 'error'
        return data, error
    if response.status_code != 200:
        return None, response.status_code
    data = response.json()
    return data, error
    
    
def get_interval_period(period):
    if period == '1D':
        i = 'P1D'
        p = 'PT5M'
    elif period == '1M':
        i = 'P1M'
        p = 'P1D'
    elif period == '1Y':
        i = 'P1Y'
        p = 'P1D'
    elif period == '5Y':
        i = 'P5Y'
        p = 'P1D'
    else:
        raise Exception('date type is Invalid')
    return p, i

def connect(url, headers=None, trials=0, response_error=None):
    response = None
    if trials > 3:
        return response_error
    try:
        print('before response inside')
        response = requests.get(url, headers=headers)
        print('after response inside works well')

        if response.status_code != 200:
            print('after response inside not work well 200')
            print(f'response code{response.status_code}')
            print(f'response reason{response.reason}')

            time.sleep(2 ** (trials + 1))
            response = connect(url, headers, trials + 1, response)
    except:
        print('after response inside not work well')

        time.sleep(2 ** (trials + 1))
        response = connect(url, headers, trials + 1, response)
    return response


def get_data(id, period, url):
    chart_data, currency, regular_market_time, timezone, previous_close, high, low = None, None, None, None, None, None, None
    raw_data, error = get_raw_data(id, period)
    if error is None:
        chart_data, currency, regular_market_time, timezone, previous_close, high, low = process_data(raw_data, url)
    return error, chart_data, currency, regular_market_time, timezone, previous_close, high, low


def process_data(data, url):
    currency, previous_close = scrap_additional(url, float(data['data'][-1][4]))
    timezone = 'UTC'
    open_ = [d[1] for d in data['data']]
    high_ = [d[2] for d in data['data']]
    low_ = [d[3] for d in data['data']]
    close_ = [d[4] for d in data['data']]
    date = [pd.Timestamp(d[0], unit='ms', tz='utc') for d in data['data']]
    chart_data = pd.DataFrame({'Date': date, 'Close':close_, 'Open':open_, 'High':high_, 'Low':low_})
    high,low = get_high_low(chart_data, True)
    return chart_data, currency, None, timezone, previous_close, high, low



def scrap_additional(url, price):
    is_crypto = url.split('/')[1] == 'crypto'
    currency, prev_close = None, None
    url = investing_url + url
    headers = {
    'Accept':'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Access-Control-Allow-Credentials': 'true',  # This is another valid field
    'Access-Control-Allow-Origin':'https://www.investing.com'
    }
    page = connect(url,headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")
    currency = get_currency(soup)
    
    prev_close = get_prev_close(soup, price,  is_crypto)
    return currency, prev_close

def get_high_low(chart_data, is_long):
    col = 'Close'
    if is_long:
        col = 'High'
    high = chart_data[col].max()
    low = chart_data[col].min()
    return high, low

def get_currency(soup):
    currency_field = soup.find('span',{'class':'ml-1.5 font-bold'})
    if currency_field is None:
        currency_field = soup.find('span',{'class':'flex-shrink overflow-hidden text-ellipsis text-xs font-normal leading-4'})

    currency = currency_field.get_text()
    return currency

def get_prev_close(soup, price, is_crypto):
    if is_crypto:
        span=soup.find('span',{'data-test':'instrument-price-change'})
        prev_close = price - float(span.get_text())
    else:
        spans = soup.find('span',{'class':'key-info_dd-numeric__ZQFIs'})
        prev_close = spans.find_all('span')[1].get_text()
        prev_close = float(prev_close.replace(',',''))
    return prev_close
