from flask import Flask, request, Response
from investing import data_handling
app = Flask(__name__)
@app.route('/search/<key>')
def index(key):
    return data_handling.search_keyword(key)
app.run()

@app.route('/getdata/<int:id>')
def getdata(id):
    website = None
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
    symbol = content['symbol']
         
    content = request.json
    date_type = content['date_type']
    
    url = content['url']
    if website and website != 'Investing':
        if website == 'Yahoo Finance':
            return 'Yahoo Finanace'
        elif website == 'Nasdaq':
            return "Nasdaq"
        else:
            return data_handling.get_data(id, url, date_type)
    return data_handling.get_data(id, url, date_type)
app.run()

