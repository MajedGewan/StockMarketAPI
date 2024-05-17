import requests
import time
from datetime import datetime, timedelta
import pandas as pd

def get_raw_data(symbol, from_date=None, to_date=None):
        link = f'https://api.nasdaq.com/api/quote/{symbol}/chart?assetclass=stocks'
        if from_date is not None and to_date is not None:
             additional = f'&fromdate={from_date}&todate={to_date}'
             link = link + additional
        headers = {
                        'Accept':'application/json, text/plain, */*',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                        'From': 'youremail@domain.example'  # This is another valid field
                    }
        raw_data, error = None, None
        for attempt in range(3):  # Retry up to 5 times
            response = requests.get(link, headers=headers)
            if response.status_code == 429:
                time.sleep(2 ** attempt)
                continue
            elif response.status_code == 200:
                if response.json()['status']['rCode'] !=200:
                    break
                raw_data = response.json()
                print(raw_data)
                return raw_data, None 
            else:
                error = response.status_code
                return None, error
        if raw_data is None:
            error = "429 unknow request code"
            return None, error
        return raw_data, error


def get_data(symbol, period):
    chart_data, currency, regular_market_time, timezone, previous_close, high, low = None, None, None, None, None, None, None
    from_date, to_date = get_from_to_date(period)
    raw_data, error = get_raw_data(symbol, from_date, to_date)
    if error is None:
        chart_data, currency, regular_market_time, timezone, previous_close, high, low = process_data(raw_data,period)
    return error, chart_data, currency, regular_market_time, timezone, previous_close, high, low

def get_from_to_date(period):
    if period == '1D':
        from_date, to_date = None, None
    else:
        to_date = datetime.today()
        if period == '1M':
            from_date = datetime.today()- timedelta(days=30)
        elif period == '1Y':
            from_date = datetime.today()- timedelta(days=365)
        elif period == '5Y':
            from_date = datetime.today()- timedelta(days=365*5)
        else:
            raise Exception
        to_date = to_date.date()
        from_date = from_date.date()
    return from_date, to_date

def process_data(data, period):
    if period =='1D':
        return process_daily_data(data)
    else:
        return process_long_data(data)


def process_long_data(data):

    previous_close = data['data']['previousClose']
    timezone = 'ET'
    currency = 'USD'
    high_ = [i['z']['high'] for i in data['data']['chart']]
    low_ = [i['z']['low'] for i in data['data']['chart']]
    open_ = [i['z']['open'] for i in data['data']['chart']]
    close_ = [i['z']['close'] for i in data['data']['chart']]
    date = [datetime.strptime(i['z']['dateTime'], '%m/%d/%Y') for i in data['data']['chart']]
    chart_data = pd.DataFrame({'Date': date, 'Close':close_, 'Open':open_, 'High':high_, 'Low':low_})
    high,low = get_high_low(chart_data, True)
    return chart_data, currency, None, timezone, previous_close, high, low

def process_daily_data(data):
    day = data['data']['timeAsOf'][:12].strip()
    day = datetime.strptime(day, '%b %d, %Y')
    previous_close = data['data']['previousClose']
    timezone = 'ET'
    currency = 'USD'
    times = get_date_time(data, day)
    values = [i['z']['value'] for i in data['data']['chart']]
    chart_data = pd.DataFrame({'Date': times, 'Close':values})
    high,low = get_high_low(chart_data, False)
    return chart_data, currency, None, timezone, previous_close, high, low

    
def get_date_time(data,day):
    times = []
    date_format = '%I:%M %p'
    for i in data['data']['chart']:
        time = i['z']['dateTime'].rsplit(' ', 1)[0]
        time = datetime.strptime(time, date_format)
        day_time = datetime.combine(day.date(), time.time())
        times.append(day_time)
    return times
        
def get_high_low(chart_data, is_long):
    col = 'Close'
    if is_long:
        col = 'High'
    high = chart_data[col].max()
    low = chart_data[col].min()
    return high, low

