from datetime import datetime
import MetaTrader5 as mt5
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import dotenv
dotenv.load_dotenv(".env", override=True)
import os

# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ", mt5.__author__)
print("MetaTrader5 package version: ", mt5.__version__)

# import the 'pandas' module for displaying data obtained in the tabular form
import pandas as pd
import time

pd.set_option('display.max_columns', 500)  # number of columns to be displayed
pd.set_option('display.width', 1500)  # max table width to display

Login = int(os.getenv("Login"))
Server = os.getenv("Server")
Password = os.getenv("Password")

# establish MetaTrader 5 connection to a specified trading account
if not mt5.initialize(login=Login, server=Server, password=Password):
    print("initialize() failed, error code =", mt5.last_error())
    quit()

def fetch_data(product_id, granularity, count=100):
    rates = mt5.copy_rates_from_pos(product_id, granularity, 0, count)
    # create DataFrame out of the obtained data
    df = pd.DataFrame(rates)
    # convert time in seconds into the datetime format
    # df['time'] = pd.to_datetime(df['time'], unit='s')
    # df.set_index('time', inplace=True)
    # df.sort_index(ascending=True, inplace=True)

    return df

def save_data(product_id, granularity, count=100):
    df = fetch_data(product_id, granularity, count)
    df = df[['open', 'high', 'low', 'close', 'real_volume']]
    df = df.rename(columns={'real_volume': 'volume'})

    df.to_csv('data/data.csv', index=False)
    return df
df = save_data("EURUSD", mt5.TIMEFRAME_M5, 92160)
print(df)