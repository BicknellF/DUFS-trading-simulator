from enum import Enum
from collections import deque
from sortedcontainers import SortedDict


class OrderDirection(Enum):
    BUY = 1
    SELL = 2

    def __str__(self):
        if self.value == 1:
            return "BUY"
        elif self.value == 2:
            return "SELL"
        else:
            return ""

class PricePoint:
    def __init__(self):
        self.limit_price: int | None = None
        self.size: int = 0
        self.total_volume: int = 0

        self.head_order: OrderBookEntry | None = None
        self.tail_order: OrderBookEntry | None = None


class Order:
    """
    id, 
    timestamp (utc) use time.time(), 
    type (buy/sell), 
    price, 
    size
    """
    def __init__(self, id : int, timestamp : float, direction : OrderDirection, price : int, quantity : int, ) -> None:
        self.id: int = id
        self.timestamp: float = timestamp
        self.direction: OrderDirection = direction
        self.price: int = price
        self.quantity: int = quantity

    def __str__(self):
        return f"{self.direction} {self.quantity}@{self.price} [{self.id}; {self.timestamp}]" 




class OrderBookEntry:
    def __init__(self, order: Order, parent_pricepoint = None):  
        self.order: Order = order

        self.next_order = None
        self.prev_order = None
        self.parent_pricepoint = parent_pricepoint
    

class OrderTree:
    def __init__(self):
        self.price_points: SortedDict = SortedDict() # maps price (int) -> PricePoint (sorted increasingly)
    
    def get_depth(self) -> int:
        return len(self.price_points)

    def get_max_price(self) -> int | None:
        if len(self.price_points) > 0:
            price, pricepoint = self.price_points.peekitem(-1)
            return price
        else:
            return None

    def get_min_price(self) -> int | None:
        if len(self.price_points) > 0:
            price, pricepoint = self.price_points.peekitem(0)
            return price
        else:
            return None

class OrderBook:
    """
    https://quant.stackexchange.com/questions/3783/what-is-an-efficient-data-structure-to-model-order-book

    https://web.archive.org/web/20110219163448/http://howtohft.wordpress.com/2011/02/15/how-to-build-a-fast-limit-order-book/

    For each price point save a list of orders (in order of arrival).
    """

    def __init__(self):
        self.history = deque()
        self.orders: dict[int, OrderBookEntry] = dict() # Maps order id -> order

        self.buy_book: OrderTree = OrderTree()
        self.sell_book: OrderTree = OrderTree()


    
    def process_order(self, order: Order):
        # Add new order to books
        entry = None
        trades = []

        if order.direction == OrderDirection.BUY:
            while order.quantity > 0 and self.sell_book.get_depth() != 0 and order.price >= self.sell_book.get_max_price(): # cross trades
                ...
            
            # insert into buy order book

        elif order.direction == OrderDirection.SELL:

            while order.quantity > 0 and self.buy_book.get_depth() != 0 and order.price <= self.buy_book.get_min_price(): # cross trades
                ...
            
            # insert order into sell order book




        
