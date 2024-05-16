from . import connection_data_helper
from finance.Ticker import Ticker
class YahooTicker(Ticker):
    def get_connection_data(self):
        returned_value = connection_data_helper.get_data(self.symbol, self.period)
        return returned_value
        
    def get_website(self):
        return 'Yahoo Finance'