from datamodel import Listing, Order
from dataimport import read_file, extract_orders, read_bot_file
from ordermatching import match_order
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List
from examplealgo import Trader
import datetime

# Constants
FILE_PATH = "Round Data/Options/Option_round_test.csv"
BOT_FILE_PATH = "path/to/bot_data.csv"
POSITION_LIMIT = 20
MAX_TICKS = 100

class Portfolio:
    def __init__(self) -> None:
        self.cash: float = 0
        self.quantity: Dict[str, int] = {}
        self.pnl: float = 0

def initialize_portfolio(products: List[str]) -> Portfolio:
    portfolio = Portfolio()
    for product in products:
        portfolio.quantity[product] = 0
    return portfolio

def add_bot_orders_to_orderbook(orderbook: Dict[str, Dict], bot_orders: List[Order]) -> None:
    """
    IMPLEMEMNT THIS
    """

def process_tick(tick: int, orderbook: Dict[str, Dict], algo: Trader, bot_orders: List[Order], portfolio: Portfolio, products: List[str], pos_limit: Dict[str, int]) -> None:
    # Get orders from the trader 
    algo_orders = algo.run(orderbook, products)

    # Add bot orders to the orderbook
    add_bot_orders_to_orderbook(orderbook, bot_orders)

    # Process algo orders
    if algo_orders:
        for order in algo_orders:
            if order.is_valid():
                match_order(order, orderbook, portfolio, pos_limit)

    portfolio.pnl = portfolio.cash
    for product in products:
        portfolio.pnl += portfolio.quantity[product] * next(iter(orderbook[product]["SELL"]))

def update_quantity_data(quantity_data: pd.DataFrame, tick: int, portfolio: Portfolio, products: List[str]) -> None:
    quantity_data.loc[tick, "PnL"] = portfolio.pnl
    quantity_data.loc[tick, "Cash"] = portfolio.cash
    for product in products:
        quantity_data.loc[tick, f"{product}_quantity"] = portfolio.quantity[product]

def main():
    products, ticks, df = read_file(FILE_PATH)
    bot_data = read_bot_file(BOT_FILE_PATH)
    portfolio = initialize_portfolio(products)
    pos_limit = {product: POSITION_LIMIT for product in products}

    quantity_data = pd.DataFrame(index=range(1, ticks), columns=[f"{product}_quantity" for product in products] + ["PnL", "Cash"])
    algo = Trader()

    start = datetime.now()
    for tick in range(1, MAX_TICKS):
        print(tick)
        orderbook = {product: extract_orders(df, tick, product) for product in products}
        bot_orders = [order for order in bot_data if order.tick == tick]
        process_tick(tick, orderbook, algo, bot_orders, portfolio, products, pos_limit)
        update_quantity_data(quantity_data, tick, portfolio, products)

    end = datetime.now()
    print(f"Time per tick: {(end-start)/MAX_TICKS}")
    print(quantity_data)

    # Plotting
    quantity_data["PnL"].plot(legend=True)
    quantity_data["Cash"].plot(legend=True)
    plt.show()

if __name__ == "__main__":
    main()