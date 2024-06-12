from datamodel import *
from dataimport import *
from Runscript import *
from datetime import datetime


#### CURRENT ISSUES
"""
Orders ordering too much, specifically when trying to buy
"""
class Portfolio:
    def __init__(self) -> None:
        self.cash = 100000
        self.quantity = 0

portfolio = Portfolio()

filepath = "trading comp\prices_round_1_day_-1.csv"
product = "AMETHYSTS"
pos_limit = 20
df = read_file(filepath, product)
ticks = len(df)
# for each trader id in list
#from trader_id import Trader

from examplealgo import Trader

start = datetime.now()
for tick in range(0, ticks):
    market_listings = extract_orders(df, tick)
    sell_orders = market_listings[1]
    buy_orders = market_listings[0]

    algo = Trader()
    orders = algo.run(market_listings)
    if orders != []:
        buy_prices = list(buy_orders.keys())
        buy_quantities = list(buy_orders.values())
        buy_quantities = [value.iloc[0] for value in buy_quantities]

        sell_prices = list(sell_orders.keys())
        sell_quantities = list(sell_orders.values())
        sell_quantities = [value.iloc[0] for value in sell_quantities]

        # order matching
        for order in orders: 
            print("!!")
            print(order.quantity)
            print(order.price)
            print("!!")
            if order.quantity < 0: # sell orders
                #match order with a buy order
                quantity = order.quantity
                for i in range(len(buy_orders)):
                    if buy_quantities[i] != 0:
                        if buy_prices[i] >= order.price:
                            print(f"Quantity at {buy_prices[i]} = {buy_quantities[i]}")
                            fulfilled_amount = min(int(pos_limit - abs(portfolio.quantity)), -quantity, buy_quantities[i]) #quantity before order limit, order quantity remaining, quantity avaliable, 
                            print(fulfilled_amount)
                            portfolio.quantity -= fulfilled_amount
                            buy_quantities[i] -= fulfilled_amount
                            portfolio.cash += fulfilled_amount * order.price
                            quantity += fulfilled_amount
                    if quantity == 0 or buy_prices[i] < order.price:
                        print("OUT")
                        break
                    print(f"quantity left = {quantity}")

            elif order.quantity > 0: # buy orders
                quantity = order.quantity
                for i in range(0,len(buy_orders)):
                    if sell_quantities[i] != 0:
                        print(f"sell price = {sell_prices[i]}, our order = {order.price}")
                        if sell_prices[i] <= order.price:
                            print(f"Quantity at {sell_prices[i]} = {sell_quantities[i]}")
                            fulfilled_amount = min(int(pos_limit - abs(portfolio.quantity)), order.quantity, sell_quantities[i])
                            print(f"ffd amt:{fulfilled_amount}")
                            portfolio.quantity += fulfilled_amount
                            sell_quantities[i] += fulfilled_amount
                            portfolio.cash -= fulfilled_amount * order.price
                            quantity -= fulfilled_amount
                    if quantity == 0 or sell_prices[i] > order.price:
                        print("OUT")
                        break
                    print(f"quantity left = {quantity}")
    break

end = datetime.now()

print(end-start)

print(portfolio.quantity)
    