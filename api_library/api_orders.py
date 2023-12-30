from enum import Enum
from api_library.api_core import CoinDCXAPICore
from api_library.api_common import OrderType, OrderKind

class CoinDCXAPIOrders(CoinDCXAPICore):
    def get_active_orders(self):
        url = self.base_url + '/exchange/v1/orders'
        return self.make_post_request(url, {})

    def get_order_status(self, order_id):
        url = self.base_url + '/exchange/v1/orders/status'
        body = {
            "id": order_id
        }
        return self.make_post_request(url, body)

    def make_order(self, side: OrderKind, market, quantity, price, order_type: OrderType):
        url = self.base_url + '/exchange/v1/orders/create'
        body = {
            "side": side.value,
            "order_type": order_type.value,
            "market": market,
            "price_per_unit": price,
            "total_quantity": quantity,
        }
        return self.make_post_request(url, body)
