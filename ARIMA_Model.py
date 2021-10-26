import pandas as pd
from datetime import date, timedelta

def AM(df):
    df2 = df['Close'].reset_index()
    train = df.iloc[0:int(0.8*len(df)),:]
    test = df.iloc[int(0.8*len(df)):,:]
    from statsmodels.tsa.arima_model import ARIMA
    model=ARIMA(train['Close'],order=(5,1,3))
    model=model.fit()
    df2 = test.reset_index()
    start=len(train)
    end=len(train)+len(test)-1

    # # #if the predicted values dont have date values as index, you will have to uncomment the following two commented lines to plot a graph
    index_future_dates=pd.date_range(start='2020-09-12',end='2021-02-09')
    pred=model.predict(start=start,end=end,typ='levels').rename('ARIMA predictions')
    # pred.index=index_future_dates
    df2['Predictions'] = pred.values



    import matplotlib.pyplot as plt2
    plt2.figure(figsize=(9.2,4.8))
    plt2.plot(df2['Close'],label='Actual Price' )
    plt2.plot(df2['Predictions'],label='Predicted Price')
    plt2.legend(loc=4)
    plt2.savefig('static/AM.jpg')
    plt2.close()


    from sklearn.metrics import mean_squared_error
    from math import sqrt
    error_ar=round(sqrt(mean_squared_error(pred,test['Close'])),2)
    model2=ARIMA(df['Close'],order=(5,1,3))
    model2=model2.fit()
    index_future_dates=pd.date_range(start=date.today(),end= date.today() + timedelta(days=1))
    #print(index_future_dates)
    pred=model2.predict(start=len(df),end=len(df)+1,typ='levels').rename('ARIMA Predictions')
    #print(comp_pred)
    pred.index=index_future_dates
    ar_pred = round(pred.tail(1).item(),2)
    return ar_pred, error_ar

