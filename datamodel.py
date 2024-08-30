#position limit needs adding

class Listing: # potentially separate buyprice and sell price
    def __init__(self, orderbook, product) -> None:
        self.buy_orders = orderbook["BUY"] #dict of {price: quantity} top is lowest price
        self.sell_orders = orderbook["SELL"] #dict of {price: quantity} top is highest price
        self.product = product
        
class Order:
    def __init__(self, product: str, order_type: str, quantity: int, price: float):
        self.product = product
        self.order_type = order_type
        self.quantity = quantity
        self.price = price

    def is_valid(self) -> bool:
        """
        Check if the order is valid based on certain criteria.
        
        Returns:
        bool: True if the order is valid, False otherwise.
        """
        # Check if the order has a valid product
        if not self.product or not isinstance(self.product, str):
            return False
        
        # Check if the order has a valid quantity (non-zero integer)
        if not isinstance(self.quantity, int) or self.quantity == 0:
            return False
        
        # Check if the order has a valid price (positive float)
        if not isinstance(self.price, float) or self.price <= 0:
            return False
        
        # Check if the order type is valid (BUY or SELL)
        if self.order_type not in ["BUY", "SELL"]:
            return False
        
        # All checks passed, the order is valid
        return True

class Market:
    def __init__(self, traderData, tick, listings, order_depths, own_trades, market_trades, position, observations):
        self.tick = tick
        self.listings = listings
