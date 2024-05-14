from .Ticker import Ticker

def get_data(dataset_input, date_type):
    finance = Ticker(dataset_input, period=date_type)
    
    return finance 