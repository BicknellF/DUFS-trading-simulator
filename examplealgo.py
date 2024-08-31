from datamodel import *

class Trader:
    last_price = 0
    def run(self, orderbook, products, state):
        orders = []
        for product in products:
            listings = Listing(orderbook[product], product)
            
            highest_bid = list(listings.buy_orders.keys())[0]
            bid_quantities = list(listings.buy_orders.values())

            lowest_ask = list(listings.sell_orders.keys())[0]
            ask_quantities = list(listings.sell_orders.values())
            
            orders.append(Order(product, lowest_ask - 1, 5))
            orders.append(Order(product, highest_bid + 1, -5))
        return orders