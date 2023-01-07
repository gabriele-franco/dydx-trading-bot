from regex import E
from func_connection import connect_dydx
from constants import ABORT_ALL_POSITIONS
from func_private import abort_all_positions, place_market_order
from constants import FIND_COINTEGRATED
from func_public import construct_market_prices

if __name__ == "__main__":

    #connect to client
    try:
        print("Connecting to client...")
        client=connect_dydx()
    except Exception as e:
        print(e)
        print("error connecting to client", e)
        exit(1)

if  ABORT_ALL_POSITIONS == True:
    try:
        print("Closing all position...")
        close_orders=abort_all_positions(client)
    except Exception as e:
        print("error closing all positions", e)
        exit(1)

#find cointegrated pairs

if FIND_COINTEGRATED:
    #construct market prices

    try:
        print("Fetch market prices, please wait 3 minutes...")
        df_market_prices= construct_market_prices(client)
    except Exception as e:
        print(e)
        print("error constructing market prices", e)
        exit(1)

