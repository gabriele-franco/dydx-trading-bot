import backtrader as bt
from func_public import get_candles_historical
from func_cointegration import calculate_cointegration
from func_connection import connect_dydx
from statsmodels.tsa.stattools import coint
import numpy as np
import statsmodels.api as sm


def calculate_cointegrations(series_1, series_2, market_1, market_2):
  array_1 = [d[market_1] for d in series_1]
  array_2= [d[market_2] for d in series_2]
  coint_flag = 0
  coint_res = coint(array_1, array_2)
  coint_t = coint_res[0]
  p_value = coint_res[1]
  critical_value = coint_res[2][1]
  model = sm.OLS(array_1, array_2).fit()
  hedge_ratio = model.params[0]
  spread = array_1 - (hedge_ratio * array_2)
  print(spread)
  
  return coint_res

class StatArbitrage(bt.Strategy):
    def __init__(
        self,
        client,
        market_1,
        market_2):
        client=self.client
        market_1=self.market_1
        market_2=self.market_2
        price_1=self.price_1
        price_2=self.price_2

    def get_data(client, market_1, market_2):
        price_1= get_candles_historical(client,market_1)
        price_2= get_candles_historical(client,market_2)
        return market_1, market_2, price_1, price_2
    
    def backtesting( price_1, price_2, market_1,market_2, Z_SCORE=1.5):
        coint_res=calculate_cointegrations(price_1, price_2, market_1,market_2)
        print(coint_res)





client=connect_dydx()

cerebro = bt.Cerebro()
market_1, market_2, price_1, price_2=StatArbitrage.get_data(client, "AAVE-USD", "SNX-USD")
coint_res= StatArbitrage.backtesting( price_1, price_2,market_1, market_2)

cerebro.addstrategy(StatArbitrage)
cerebro.run()




