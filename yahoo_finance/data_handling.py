from .Ticker import Ticker
def get_data(dataset_input, date_type):
    if date_type == '1D':
        interval, period = '1m', '1d'
    elif date_type == '1M':
        interval, period = '1d', '1mo'
    elif date_type == '1Y':
        interval, period = '1d', '1y'
    elif date_type == '5Y':
        interval, period = '1d', '5y'
    else:
        raise Exception
    finance = Ticker(dataset_input, interval=interval, period=period)
    
    return finance 