import matplotlib.pyplot as plt

def process(stock_df):
    stock_df1 = stock_df.dropna()
    start_year = stock_df1.index[0].year
    end_year = stock_df1.index[-1].year

    plt.figure(figsize=(9.2,4.8),dpi=100)
    stock_df1['Open'].plot()
    plt.ylabel('Pices in ₹')
    plt.title(f'Opening Prices for {start_year}-{end_year}')
    plt.savefig('static/Open_price.jpg')
    plt.close()

    plt.figure(figsize=(9.2,4.8),dpi=100)
    stock_df1['Close'].plot()
    plt.title(f'Closing Prices for {start_year}-{end_year}')
    plt.ylabel('Pices in ₹')
    plt.savefig('static/Close_price.jpg')
    plt.close()

    plt.figure(figsize=(11.2,5.2),dpi=100)
    stock_df1['Volume'].plot()
    plt.title(f"Trading Volume {start_year}-{end_year}")
    plt.savefig('static/Volume.jpg')
    plt.close()


    stock_df1['Intraday Volume'] = stock_df1['Volume'] - stock_df1['Deliverable Volume']
    piechart_vars = ['Deliverable Volume','Intraday Volume']
    piechart_values = [stock_df1['Deliverable Volume'].sum(), stock_df1['Intraday Volume'].sum()]
    plt.pie(piechart_values, labels=piechart_vars, autopct="%1.2f%%")
    plt.title('Types of Volume')
    plt.savefig('static/Pie_Chart.jpg')
    plt.close()


    stock_ma = stock_df1
    stock_ma['Returns'] = (stock_ma['Close']/ stock_ma['Close'].shift(1)) - 1
    stock_ma['Cumulative Return'] = (1 + stock_ma['Returns']).cumprod()
    cum_ret = round(stock_ma['Cumulative Return'].iloc[-1], 2)

    plt.figure(figsize=(11.2,5.2),dpi=100)
    stock_ma['Cumulative Return'].plot()
    plt.title("Cumulative Return Over Time")
    plt.savefig('static/Cum_Ret.jpg')
    plt.close()

    return cum_ret









