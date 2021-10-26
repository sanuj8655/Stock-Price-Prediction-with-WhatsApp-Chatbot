import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense,LSTM,Dropout
import math
from sklearn.metrics import mean_squared_error

def LSTM_RNN(data):
    og_df = data
    data["Close"]=pd.to_numeric(data.Close,errors='coerce')
    data = data.dropna()
    trainData = data.iloc[:,8:9].values
    sc = MinMaxScaler(feature_range=(0,1))
    trainData = sc.fit_transform(trainData)
    X_train = []
    y_train = []

    for i in range(60, int(len(trainData))): #60 : timestep // 907 : length of the data
        X_train.append(trainData[i-60:i,0]) 
        y_train.append(trainData[i,0])

    X_train,y_train = np.array(X_train),np.array(y_train)
    X_train = np.reshape(X_train,(X_train.shape[0],X_train.shape[1],1)) #adding the batch_size axis
    model = Sequential()

    model.add(LSTM(units=20, return_sequences = True, input_shape =(X_train.shape[1],1)))
    model.add(Dropout(0.2))

    model.add(LSTM(units=20, return_sequences = False))
    model.add(Dropout(0.2))

    model.add(Dense(units =1))
    model.compile(optimizer='adam',loss="mean_squared_error")
    hist = model.fit(X_train, y_train, epochs = 5, batch_size = 32, verbose=2)


    testData = og_df
    testData["Close"]=pd.to_numeric(testData.Close,errors='coerce')
    testData = testData.dropna()
    testData = testData.iloc[:,8:9]
    y_test = testData.iloc[60:,0:].values 
    #input array for the model
    inputClosing = testData.iloc[:,0:].values 
    inputClosing.shape
    inputClosing_scaled = sc.transform(inputClosing)
    inputClosing_scaled.shape
    X_test = []
    length = len(testData)
    timestep = 60
    for i in range(timestep,length):  
        X_test.append(inputClosing_scaled[i-timestep:i,0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))

    y_pred = model.predict(X_test)
    predicted_price = sc.inverse_transform(y_pred)


    plt.figure(figsize=(9.2,4.8))
    plt.plot(y_test,label='Actual Price' )
    plt.plot(predicted_price,label='Predicted Price')
    plt.legend(loc=4)
    plt.savefig('static/LSTM.jpg')
    plt.close()

    X_forecast=np.array(X_train[-1,1:])
    X_forecast=np.append(X_forecast,y_train[-1])
    #Reshaping: Adding 3rd dimension
    X_train=np.reshape(X_train, (X_train.shape[0],X_train.shape[1],1))#.shape 0=row,1=col
    X_forecast=np.reshape(X_forecast, (1,X_forecast.shape[0],1))
    forecasted_stock_price=model.predict(X_forecast)
    forecasted_stock_price=sc.inverse_transform(forecasted_stock_price)
    lstm_pred=forecasted_stock_price[0,0]
    
    
    lstm_pred = round(lstm_pred, 2)
    error_lm = round(math.sqrt(mean_squared_error(y_test, predicted_price)),2)
    
    return lstm_pred, error_lm