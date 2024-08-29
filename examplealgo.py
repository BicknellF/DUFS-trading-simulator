from datamodel import *

class Trader:
    last_price = 0
    def run(self, orderbook, products):
        orders = []
        product = Listing(orderbook, "Amethysts")
        
        bids= list(product.buy_orders)
        bid_quantities = list(product.buy_orders.values())

        asks = list(product.sell_orders.keys())
        ask_quantities = list(product.sell_orders.values())

        price = self.last_price
        if bids[0] > price:
            highest_bid = asks[0]
            orders.append(Order("Amethysts", asks[0], -5))
            self.last_price = bids[0]
        
        elif asks[0] < price:
            lowest_ask = bids[0]
            orders.append(Order("Amethysts", bids[0], 5))
            self.last_price = bids[0]
        return orders