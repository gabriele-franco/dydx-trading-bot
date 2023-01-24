from test import data
import numpy as np


ask_prices = np.array([ask['price'] for ask in data['asks']]).astype(np.float64)
ask_sizes = np.array([ask['size'] for ask in data['asks']]).astype(np.float64)


"""bid_prices = np.array([bid['price'] for bid in data['bids']]).astype(np.float)
bid_sizes = np.array([bid['size'] for bid in data['bids']]).astype(np.float)
"""




if len(ask_sizes) > 0:
    t=sum(ask_sizes)/len(ask_sizes)
    p= ask_prices[0]

    print(f'sizes {t} and price{p}')
