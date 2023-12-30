from api_library.api_core import CoinDCXAPICore
from api_library.api_common import OrderType, OrderKind
from api_library.api_market import CoinDCXAPIMarket
from celery import app


class CoinDCXAPIMargin(CoinDCXAPICore, CoinDCXAPIMarket):
    @app.task
    def get_margin_balances(self):
        url = self.base_url + '/exchange/margin/v1/balances'
        return self.make_post_request(url, {})
    
    def get_margin_balance(self, currency):
        url = self.base_url + '/exchange/margin/v1/balances'
        data = self.make_post_request(url, {})
        for balance in data:
            if balance['currency'] == currency:
                return balance
    
    def get_margin_info(self):
        url = self.base_url + '/exchange/margin/v1/info'
        return self.make_post_request(url, {})
    
    def get_margin_positions(self):
        url = self.base_url + '/exchange/margin/v1/positions'
        return self.make_post_request(url, {})
    
    def get_margin_position(self, pair):
        url = self.base_url + '/exchange/margin/v1/positions'
        data = self.make_post_request(url, {})
        for position in data:
            if position['pair'] == pair:
                return position
    
    def get_margin_active_orders(self):
        url = self.base_url + '/exchange/margin/v1/orders'
        return self.make_post_request(url, {})
    
    def get_margin_order_status(self, order_id):
        url = self.base_url + '/exchange/margin/v1/orders/status'
        body = {
            "id": order_id
        }
        return self.make_post_request(url, body)
    
    def get_margin_order_history(self):
        url = self.base_url + '/exchange/margin/v1/orders/trade_history'
        return self.make_post_request(url, {})
    
    def get_margin_order_history_by_id(self, order_id):
        url = self.base_url + '/exchange/margin/v1/orders/trade_history'
        body = {
            "id": order_id
        }
        return self.make_post_request(url, body)
    
    def get_margin_order_history_by_pair(self, pair):
        url = self.base_url + '/exchange/margin/v1/orders/trade_history'
        body = {
            "pair": pair
        }
        return self.make_post_request(url, body)
    
    def place_margin_order(self, side: OrderKind, pair, quantity, price, order_type: OrderType, leverage):
        url = self.base_url + '/exchange/v1/margin/create'
        body = {
            "side": side.value,
            "order_type": order_type.value,
            "market": pair,
            "price": price,
            "quantity": quantity,
            "ecode": self.current_markets_data[pair]['ecode'],
            "leverage": leverage,
        }
        return self.make_post_request(url, body)