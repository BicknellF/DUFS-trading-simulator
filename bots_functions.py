from typing import Dict
from datamodel import Portfolio


def clean_resting_orders(resting_orders: Dict[str, Dict[str, Dict[int, int]]]):
    """
    Removes price levels with 0 quantity from order books.

    :param resting_orders: An orderbook to clean.
    """
    for product, sides in resting_orders.items():
        for side, book in sides.items():
            empty_prices = [price for price, qty in book.items() if qty == 0]
            for price in empty_prices:
                del book[price]


def add_bot_orders(
    bot_orders: Dict[str, Dict],
    market_orderbook: Dict[str, Dict],
    algo_resting_orders: Dict[str, Dict],
    portfolio: Portfolio,
    pos_limit: Dict[str, int],
) -> None:
    """
    Process bot orders against the market and algo resting orders.

    :param bot_orders: Bot orders in the same format as the orderbook
    :param market_orderbook: The main market orderbook
    :param algo_resting_orders: The algo's resting orders
    :param portfolio: The portfolio to be updated
    :param pos_limit: The maximum quantity the portfolio can hold
    """

    for product, sides in bot_orders.items():
        if "BUY" in sides:
            bot_buy_orders = sides["BUY"]
            best_bot_buy_price = next(iter(bot_buy_orders.keys()), -1)

            if best_bot_buy_price == -1:
                continue

            bot_quantity = bot_buy_orders[best_bot_buy_price]

            all_sell_prices = set(market_orderbook[product]["SELL"].keys())
            if product in algo_resting_orders:
                all_sell_prices.update(algo_resting_orders[product]["SELL"].keys())

            for pricepoint in sorted(all_sell_prices):
                if best_bot_buy_price < pricepoint:
                    break
                if bot_quantity == 0:
                    break

                market_sells = market_orderbook[product]["SELL"]
                if pricepoint in market_sells:
                    available_market = market_sells[pricepoint]
                    filled = min(bot_quantity, available_market)

                    if filled > 0:
                        market_sells[pricepoint] -= filled
                        bot_quantity -= filled

                if bot_quantity > 0 and product in algo_resting_orders:
                    algo_sells = algo_resting_orders[product]["SELL"]
                    if pricepoint in algo_sells:
                        available_algo = algo_sells[pricepoint]

                        sell_room = int(
                            pos_limit[product] + portfolio.quantity.get(product, 0)
                        )

                        filled = min(bot_quantity, available_algo, sell_room)

                        if filled > 0:
                            portfolio.quantity[product] -= filled
                            portfolio.cash += filled * pricepoint

                            algo_sells[pricepoint] -= filled
                            bot_quantity -= filled

            if bot_quantity > 0:
                market_buys = market_orderbook[product]["BUY"]
                market_buys[best_bot_buy_price] = (
                    market_buys.get(best_bot_buy_price, 0) + bot_quantity
                )

        elif "SELL" in sides:
            bot_sell_orders = sides["SELL"]
            best_bot_sell_price = next(iter(bot_sell_orders.keys()), -1)

            if best_bot_sell_price == -1:
                continue

            bot_quantity = bot_sell_orders[best_bot_sell_price]

            all_buy_prices = set(market_orderbook[product]["BUY"].keys())
            if product in algo_resting_orders:
                all_buy_prices.update(algo_resting_orders[product]["BUY"].keys())

            for pricepoint in sorted(all_buy_prices, reverse=True):
                if best_bot_sell_price > pricepoint:
                    break
                if bot_quantity == 0:
                    break

                market_buys = market_orderbook[product]["BUY"]
                if pricepoint in market_buys:
                    available_market = market_buys[pricepoint]
                    filled = min(bot_quantity, available_market)

                    if filled > 0:
                        market_buys[pricepoint] -= filled
                        bot_quantity -= filled

                if bot_quantity > 0 and product in algo_resting_orders:
                    algo_buys = algo_resting_orders[product]["BUY"]
                    if pricepoint in algo_buys:
                        available_algo = algo_buys[pricepoint]

                        buy_room = int(
                            pos_limit[product] - portfolio.quantity.get(product, 0)
                        )

                        filled = min(bot_quantity, available_algo, buy_room)

                        if filled > 0:
                            portfolio.quantity[product] += filled
                            portfolio.cash -= filled * pricepoint

                            algo_buys[pricepoint] -= filled
                            bot_quantity -= filled

            if bot_quantity > 0:
                market_sells = market_orderbook[product]["SELL"]
                market_sells[best_bot_sell_price] = (
                    market_sells.get(best_bot_sell_price, 0) + bot_quantity
                )

    clean_resting_orders(algo_resting_orders)
