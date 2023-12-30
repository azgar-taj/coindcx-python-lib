from time import sleep
from api_library.api_market import CoinDCXAPIMarket
from api_library.api_user import CoinDCXAPIUser
from api_library.api_orders import CoinDCXAPIOrders
from api_library.api_common import OrderType, OrderKind
from datetime import datetime
import math

MARKET_DATA = CoinDCXAPIMarket()
USER_DATA = CoinDCXAPIUser()
ORDERS_DATA = CoinDCXAPIOrders()

viable_markets = MARKET_DATA.markets_data

BUY_PRICE = 999999.99
IN_INVENTORY = False
TREND_INDICATOR = 0
TREND_PRICE = 0

def fill_order_and_get_average_price(order_kind: OrderKind, market, quantity, price, order_type: OrderType):
    print(f'[{datetime.now()}] Filling order for {market} at {price} for {quantity} {order_kind.value}')
    order = ORDERS_DATA.make_order(order_kind, market, quantity, price, order_type)
    print(order)
    order_id = order['orders'][0]['id']
    order_filled = False
    order_status = ''
    while not order_filled:
        sleep(0.5)
        order_status = ORDERS_DATA.get_order_status(order_id)
        order_filled = order_status['status'] == 'filled'
    return order_status['avg_price']

COIN_MARKET = 'CLVUSDT'
INVESTMENT = 10.0

def get_investing_quantity(last_price):
    return round(INVESTMENT/float(last_price), viable_markets[COIN_MARKET]['precision'])

while True:
    sleep(0.75) # 0.75 seconds is the minimum time between requests
    for current_trend in MARKET_DATA.get_tickers():
        if COIN_MARKET in current_trend.get('market', 'UNKNOWN') :
            print(f'[{datetime.now()}] Current Price: {current_trend["last_price"]}, Our Price: {BUY_PRICE}, Trend Indicator: {TREND_INDICATOR} ')

            if float(current_trend['last_price']) > TREND_PRICE:
                if TREND_INDICATOR < 0:
                    TREND_INDICATOR = 0
                TREND_INDICATOR = TREND_INDICATOR + 1
            elif float(current_trend['last_price']) < TREND_PRICE:
                if TREND_INDICATOR > 0:
                    TREND_INDICATOR = 0
                TREND_INDICATOR = TREND_INDICATOR - 1

            TREND_PRICE = float(current_trend['last_price'])

            if (float(current_trend['last_price']) < BUY_PRICE or TREND_INDICATOR > 5 or TREND_INDICATOR < -5) and not IN_INVENTORY:
                print(f'[{datetime.now()}] Buying {current_trend["market"]} at {current_trend["last_price"]}')
                price = (fill_order_and_get_average_price(OrderKind.BUY, current_trend["market"], get_investing_quantity(current_trend['last_price']), current_trend['last_price'], OrderType.MARKET))
                print(f'[{datetime.now()}] Bought {current_trend["market"]} at {price}')
                IN_INVENTORY = True
                BUY_PRICE = price * 1.005 # 0.5% surcharge by coinDCX

            if float(current_trend['last_price']) > BUY_PRICE and IN_INVENTORY:
                print(f'[{datetime.now()}] Selling {current_trend["market"]} at {current_trend["last_price"]}')
                price = (fill_order_and_get_average_price(OrderKind.SELL, current_trend["market"], get_investing_quantity(current_trend['last_price']), current_trend['last_price'], OrderType.MARKET))
                print(f'[{datetime.now()}] Sold {current_trend["market"]} at {price}')
                IN_INVENTORY = False
                BUY_PRICE = price
