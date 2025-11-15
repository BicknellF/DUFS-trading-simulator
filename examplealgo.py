from datamodel import *

class Trader:
    def run(self, state):
        orders = []
        for product in state.products:
            listings = Listing(state.orderbook[product], product)
            highest_bid = list(listings.buy_orders.keys())[0]
            bid_quantities = list(listings.buy_orders.values())

            lowest_ask = list(listings.sell_orders.keys())[0]
            ask_quantities = list(listings.sell_orders.values())
            if highest_bid > 10000:
                orders.append(Order(product, highest_bid, -5))
            if lowest_ask < 10000:
                orders.append(Order(product, lowest_ask, 5))

        return orders
