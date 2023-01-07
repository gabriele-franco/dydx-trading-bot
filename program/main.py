from numpy import True_
from regex import E
from func_connection import connect_dydx
from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED, PLACE_TRADES, MANAGE_EXITS
from func_private import abort_all_positions, place_market_order
from func_public import construct_market_prices
from func_cointegration import store_cointegration_results
from func_exit_pairs import manage_trade_exits
from func_entry_pairs import open_positions
from func_messaging import send_message

if __name__ == "__main__":
    send_message("Bot launch successful")

    #connect to client
    try:
        print("Connecting to client...")
        client=connect_dydx()
    except Exception as e:
        print(e)
        print("error connecting to client", e)
        send_message(f'error connecting to client {e}')
        exit(1)

if  ABORT_ALL_POSITIONS == True:
    try:
        print("Closing all position...")
        close_orders=abort_all_positions(client)
    except Exception as e:
        print("error closing all positions", e)
        send_message(f'error closing all positions {e}')
        exit(1)

#find cointegrated pairs

if FIND_COINTEGRATED:
    #construct market prices

    try:
        print("Fetch market prices, please wait 3 minutes...")
        send_message("Fetch market prices, please wait 3 minutes...")
        df_market_prices= construct_market_prices(client)
    except Exception as e:
        print(e)
        print("error constructing market prices", e)
        send_message(f'error constructing market prices {e}')
        exit(1)

    #STORE OINTEGRATED PAIRS        
    try:
        print("storing cointegrated pairs...")
        stores_result= store_cointegration_results(df_market_prices)
        if stores_result!= "saved":
            print("error saving  cointegrated pairs")
            send_message(f'error saving cointegrated pairs')
            exit(1)
    except Exception as e:
        print(e)
        print("error saving cointegrated pairs", e)
        send_message(f'error saving cointegrated pairs {e}')
        exit(1)

#run always on
while True:

    #Place trades for opening positions
    if MANAGE_EXITS==True:

        try:
            print("Managing exits...")
            send_message("Managing exits...")
            manage_trade_exits(client)
        except Exception as e:
            print(e)
            print("error managing exits positionss", e)
            send_message(f'error managing exits positionss {e}')
            exit(1)


    #Place trades for opening positions
    if PLACE_TRADES==True:

        try:
            print("finding trading opportunities...")
            send_message(f'finding trading opportunities...')
            open_positions(client)
        except Exception as e:
            print(e)
            print("error finding trading opportunities", e)
            send_message(f'error finding trading opportunities {e}')
            exit(1)


