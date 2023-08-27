from fyers_apiv3 import fyersModel
from fyers_apiv3.FyersWebsocket import order_ws
import pandas as pd
import numpy as np
import datetime as dt
import time
client_id = "XXXXXXXXXX-100"
with open("access.txt",'r') as r:
    access_token=r.read()

fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path="api_logs")

symbols =["NSE:NIFTY50-INDEX","NSE:NIFTYBANK-INDEX"]

def HisData_bydate (symbol, tf,sd,ed):
    data = {"symbol":symbol,"resolution":str(tf),
    "date_format":"1",
    "range_from":str(sd),
    "range_to":str(ed),
    "cont_flag":"1"}
    response = fyers.history(data=data)                                                             #fetching the data from historical API
    raw_df= pd.DataFrame(response['candles'])                                                       #creating raw data frame
    raw_df.columns=['timestamp','Open','High','Low','Close','tradingVolume']     # appending the collumns of data frame
    raw_df['timestamp'] = pd.to_datetime(raw_df['timestamp'],unit='s')                                # converting date time from string to date time format
    raw_df.timestamp = (raw_df.timestamp.dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata'))         #converting timeframe to IST
    raw_df['timestamp'] = raw_df['timestamp'].dt.tz_localize(None)                                    # localizing
    raw_df = raw_df.set_index('timestamp')
    return raw_df

for symbol in symbols:
    ab = None
    sd = dt.date(2017,5,1)
    endDate = dt.datetime.now().date()
    n = abs((sd-endDate).days) 
    df = pd.DataFrame()

    while ab is None:
        sd = endDate - dt.timedelta(days=n)
        ed = (sd + dt.timedelta(days=99 if n > 100 else n))
        tf="1"
    
        n = n - 100 if n > 100 else 0
        dx = HisData_bydate(symbol, tf, sd, ed)
        df = df._append(dx)
        n = n - 100 if n > 100 else 0
        print(n)
        if n == 0:
            ab = 'Done'
        
    output_filename = symbol+'.csv'
    output_filename_2 = output_filename[4:-10]
    print(len(output_filename))
    print(output_filename_2)
    df.to_csv(output_filename_2)
    print(df)