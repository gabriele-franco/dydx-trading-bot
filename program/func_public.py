from fileinput import close
from func_utils import get_ISO_times
from pprint import pprint
import pandas as pd 
import numpy as np
from constants import RESOLUTION
import time 


#get relevant time periods

ISO_TIMES=get_ISO_times()
pprint(ISO_TIMES)


#get candle data
# Get Candles Historical
def get_candles_historical(client, market):

  # Define output
  close_prices = []

  # Extract historical price data for each timeframe
  for timeframe in ISO_TIMES.keys():

    # Confirm times needed
    tf_obj = ISO_TIMES[timeframe]
    from_iso = tf_obj["from_iso"]
    to_iso = tf_obj["to_iso"]

    # Protect rate limits
    time.sleep(0.2)

    # Get data
    candles = client.public.get_candles(
      market=market,
      resolution=RESOLUTION,
      from_iso=from_iso,
      to_iso=to_iso,
      limit=100
    )
    #print('candele',dir(candles.data.keys()))

    # Structure data
    for candle in candles.data["candles"]:
 
      close_prices.append({"datetime": candle["startedAt"], market: candle["close"] })

  # Construct and return DataFrame
  close_prices.reverse()
  return close_prices

def construct_market_prices(client):
    tradable_markets=[]
    markets=client.public.get_markets()

    #find tradable pairs
    for market in markets.data['markets'].keys():
 
        market_info=markets.data['markets'][market]

        if market_info['status']=="ONLINE" and market_info['type']=="PERPETUAL":
            tradable_markets.append(market)

    #set initial dataframe
    close_prices=get_candles_historical(client,tradable_markets[0] )
    pprint(close_prices)
    df=pd.DataFrame(close_prices)
    df.set_index("datetime", inplace=True)
    print(df.head())

