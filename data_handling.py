from yahoo_finance import data_handling as ydh
def get_stock(stock, website='yahoo_finance', date_type='1D'):
    if website=='yahoo_finance':
        finance = ydh.get_data(stock, date_type)
    return finance

