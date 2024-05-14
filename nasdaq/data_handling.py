from .Ticker import NasdaqTicker

def get_data(dataset_input, date_type):
    finance = NasdaqTicker(dataset_input, period=date_type)
    
    return finance 