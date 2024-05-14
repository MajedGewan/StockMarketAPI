from . import connection_data_helper
from .Ticker import Ticker
def search_keyword(keyword):
    return connection_data_helper.search_keyword(keyword)
    
def get_data(dataset_input, url, date_type='1d'):
    finance = Ticker(dataset_input, period=date_type, url=url)
    return finance.to_json()
