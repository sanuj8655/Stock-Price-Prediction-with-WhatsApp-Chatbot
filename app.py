from flask import Flask, render_template, request
import pandas as pd
import nsepy as nse
from datetime import date
import sys
from twilio.rest import Client
import os
from analysis import process
from ARIMA_Model import AM
from LSTM_Model import LSTM_RNN
from Linear import LM
from ChatBot import get_lastprice

app = Flask(__name__)

ACCOUNT_ID = ''
TWILIO_TOKEN = ''
TWILIO_NUMBER = 'whatsapp:+14155238886'

client = Client(ACCOUNT_ID, TWILIO_TOKEN)

def process_msg(msg):
    response = ""
    if msg == "Hi":
        response = 'Hello! Welcome to Stock Market BOT Developed by Anuj!\n'
        response += 'Enter SYM:<stock symbol> to get started'
    elif 'SYM:' in msg:
        data = msg.split(':')
        stock_sym = data[1]
        stock_data = get_lastprice(str(stock_sym))
        # stock_price = stock_data[1]
        last_price = stock_data[1]
        last_price_str = str(last_price)
        response = f"The Stock Price of {stock_sym} is ₹{last_price_str}"
    else:
        response = "Type \"Hi\" to get started"
    return response

def send_msg(msg, recipient):
    client.messages.create(
        from_=TWILIO_NUMBER,
        body=msg,
        to=recipient)

@app.route("/webhook", methods=["POST"])
def webhook():
    f = request.form
    msg = f['Body']
    sender = f['From']
    response = process_msg(msg)
    send_msg(response, sender)
    return 'OK', 200

@app.after_request
def add_header(response):
    response.headers['Pragma'] = 'no-cache'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = '0'
    return response


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/error')
def error():
    return render_template('404.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
  if request.method == 'POST':
        try:
          print('######## Connected ########', file=sys.stdout)
          sys.stdout.flush()
          stock_name = request.form.get("stockname")
          stock_data = nse.get_quote(stock_name)
          last_traded = stock_data['tradedDate']
          current_price = stock_data['data'][0]['lastPrice']
          open_price = stock_data['data'][0]['open']
          high_price = stock_data['data'][0]['dayHigh']
          low_price = stock_data['data'][0]['dayLow']
          close_price = stock_data['data'][0]['closePrice']
          last_refreshed = stock_data['lastUpdateTime']
        except:
          return render_template('404.html')
        else:
            ## Fetch Historical Data  ###
            stock_name = request.form.get("stockname")
            stock_df = nse.get_history(symbol= stock_name, start=date(2018,1,1), end=date.today())
            print('######## Getting Historical Data ########', file=sys.stdout)
            sys.stdout.flush()
            stock_df.to_csv(''+stock_name+'.csv')
            print('######## Data Written onto CSV File ########', file=sys.stdout)
            sys.stdout.flush()
            cum_returns = process(stock_df)
            print('######## Primary Analysis Completed ########', file=sys.stdout)
            sys.stdout.flush()

            lr_pred, lr_err = LM(stock_df)
            print('######## Linear Model Prediction Completed ########', file=sys.stdout)
            sys.stdout.flush()

            ar_pred, ar_err = AM(stock_df)
            print('######## ARIMA Model Prediction Completed ########', file=sys.stdout)
            sys.stdout.flush()

            lstm_pred, lstm_err = LSTM_RNN(stock_df)
            print('######## LSTM Model Prediction Completed ########', file=sys.stdout)
            sys.stdout.flush()

            return render_template("results.html",
            stock_name=stock_name.upper(),
            last_traded=last_traded, current_price=current_price, open_price=open_price,
            high_price=high_price, low_price=low_price, close_price=close_price, last_refreshed=last_refreshed, cum_returns=cum_returns,
            lr_pred=lr_pred, lr_err=lr_err, ar_pred=ar_pred, ar_err=ar_err, 
            lstm_pred=lstm_pred, lstm_err=lstm_err)
            
    


if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)



