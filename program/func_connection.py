from decouple import config
from dydx3 import  Client
from web3 import Web3
from func_messaging import send_message
from constants import (
    HOST, 
    ETHEREUM_ADDRESS,
    DYDX_API_KEY,
    DYDX_SECRET,
    DYDX_API_PASSPHRASE,
    STARK_PRIVATE_KEY,
    HTT_PROVIDER
)

def connect_dydx():
    client=Client(


        host=HOST,
        api_key_credentials={
            "key":DYDX_API_KEY,
            "secret":DYDX_SECRET,
            "passphrase":DYDX_API_PASSPHRASE
        },

        stark_private_key=STARK_PRIVATE_KEY,
        eth_private_key=config("ETH_PRIVATE_KEY"),
        default_ethereum_address=ETHEREUM_ADDRESS,
        web3=Web3(Web3.HTTPProvider(HTT_PROVIDER))
    )

    #confirm client

    account= client.private.get_account()
    account_id=account.data["account"]["id"]
    quote_balance= account.data['account']["quoteBalance"]
    send_message(f'Your balance is {quote_balance}')
    print("connection")
    print(account_id)
    print(quote_balance)

    return client