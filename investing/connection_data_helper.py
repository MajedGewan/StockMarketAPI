import requests
from .InvestingResult import InvestingResult
import json
import time
from bs4 import BeautifulSoup
import pandas as pd


investing_url = 'https://www.investing.com'
search_url = 'https://api.investing.com/api/search/v2/search?q='

def search_keyword(keyword):
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
    response = connect(link, headers)
    if response is None:
        error = 'error'
        return None, None
    data = response.json()
    return data, error
    
    
def get_interval_period(period):
    if period == '1d':
        i = 'P1D'
        p = 'PT5M'
    elif period == '1m':
        i = 'P1M'
        p = 'P1D'
    elif period == '1y':
        i = 'P1Y'
        p = 'P1D'
    elif period == '5y':
        i = 'P5Y'
        p = 'P1D'
    else:
        raise Exception
    return p, i

def connect(url, headers=None, trials=0):
    if trials > 5:
        return None
    try:
        response = requests.get(url, headers=headers)
    except:
        time.sleep(2 ** (trials + 1))
        response = connect(url, headers, trials + 1)
    return response


def get_data(id, period, url):
    raw_data, error = get_raw_data(id, period)
    if error is None:
        chart_data, currency, regular_market_time, timezone, previous_close, high, low = process_data(raw_data, url)
    return error, chart_data, currency, regular_market_time, timezone, previous_close, high, low


def process_data(data, url):
    currency, previous_close = scrap_additional(url)
    timezone = 'UTC'
    open_ = [d[1] for d in data['data']]
    high_ = [d[2] for d in data['data']]
    low_ = [d[3] for d in data['data']]
    close_ = [d[4] for d in data['data']]
    date = [pd.Timestamp(d[0], unit='ms', tz='utc') for d in data['data']]
    chart_data = pd.DataFrame({'Date': date, 'Close':close_, 'Open':open_, 'High':high_, 'Low':low_})
    high,low = get_high_low(chart_data, True)
    return chart_data, currency, None, timezone, previous_close, high, low



def scrap_additional(url):
    url = investing_url + url
    page = connect(url)

    soup = BeautifulSoup(page.content, "html.parser")
    currency_field = soup.find('span',{'class':'ml-1.5 font-bold'})
    if currency_field is None:
        currency_field = soup.find('span',{'class':'flex-shrink overflow-hidden text-ellipsis text-xs font-normal leading-4'})

    currency = currency_field.get_text()
    spans = soup.find('span',{'class':'key-info_dd-numeric__ZQFIs'})
    prev_close = spans.find_all('span')[1].get_text()
    prev_close = float(prev_close)
    return currency, prev_close

def get_high_low(chart_data, is_long):
    col = 'Close'
    if is_long:
        col = 'High'
    high = chart_data[col].max()
    low = chart_data[col].min()
    return high, low