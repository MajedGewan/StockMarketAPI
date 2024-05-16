from . import connection_data_helper
from finance.Ticker import Ticker
class InvestingTicker(Ticker):
    def __init__(self, id, symbol, period, url ) -> None:
        self.url = url
        self.id = id
        super().__init__(symbol, period)

    def get_connection_data(self):
        return connection_data_helper.get_data(self.id, self.period, self.url)

    def get_website(self):
        return 'Investing'