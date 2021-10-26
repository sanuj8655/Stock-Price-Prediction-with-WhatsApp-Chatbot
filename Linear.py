import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import math
from sklearn.metrics import mean_squared_error


def LM(df):
    #No of days to be forcasted 
    forecast_out = int(7)
    #Price after n days
    df['Close after n days'] = df['Close'].shift(-forecast_out)
    #New df with only relevant data
    df_new=df[['Close','Close after n days']]
    #Structure data for train, test & forecast
    #lables of known data, discard last 7 rows
    y =np.array(df_new.iloc[:-forecast_out,-1]) ##Close Col
    y=np.reshape(y, (-1,1))
    #all cols of known data except lables, discard last 7 rows
    X=np.array(df_new.iloc[:-forecast_out,0:-1]) ##Close after n days col
    #Unknown, X to be forecasted
    X_to_be_forecasted=np.array(df_new.iloc[-forecast_out:,0:-1])
    #Traning, testing to plot graphs, check accuracy
    X_train=X[0:int(0.8*len(df)),:]
    X_test=X[int(0.8*len(df)):,:]
    y_train=y[0:int(0.8*len(df)),:]
    y_test=y[int(0.8*len(df)):,:]
    # #Training
    model = LinearRegression(n_jobs=-1) #use all cpu cores
    model.fit(X_train, y_train)
    #Testing
    y_test_pred=model.predict(X_test)
    y_test_pred=y_test_pred
    import matplotlib.pyplot as plt2
    plt2.figure(figsize=(9.2,4.8))
    plt2.plot(y_test,label='Actual Price' )
    plt2.plot(y_test_pred,label='Predicted Price')
    plt2.legend(loc=4)
    plt2.savefig('static/LR.jpg')
    plt2.close()
    error_lr = round(math.sqrt(mean_squared_error(y_test, y_test_pred)),2)     
    #Forecasting
    forecast_set = model.predict(X_to_be_forecasted)
    mean=forecast_set.mean()
    lr_pred=round(forecast_set[0,0],2)
    return lr_pred, error_lr
   

    
    
    
    
    
    
    






