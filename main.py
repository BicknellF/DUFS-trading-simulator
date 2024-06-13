from datamodel import *
from dataimport import *
from Runscript import *
from datetime import datetime
import matplotlib.pyplot as plt


#### CURRENT ISSUES
"""
Orders ordering too much, specifically when trying to buy
"""
class Portfolio:
    def __init__(self) -> None:
        self.cash = 0
        self.quantity = 0
        self.value = 0

portfolio = Portfolio()

filepath = "trading comp\prices_round_1_day_-1.csv"
product = "AMETHYSTS"
pos_limit = 20
df = read_file(filepath, product)
ticks = len(df)
# for each trader id in list
#from trader_id import Trader

from examplealgo import Trader

vis = []
start = datetime.now()
for tick in range(0, 5000):
    print(tick)
    market_listings = extract_orders(df, tick)
    sell_orders = market_listings[1]
    buy_orders = market_listings[0]

    algo = Trader()
    orders = algo.run(market_listings)
    if orders != []:
        buy_prices = list(buy_orders.keys()) # market buy orders aka the price we can sell at
        buy_quantities = list(buy_orders.values())
        buy_quantities = [value.iloc[0] for value in buy_quantities]

        sell_prices = list(sell_orders.keys())
        sell_quantities = list(sell_orders.values())
        sell_quantities = [value.iloc[0] for value in sell_quantities]

        # order matching
        for order in orders: 
            if order.quantity < 0: # sell orders
                #match order with a buy order
                quantity = order.quantity
                for i in range(len(buy_orders)):
                    if buy_quantities[i] != 0:
                        if buy_prices[i] >= order.price:
                            fulfilled_amount = min(int(pos_limit + portfolio.quantity), -quantity, buy_quantities[i]) #quantity before order limit, order quantity remaining, quantity avaliable, 
                            portfolio.quantity -= fulfilled_amount
                            buy_quantities[i] -= fulfilled_amount
                            portfolio.cash += fulfilled_amount * order.price
                            portfolio.value -= fulfilled_amount * order.price
                            quantity += fulfilled_amount
                            print(f"selling {fulfilled_amount} at {buy_prices[i]}")
                    if quantity == 0 or buy_prices[i] < order.price:
                        #print("OUT")
                        break
                    #print(f"quantity left = {quantity}")

            elif order.quantity > 0: # buy orders
                quantity = order.quantity
                for i in range(0,len(sell_orders)):
                    if sell_quantities[i] != 0:
                        #print(f"sell price = {sell_prices[i]}, our order = {order.price}")
                        if sell_prices[i] <= order.price:
                            #print(f"Quantity at {sell_prices[i]} = {sell_quantities[i]}")
                            fulfilled_amount = min(int(pos_limit - portfolio.quantity), quantity, sell_quantities[i])
                            #print(f"ffd amt:{fulfilled_amount} out of qty: {quantity}")
                            portfolio.quantity += fulfilled_amount
                            sell_quantities[i] += fulfilled_amount
                            portfolio.cash -= fulfilled_amount * order.price
                            portfolio.value += fulfilled_amount * order.price
                            quantity -= fulfilled_amount
                            print(f"buying {fulfilled_amount} at {sell_prices[i]}")
                    if quantity == 0 or sell_prices[i] > order.price:
                        #print("OUT")
                        break
                    #print(f"quantity left = {quantity}")
    vis.append(portfolio.quantity)

end = datetime.now()

# roughly 0:00:00.001054 per tick
# roughly 10 seconds per day
print((end-start))

print(portfolio.quantity)
plt.plot(vis)
plt.show()