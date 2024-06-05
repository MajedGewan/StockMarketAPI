import json
import descriptive
class Ticker:
    
    def __init__(self, symbol, period ) -> None:
        self.symbol = symbol
        self.period = period
        self.error = None
        self.raw_data = None
        self.website = self.get_website()
        self.get_data()

    def get_data(self):
        error, chart_data, currency, regular_market_time, timezone, previous_close, high, low =  self.get_connection_data()
        self.error = error
        self.data = chart_data
        self.currency = currency
        self.regular_market_time = regular_market_time
        self.timezone = timezone
        self.previous_close = previous_close
        self.high = high
        self.low = low
        self.description = descriptive.get_descriptive(self)

    def get_connection_data(self):
        pass

    def get_website(self):
        pass
        

        
    def __str__(self) -> str:
        return f'Error: {self.error}\nSymbol: {self.symbol}\nData: {self.data} \nCurrency: {self.currency}\nRegularMarketTime: {self.regular_market_time}\nTimezone: {self.timezone}\nPreviousClose: {self.previous_close}\nhigh: {self.high}\nlow: {self.low}\n'

    def to_json(self):
        
        data = json.loads(self.data.to_json())
        returned_json = {'Data':data, 'meta':{'Period': self.period,
                                              'Symbol':self.symbol,
                                            'Currency': self.currency,
                                            'RegularMarketTime': self.regular_market_time,
                                            'Timezone': self.timezone,
                                            'PreviousClose': self.previous_close,
                                            'High': self.high,
                                            'Low': self.low,
                                            'Website':self.website,
                                            'Description': self.description}}
        return json.dumps(returned_json)
    