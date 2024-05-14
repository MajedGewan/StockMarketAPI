from . import connection_data_helper
from finance.Ticker import Ticker
class YahooTicker(Ticker):
    def get_connection_data(self):
        return connection_data_helper.get_data(self.symbol, self.period)
        
