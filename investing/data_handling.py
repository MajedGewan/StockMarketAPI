from . import connection_data_helper
from .Ticker import InvestingTicker
def search_keyword(keyword):
    return connection_data_helper.search_keyword(keyword)
    
def get_data(id, url, date_type='1D'):
    finance = InvestingTicker(id, None, date_type, url)
    return finance
    