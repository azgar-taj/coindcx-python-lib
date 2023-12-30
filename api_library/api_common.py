from enum import Enum

class OrderType(Enum):
    LIMIT = 'limit_order'
    MARKET = 'market_order'

class OrderKind(Enum):
    BUY = 'buy'
    SELL = 'sell'
