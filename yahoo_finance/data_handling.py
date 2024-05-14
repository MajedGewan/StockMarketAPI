from .Ticker import YahooTicker
def get_data(dataset_input, date_type):
    if date_type == '1D':
        period = '1d'
    elif date_type == '1M':
        period = '1mo'
    elif date_type == '1Y':
        period = '1y'
    elif date_type == '5Y':
        period = '5y'
    else:
        raise Exception
    finance = YahooTicker(dataset_input, period=period)
    
    return finance 