from datamodel import *

class Trader:
    def run(self, market_listings):
        orders = []
        product = Listing(market_listings, "Amethysts")
        
        bids= list(product.buy_orders)
        bid_quantities = list(product.buy_orders.values())
        bid_quantities = [value.iloc[0] for value in bid_quantities]

        asks = list(product.sell_orders.keys())
        ask_quantities = list(product.sell_orders.values())
        ask_quantities = [value.iloc[0] for value in ask_quantities]

        # print(list(product.buy_orders.items()))
        #error with getting the asks
        price = 100000
        if bids[0] > price:
            highest_bid = asks[0]
            orders.append(Order("Amethysts", price, -5))
        
        elif asks[0] < price:
            lowest_ask = bids[0]
            orders.append(Order("Amethysts", price, 5))
        return orders