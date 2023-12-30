import requests
from typing import List, Dict

class CoinDCXAPIMarket:
    def __init__(self):
        self.base_url = "https://api.coindcx.com"
        self.public_url = "https://public.coindcx.com"
        self.current_markets_data = self.get_markets_data()

    def get_markets_data(self) -> List[Dict[str, str]]:
        viable_markets={}
        for market_data in self.get_markets_details():
            if market_data['status'] == 'active':
                viable_markets[market_data['symbol']] = \
                    { 
                        'market_pair': market_data['pair'],
                        'precision': market_data['target_currency_precision'],
                        'min_quantity': market_data['min_quantity'],
                        'ecode': market_data['ecode'],
                    }
        return viable_markets

    def get_markets(self) -> List[Dict[str, str]]:
        uri = '/exchange/v1/markets'
        url = self.base_url + uri
        response = requests.get(url)
        data = response.json()
        return data

    def get_tickers(self) -> List[Dict[str, str]]:
        uri = '/exchange/ticker'
        url = self.base_url + uri
        response = requests.get(url)
        data = response.json()
        return data

    def get_markets_details(self) -> List[Dict[str, str]]:
        uri = '/exchange/v1/markets_details'
        url = self.base_url + uri
        response = requests.get(url)
        data = response.json()
        return data

    def get_orderbook(self, pair):
        uri = f'/market_data/orderbook?pair={pair}'
        url = self.public_url + uri
        response = requests.get(url)
        data = response.json()
        return data

    def get_trades(self, pair):
        uri = f'/market_data/trade_history?pair={pair}&limit=50'
        url = self.public_url + uri
        response = requests.get(url)
        data = response.json()
        return data
