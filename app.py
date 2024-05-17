from flask import Flask, request, Response
from investing import data_handling as inv_data_handling
from yahoo_finance import data_handling as yah_data_handling
from nasdaq import data_handling as nas_data_handling
app = Flask(__name__)
@app.route('/search/')
def index():
    keyword = request.args.get('q')
    return inv_data_handling.search_keyword(keyword)

@app.route('/getdata/<int:id>')
def getdata(id):
    print('hi')
    website = None
    symbol = None
    content = request.json
    if not 'url' in content:
        return Response(
        "url is not found",
        status=400, 
    )
    if 'website' in content:
        website = content['website']
        if not 'symbol' in content:
            return Response(
            "When choosing another website, symbol should be added",
            status=400,
            )
    if 'symbol' in content:
        symbol = content['symbol']
         
    date_type = content['date_type']
    
    url = content['url']
    if website and website != 'Investing':
        if website == 'Yahoo Finance':
            if symbol is None:
                return Response(
                    "symbol not found",
                    status=400, 
                )
            finance =  yah_data_handling.get_data(symbol, date_type)
            if finance.error is not None:
                return get_investing_data(id, url, date_type)
            return finance.to_json()
        elif website == 'Nasdaq':
            if symbol is None:
                return Response(
                    "symbol not found",
                    status=400, 
                )
            finance =  nas_data_handling.get_data(symbol, date_type)
            if finance.error is not None:
                return get_investing_data(id, url, date_type)
            return finance.to_json()
        else:
            return Response(
                    "Website can be only; Investing, Yahoo Finance or Nasdaq",
                    status=400, 
                )
    return get_investing_data(id, url, date_type)

def get_investing_data(id, url, date_type):
    ticker = inv_data_handling.get_data(id, url, date_type)
    if ticker.error is not None:
        if ticker.error == 403:
            return Response(
            "Connection Error: Try again or contact with API developer",
            status=500
        )    
        return Response(
            "Try again or check contact with API developer",
            status=ticker.error
        )
    return ticker.to_json()

