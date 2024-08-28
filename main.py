from datamodel import Listing, Order
from dataimport import read_file, extract_orders
from ordermatching import match_order
from datetime import datetime

class Portfolio:
    def __init__(self) -> None:
        self.cash = 0
        self.quantity = {} 
        self.pnl = {}

filepath = "Round Data\Options\Option_round_test.csv"

pos_limit = 20
products, ticks, df = read_file(filepath)

from examplealgo import Trader # Loads the Trader class from the algorithm

# Initialise holdings of each product at 0
portfolio = Portfolio()
for product in products: 
    portfolio.quantity[product] = 0

algo = Trader()

start = datetime.now()
for tick in range(1, ticks):
    for product in products:
        orderbook = extract_orders(df, tick, product) 
        buy_orders = orderbook[0]
        sell_orders = orderbook[1]

        orders = algo.run(orderbook, products) # Run the submitted algorithm on this tick
        if orders != []:
            for order in orders: 
                #if order is valid:
                """
                CHECK IF THE ORDER IS A VALID ORDER
                """
                match_order(order, orderbook, portfolio, product, pos_limit)
    
    """
    PNL CALCULATIONS
    """

end = datetime.now()

# roughly 0:00:00.001054 per tick
# roughly 10 seconds per day
# 9.35
# 3 seconds with no printing
print((end-start))