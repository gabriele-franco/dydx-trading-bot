
import pandas as pd
from func_cointegration import calculate_cointegration, calculate_zscore
import matplotlib.pyplot as plt
from func_public import get_candles_historical
from func_connection import connect_dydx
import backtrader as bt


def plot_trends(market_1, market_2, price_data):
    client=connect_dydx()
    prices_1=get_candles_historical(client, market_1)
    prices_2=get_candles_historical(client, market_2)

    #get z score
    coint_flag, hedge_ratio, half_life=calculate_cointegration(market_1, market_2)
    spread = prices_1 - (hedge_ratio * prices_2)
    print(spread)

market_1="AAVE-USD"
market_2="SNX-USD"

price_data= pd.read_csv("/Users/gabriele/Documents/Cassandra_data_science/dydx_course/program/cointegrated_pairs.csv")
if len(price_data)> 0:
    plot_trends(market_1, market_2, price_data)




