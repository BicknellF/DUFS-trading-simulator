from datamodel import Listing, Order
from dataimport import read_file, extract_orders
from ordermatching import match_order
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List
from examplealgo import Trader

# Constants
FILE_PATH = "Round Data/Options/Option_round_test.csv"
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

def process_tick(tick: int, orderbook: Dict[str, Dict], algo: Trader, portfolio: Portfolio, products: List[str], pos_limit: Dict[str, int]) -> None:
    orders = algo.run(orderbook, products)

    if orders:
        for order in orders:
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
    portfolio = initialize_portfolio(products)
    pos_limit = {product: POSITION_LIMIT for product in products}

    quantity_data = pd.DataFrame(index=range(1, ticks), columns=[f"{product}_quantity" for product in products] + ["PnL", "Cash"])
    algo = Trader()

    start = datetime.now()
    for tick in range(1, MAX_TICKS):
        print(tick)
        orderbook = {product: extract_orders(df, tick, product) for product in products}
        process_tick(tick, orderbook, algo, portfolio, products, pos_limit)
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