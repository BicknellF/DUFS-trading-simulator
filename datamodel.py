#position limit needs adding

class Listing: # potentially separate buyprice and sell price
    def __init__(self, orderbook, product) -> None:
        self.buy_orders = orderbook["BUY"] #dict of {price: quantity} top is lowest price
        self.sell_orders = orderbook["SELL"] #dict of {price: quantity} top is highest price
        self.product = product
        
class Order:
    def __init__(self, symbol, price, quantity) -> None:
        self.symbol = symbol
        self.quantity = quantity
        self.price = price

class Market:
    def __init__(self, traderData, tick, listings, order_depths, own_trades, market_trades, position, observations):
        self.tick = tick
        self.listings = listings
