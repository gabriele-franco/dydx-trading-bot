from func_public import get_candles_historical
from pprint import pprint
from func_connection import connect_dydx

client=connect_dydx()

t=get_candles_historical(client, "BTC-USD")
pprint(t)