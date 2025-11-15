import logging
from datetime import datetime
import argparse
import sys
from typing import Dict, List
import importlib.util
import pandas as pd
import matplotlib.pyplot as plt
import copy

from datamodel import Portfolio, State
from dataimport import read_file, extract_orders, extract_bot_orders
from ordermatching import match_order
from analytics_vis import Visualiser

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Constants
POSITION_LIMIT = 20
MAX_TICKS = 1000


def import_trader(file_path: str) -> type:
    """
    Import the Trader class from the specified file.

    :param file_path: Trading algo filepath.
    """
    try:
        spec = importlib.util.spec_from_file_location("trader_module", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.Trader
    except Exception as e:
        logging.error(f"Error importing Trader class from {file_path}: {str(e)}")
        sys.exit(1)


def initialise_portfolio(products: List[str]) -> Portfolio:
    """
    Create an empty portfolio.

    :param products: Products to be traded.
    """
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


def process_tick(state: State, bot_orders: Dict[str, Dict], algo, portfolio) -> None:
    # Get orders from the trader

    ob_copy = {
        product: {side: orders.copy() for side, orders in ob.items()}
        for product, ob in state.orderbook.items()
    }
    publicstate = State(
        ob_copy, state.positions.copy(), state.products, state.pos_limit
    )

    algo_orders = algo.run(publicstate)

    # Process algo orders
    if algo_orders:
        # Add bot orders to the orderbook
        add_bot_orders(state.orderbook, bot_orders)
        for order in algo_orders:
            match_order(order, state.orderbook, portfolio, state.pos_limit)

    portfolio.pnl = portfolio.cash
    for product in state.products:
        best_bid = next(iter(state.orderbook[product]["BUY"]))
        best_ask = next(iter(state.orderbook[product]["SELL"]))
        midprice = (best_bid + best_ask) / 2
        portfolio.pnl += portfolio.quantity[product] * midprice


def update_quantity_data(
    quantity_data: pd.DataFrame, tick: int, portfolio: Portfolio, products: List[str]
) -> None:
    quantity_data.loc[tick, "PnL"] = portfolio.pnl
    quantity_data.loc[tick, "Cash"] = portfolio.cash
    for product in products:
        quantity_data.loc[tick, f"{product}_quantity"] = portfolio.quantity[product]


def prepare_analytics_data(
    quantity_data: pd.DataFrame, products: List[str], market_data: pd.DataFrame
) -> pd.DataFrame:

    analytics_df = pd.DataFrame(index=quantity_data.index)

    ticks = quantity_data.index

    for product in products:
        mid_prices = []
        bid_prices = []
        offer_prices = []
        for tick in ticks:
            try:
                row = market_data[market_data["timestamp"] == tick * 100]
                row = row[row["product"] == product]
                best_bid = row["bid_price_1"].iloc[0]
                best_ask = row["ask_price_1"].iloc[0]
                mid_price = (best_bid + best_ask) / 2
                bid_prices.append(best_bid)
                offer_prices.append(best_ask)
                mid_prices.append(mid_price)
            except:
                # If data missing, use NaN
                mid_prices.append(None)
                bid_prices.append(None)
                offer_prices.append(None)
        analytics_df[product] = mid_prices
        analytics_df[f"{product}_bid"] = bid_prices
        analytics_df[f"{product}_offer"] = offer_prices
    analytics_df["pnl"] = quantity_data["PnL"]

    return analytics_df


def main(round_data_path: str, trading_algo: str) -> None:
    products, ticks, df = read_file(round_data_path)
    bot_df = pd.read_csv(round_data_path[:-4] + "_bots.csv")
    market_data = df.copy()
    portfolio = initialise_portfolio(products)
    pos_limit = {product: POSITION_LIMIT for product in products}

    # Import the Trader class
    Trader = import_trader(trading_algo)
    algo = Trader()

    # Create a DataFrame to store the quantity data
    quantity_data = pd.DataFrame(
        index=range(1, ticks),
        columns=[f"{product}_quantity" for product in products] + ["PnL", "Cash"],
    )
    start = datetime.now()

    metrics = {"tick": [], "PnL": [], "Cash": []}
    for product in products:
        metrics[f"{product}_quantity"] = []

    for tick in range(1, MAX_TICKS):
        if tick % 100 == 0:
            print(tick)

        orderbook = {product: extract_orders(df, tick, product) for product in products}
        bot_orders = {
            product: extract_bot_orders(bot_df, tick, product) for product in products
        }
        state = State(orderbook, portfolio.quantity, products, pos_limit)
        try:
            process_tick(state, bot_orders, algo, portfolio)
            metrics["tick"].append(tick)
            metrics["PnL"].append(portfolio.pnl)
            metrics["Cash"].append(portfolio.cash)
            for product in products:
                metrics[f"{product}_quantity"].append(portfolio.quantity[product])

        except:
            break

    end = datetime.now()
    quantity_data = pd.DataFrame(metrics).set_index("tick")

    print(f"Time per tick: {(end-start)/MAX_TICKS}")

    # Portfolio summary
    print("\n=== Final Portfolio State ===")
    print(f"PnL: {portfolio.pnl:.2f}")

    analytics_df = prepare_analytics_data(quantity_data, products, market_data)
    positions_df = pd.DataFrame(index=quantity_data.index)
    for product in products:
        positions_df[product] = quantity_data[f"{product}_quantity"]
    vis = Visualiser(
        dataframe=analytics_df, products=products, volume_data=positions_df
    )
    vis.display_visualisation()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the trading simulation.")
    parser.add_argument(
        "--round",
        default="Round Data/Tutorial/tutorial.csv",
        help="Main data file path",
    )
    parser.add_argument(
        "--algo", default="examplealgo.py", help="Trading alngorithm path"
    )
    args = parser.parse_args()

    main(args.round, args.algo)
