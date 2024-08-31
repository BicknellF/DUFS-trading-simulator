import logging
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List
import argparse
import importlib.util
import sys

from datamodel import Listing, Order, Portfolio
from dataimport import read_file, extract_orders, extract_bot_orders
from ordermatching import match_order

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
POSITION_LIMIT = 20
MAX_TICKS = 1000

def import_trader(file_path: str) -> type:
    """
    Import the Trader class from the specified file.

    :param file-path: Trading algo filepath.
    """
    try:
        spec = importlib.util.spec_from_file_location("trader_module", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.Trader
    except Exception as e:
        logging.error(f"Error importing Trader class from {file_path}: {str(e)}")
        sys.exit(1)

def initialize_portfolio(products: List[str]) -> Portfolio:
    portfolio = Portfolio()
    for product in products:
        portfolio.quantity[product] = 0
    return portfolio

def add_bot_orders(orderbook: Dict[str, Dict], bot_orders: Dict[str, Dict]) -> None:
    """
    Add bot orders to the existing orderbook.
    
    :param orderbook: Current orderbook
    :param bot_orders: Bot orders in the same format as the orderbook
    """
    for product, sides in bot_orders.items():
        for side, pricepoints in sides.items():
            if product not in orderbook:
                orderbook[product] = {"BUY": {}, "SELL": {}}
            if side not in orderbook[product]:
                orderbook[product][side] = {}
            
            for price, quantity in pricepoints.items():
                if price in orderbook[product][side]:
                    orderbook[product][side][price] += quantity
                else:
                    orderbook[product][side][price] = quantity

def process_tick(tick: int, orderbook: Dict[str, Dict], bot_orders: Dict[str, Dict], algo, portfolio: Portfolio, products: List[str], pos_limit: Dict[str, int]) -> None:
    try:
        # Get orders from the trader 
        algo_orders = algo.run(orderbook, products)

        # Add bot orders to the orderbook
        add_bot_orders(orderbook, bot_orders)

        # Process algo orders
        if algo_orders:
            for order in algo_orders:
                # if order.is_valid():
                #     print(order)
                match_order(order, orderbook, portfolio, pos_limit)

        portfolio.pnl = portfolio.cash
        for product in products:
            portfolio.pnl += portfolio.quantity[product] * next(iter(orderbook[product]["SELL"]))
    except Exception as e:
        logging.error(f"Error processing tick {tick}: {str(e)}")

def update_quantity_data(quantity_data: pd.DataFrame, tick: int, portfolio: Portfolio, products: List[str]) -> None:
    quantity_data.loc[tick, "PnL"] = portfolio.pnl
    quantity_data.loc[tick, "Cash"] = portfolio.cash
    for product in products:
        quantity_data.loc[tick, f"{product}_quantity"] = portfolio.quantity[product]

def main(file_path: str, bot_file_path: str, trader_file: str) -> None:
    try:
        products, ticks, df = read_file(file_path)
        bot_df = pd.read_csv(bot_file_path)
        portfolio = initialize_portfolio(products)
        pos_limit = {product: POSITION_LIMIT for product in products}

        # Import the Trader class
        Trader = import_trader(trader_file)
        algo = Trader()

        # Initialize the portfolio's initial value
        portfolio.initial_value = portfolio.cash
        for product in products:
            try:
                portfolio.initial_value += portfolio.quantity[product] * next(iter(extract_orders(df, 1, product)["SELL"]))
            except StopIteration:
                logging.warning(f"No sell orders for {product} at tick 1")

        quantity_data = pd.DataFrame(index=range(1, ticks), columns=[f"{product}_quantity" for product in products] + ["PnL", "Cash"])

        start = datetime.now()
        for tick in range(1, MAX_TICKS):
            print(tick)
            try:
                orderbook = {product: extract_orders(df, tick, product) for product in products}
                bot_orders = {product: extract_bot_orders(bot_df, tick, product) for product in products}
                process_tick(tick, orderbook, bot_orders, algo, portfolio, products, pos_limit)
                update_quantity_data(quantity_data, tick, portfolio, products)
            except Exception as e:
                logging.error(f"Error in tick {tick}: {str(e)}")

        end = datetime.now()
        logging.info(f"Time per tick: {(end-start)/MAX_TICKS}")
        logging.info(quantity_data)

        # Plotting
        quantity_data["PnL"].plot(legend=True)
        quantity_data["Cash"].plot(legend=True)
        plt.show()

    except Exception as e:
        logging.error(f"Error in main function: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the trading simulation.")
    parser.add_argument("--round", default="Round Data/Options/Option_round_test.csv", help="Path to the main data file")
    parser.add_argument("--bot-file", default="Round Data/Options/Option_round_test_bots.csv", help="Path to the bot data file")
    parser.add_argument("--trader", default="examplealgo.py", help="Path to the file containing the Trader class")
    args = parser.parse_args()

    main(args.file, args.bot_file, args.trader, args.max_ticks)