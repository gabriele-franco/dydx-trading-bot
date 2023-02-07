from constants import ZSCORE_THRESH, USD_PER_TRADE, USD_MIN_COLLATERAL,TOKEN_FACTOR_10,VERSO_CONTRARIO
from func_utils import format_number
import time
from datetime import datetime
from func_public import get_candles_recent
from func_cointegration import calculate_zscore
from func_private import is_open_positions
from func_bot_agent import BotAgent
import pandas as pd
import json
from func_messaging import send_message
from pprint import pprint


# Open positions
def open_positions(client):

  """
    Manage finding triggers for trade entry
    Store trades for managing later on on exit function
  """

  # Load cointegrated pairs
  df = pd.read_csv("cointegrated_pairs.csv")

  # Get markets from referencing of min order size, tick size etc
  markets = client.public.get_markets().data

  # Initialize container for BotAgent results
  bot_agents = []

  storico = []

  # Opening JSON file
  try:
    open_positions_file = open("bot_agents.json")
    open_positions_dict = json.load(open_positions_file)
    for p in open_positions_dict:
      bot_agents.append(p)
  except:
    bot_agents = []

#################################################
  try:
    storico_file = open("storico.json")
    storico_dict = json.load(storico_file)
    for p in storico_dict:
      storico.append(p)
  except:
    storico = []  
  
  # Find ZScore triggers
  for index, row in df.iterrows():

    # Extract variables
    base_market = row["base_market"]
    quote_market = row["quote_market"]
    hedge_ratio = row["hedge_ratio"]
    half_life = row["half_life"]

    # Get prices
    series_1 = get_candles_recent(client, base_market)
    series_2 = get_candles_recent(client, quote_market)

    # Get ZScore
    if len(series_1) > 0 and len(series_1) == len(series_2):
      spread = series_1 - (hedge_ratio * series_2)
      ###########################################
       #PRENDO DAL FOGLIO EXCEL MA POTREBBERO NON ESSERE PIU' COINTEGRATE OPPURE 
       #PER ESEMPIO p>0,005
       #oppure rifaccio ripartire tutto ogni ora
      z_score = calculate_zscore(spread).values.tolist()[-1]

      # Establish if potential trade
      if abs(z_score) >= ZSCORE_THRESH:

        # Ensure like-for-like not already open (diversify trading)

        is_base_open = is_open_positions(client, base_market)
        is_quote_open = is_open_positions(client, quote_market)

        # Place trade

        if not is_base_open and not is_quote_open:

          # Determine side ORIGINAL SHAUN
          base_side = "BUY" if z_score < 0 else "SELL"
          quote_side = "BUY" if z_score > 0 else "SELL"

          if VERSO_CONTRARIO :
            base_side = "SELL" if z_score < 0 else "BUY"
            quote_side = "SELL" if z_score > 0 else "BUY"

          # Get acceptable price in string format with correct number of decimals
          base_price = series_1[-1]
          quote_price = series_2[-1]


          accept_base_price = float(base_price) * 1.01 if z_score < 0 else float(base_price) * 0.99
          accept_quote_price = float(quote_price) * 1.01 if z_score > 0 else float(quote_price) * 0.99
          failsafe_base_price = float(base_price) * 0.05 if z_score < 0 else float(base_price) * 1.7

          if VERSO_CONTRARIO :
            accept_base_price = float(base_price) * 1.01 if z_score > 0 else float(base_price) * 0.99
            accept_quote_price = float(quote_price) * 1.01 if z_score < 0 else float(quote_price) * 0.99
            failsafe_base_price = float(base_price) * 0.05 if z_score > 0 else float(base_price) * 1.7


          base_tick_size = markets["markets"][base_market]["tickSize"]
          quote_tick_size = markets["markets"][quote_market]["tickSize"]

          # Format prices
          accept_base_price = format_number(accept_base_price, base_tick_size)
          accept_quote_price = format_number(accept_quote_price, quote_tick_size)
          accept_failsafe_base_price = format_number(failsafe_base_price, base_tick_size)
  
          # Get size
          base_quantity = 1 / base_price * USD_PER_TRADE
          quote_quantity = 1 / quote_price * USD_PER_TRADE
          for particolari in TOKEN_FACTOR_10 :
            if base_market== particolari :
              base_quantity= float(int(base_quantity/10)*10) 
            if quote_market== particolari :
              quote_quantity= float(int(quote_quantity/10)*10)   
          
          base_step_size = markets["markets"][base_market]["stepSize"]
          quote_step_size = markets["markets"][quote_market]["stepSize"]

          # Format sizes
          base_size = format_number(base_quantity, base_step_size)
          quote_size = format_number(quote_quantity, quote_step_size)

          # Ensure size
          base_min_order_size = markets["markets"][base_market]["minOrderSize"]
          quote_min_order_size = markets["markets"][quote_market]["minOrderSize"]
          check_base = float(base_quantity) > float(base_min_order_size)
          check_quote = float(quote_quantity) > float(quote_min_order_size)

          # If checks pass, place trades
          if check_base and check_quote:

            # Check account balance
            account = client.private.get_account()
            free_collateral = float(account.data["account"]["freeCollateral"])
            print(f"Balance: {free_collateral} and minimum at {USD_MIN_COLLATERAL}")

            # Guard: Ensure collateral
            if free_collateral < USD_MIN_COLLATERAL:
              break

            # Create Bot Agent
            bot_agent = BotAgent(
              client,
              market_1=base_market,
              market_2=quote_market,
              base_side=base_side,
              base_size=base_size,
              base_price=accept_base_price,
              quote_side=quote_side,
              quote_size=quote_size,
              quote_price=accept_quote_price,
              accept_failsafe_base_price=accept_failsafe_base_price,
              z_score=z_score,
              half_life=half_life,
              hedge_ratio=hedge_ratio
            )

            # Open Trades
            bot_open_dict = bot_agent.open_trades()
            

               
            # Guard: Handle failure
            if bot_open_dict == "failed":
              continue

            # Handle success in opening trades
            if bot_open_dict["pair_status"] == "LIVE":

              nowtemp = datetime.now()
              now = nowtemp.strftime("%d/%m/%Y %H:%M:%S")
              ################################################################

              if base_side=="BUY" :
                base_tot = -(float(base_price)*float(base_size))
                quote_tot = (float(quote_price)*float(quote_size))
              
              if base_side=="SELL":
                base_tot = (float(base_price)*float(base_size))
                quote_tot = -(float(quote_price)*float(quote_size))

              ################################################################
              # AL POSTO DI accept_base_price and quote size
              # vorrei inserire il valore effettivo del costo dell'ordine
              # da prendere da dydx



              posizione= {"market_1":base_market, "market_2":quote_market,"base_side":base_side,"base_size":base_size,"base_price":accept_base_price,"quote_side":quote_side,"quote_size":quote_size,"quote_price":accept_quote_price,"z_score":z_score,"half_life":half_life,
              "order_time_m1":now,"order_time_m2":now,
              "order_id_m1":bot_open_dict["order_id_m1"],"order_id_m2":bot_open_dict["order_id_m2"],"base_tot":base_tot,"quote_tot":quote_tot}

              storico.append(posizione)
              ##############################################################
              # Append to list of bot agents
              bot_agents.append(bot_open_dict)
              print("Ok - trade aperto on dydx - aggiorno anche json")
              send_message("Ok - trade aperto on dydx - aggiorno anche json")
              
              if len(bot_agents) > 0:
                with open("bot_agents.json", "w") as f:json.dump(bot_agents, f)
              # Confirm live status in print
              send_message("Trade status: Live")
              print("Trade status: Live")
              print("---")
              ##################################################################
              #QUI VORREI INSERIRE L'APERTURA DELL'ORDINE NELLO STORICO ORDINI
              if len(storico) > 0:
                with open("storico.json", "w") as f:json.dump(storico, f)
                


  # Save agents
  print(f"Success: Manage open trades checked- aggiornamento di fine ciclo json")
  send_message(f"Success: Manage open trades checked- aggiornamento di fine ciclo json")

  del bot_agents
  del storico  
