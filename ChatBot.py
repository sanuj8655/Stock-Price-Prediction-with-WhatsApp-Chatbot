import nsepy as nse

def get_lastprice(stock_name):
    stock_data = nse.get_quote(stock_name)
    last_traded = stock_data['tradedDate']
    current_price = stock_data['data'][0]['lastPrice']
    open_price = stock_data['data'][0]['open']
    high_price = stock_data['data'][0]['dayHigh']
    low_price = stock_data['data'][0]['dayLow']
    close_price = stock_data['data'][0]['closePrice']
    last_refreshed = stock_data['lastUpdateTime']
    return [last_traded, current_price, open_price, high_price, low_price, close_price,last_refreshed]

