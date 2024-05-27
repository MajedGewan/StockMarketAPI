def get_descriptive(ticker):
    description = ticker.website
    last = {
        '1D':'day',
        '1M':'month',
        '1Y':'year',
        '5Y':'five years',
    }

    from_last = {
        '1D':'yesterday',
        '1M':'last month',
        '1Y':'last year',
        '5Y':'five years ago',
    }
    price = ticker.data['Close'].iloc[-1]
    big, sign = get_big(ticker, price)
    stable = get_stable(ticker)
    description = f'This dashboard shows the stock data of the last {last[ticker.period]}. The graph shows the stock changes of {ticker.symbol} stock, you can switch between OHLC and Line graph. The price now is {price}. The price is showing a {big} {sign} from {from_last[ticker.period]}. As shown in the graph, the price in this period is {stable}'
    return description
def get_big(ticker, price):
    difference = price - ticker.previous_close
    difference_portion = difference/ticker.previous_close
    abs_difference = abs(difference_portion)
    big, sign = '',''

    if ticker.period == '1D':
        if abs_difference<=0.02:
            big = 'slight'
        elif abs_difference > 0.02 and abs_difference <= 0.05:
            big = ''
        elif abs_difference > 0.05 and abs_difference <=0.1:
            big = 'big'
        else:
            big = 'massive'
    else:
        if abs_difference<=0.03:
            big = 'slight'
        elif abs_difference > 0.03 and abs_difference <= 0.1:
            big = ''
        elif abs_difference > 0.1 and abs_difference <=0.3:
            big = 'big'
        else:
            big = 'massive'
    if difference_portion >=0:
        sign = 'raise'
    else:
        sign = 'drop'

    return big, sign

def get_stable(ticker):
    changes = []
    data = ticker.data
    data = data[::10]
    highest = data['Close'].max()
    lowest = data['Close'].min()
    low, high = data['Close'][0], data['Close'][0]
    prev_high, prev_low = data['Close'][0], data['Close'][0]
    index = 0
    for i in data['Close']:
        if i < low:
            low = i
        if i > high:
            high = i
        if (high - prev_low) / (highest - lowest) > 0.2 and i != high:
            changes.append(1)
            
            low, high, prev_high, prev_low = i,i,i,i
        if (prev_high - low) / (highest - lowest) > 0.2 and i != low:
            changes.append(-1)
            low, high, prev_high, prev_low = i,i,i,i
        index +=1
    
    if not changes:
        stable = 'stable'
    else:
        changes = edit_changes(changes)
        if all(x==changes[0] for x in changes):
            if changes[0] == 1:
                stable = 'continuously increasing'
            else:
                stable = 'continuously Decreesing'
        else:
            if len(changes) <=3:
                stable = 'showing ups and downs'
            else:
                stable = 'continuously showing ups and downs'
            
    return stable


def edit_changes(changes):
    returned_changes = []
    prev = changes[0]
    returned_changes.append(prev)
    for i in changes[1:]:
        if i != prev:
            prev = i
            returned_changes.append(prev)
    return returned_changes