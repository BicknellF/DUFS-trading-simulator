from datamodel import *

class Trader:
    last_price = 0
    def run(self, orderbook, products):
        orders = []
        for product in products:
            listings = Listing(orderbook[product], product)
            
            bids= list(listings.buy_orders)
            bid_quantities = list(listings.buy_orders.values())

            asks = list(listings.sell_orders.keys())
            ask_quantities = list(listings.sell_orders.values())

            price = self.last_price
            if bids[0] > price:
                highest_bid = asks[0]
                orders.append(Order(product, asks[0], -5))
                self.last_price = bids[0]
            
            elif asks[0] < price:
                lowest_ask = bids[0]
                orders.append(Order(product, bids[0], 5))
                self.last_price = bids[0]
        return orders