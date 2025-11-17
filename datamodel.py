from typing import Dict, List

class Listing:
    """
    A class to represent the
    """
    def __init__(self, orderbook: Dict[str, Dict[int, int]], product: str) -> None:
        self.buy_orders = orderbook["BUY"] #dict of {price: quantity} top is lowest price
        self.sell_orders = orderbook["SELL"] #dict of {price: quantity} top is highest price
        self.product = product

class Order:
    """
    A class to represent an order sent to the matching engine.
    """
    def __init__(self, product: str, price: int, quantity: int):
        self.product = product
        self.price = price
        self.quantity = quantity

    def is_valid(self) -> bool:
        return (isinstance(self.product, str) and self.product and
                isinstance(self.quantity, int) and self.quantity != 0 and
                isinstance(self.price, int) and self.price > 0)

    def __str__(self):
        return f"Order(product={self.product}, price={self.price}, quantity={self.quantity})"

class Portfolio:
    """
    A class to represent the trader's current portfolio.
    """
    def __init__(self):
        self.cash: float = 0
        self.quantity: Dict[str, int] = {}
        self.pnl: float = 0

    def __str__(self):
        return f"Portfolio(cash={self.cash}, quantity={self.quantity}, pnl={self.pnl})"

class State:
    """
    A class to represent the state of the market and the trader's portfolio.
    """
    def __init__(self, orderbook: Dict[str, Dict[int, int]], positions: Dict[str, int], products: List[str], pos_limit: int):
        self.orderbook = orderbook
        self.positions = positions
        self.products = products
        self.pos_limit = pos_limit


