from datamodel import Order, Portfolio
from typing import Dict, Any

def match_order(order: Order, orderbook: Dict[str, Dict[str, Dict[int, int]]], portfolio: Any, pos_limit: Dict[str, int]):
    if order.quantity > 0:
        match_buy_order(order, orderbook[order.product]["SELL"], portfolio, pos_limit)
    elif order.quantity < 0:
        match_sell_order(order, orderbook[order.product]["BUY"], portfolio, pos_limit)
    else:
        pass

def match_buy_order(order: Order, sell_orders: Dict[int, int], portfolio: Any, pos_limit: Dict[str, int]):
    product = order.product
    product_limit = pos_limit[product]
    limit_price = order.price
    outstanding_quantity = order.quantity
    for pricepoint in sorted(sell_orders.keys()):
        if sell_orders[pricepoint] > 0:
            if pricepoint >= order.price:
                fulfilled_amount = min(int(product_limit - portfolio.quantity.get(product, 0)), outstanding_quantity, sell_orders[pricepoint]) #quantity before order limit, order quantity remaining, quantity avaliable, 
                
                # Update portfolio
                portfolio.quantity[product] += fulfilled_amount
                sell_orders[pricepoint] -= fulfilled_amount
                portfolio.cash -= fulfilled_amount * sell_orders[pricepoint]

                outstanding_quantity -= fulfilled_amount
                #print(f"selling {fulfilled_amount} at {buy_prices[i]}")
        
            if outstanding_quantity == 0 or pricepoint < limit_price:
                break
    

def match_sell_order(order: Order, buy_orders: Dict[int, int], portfolio: Any, pos_limit: Dict[str, int]):
    product = order.product
    product_limit = pos_limit[product]
    limit_price = order.price
    outstanding_quantity = order.quantity
    for pricepoint in sorted(buy_orders.keys(), reverse=True):
        if buy_orders[pricepoint] > 0:
            if pricepoint <= order.price:
                fulfilled_amount = min(int(product_limit + portfolio.quantity.get(product, 0)), -outstanding_quantity, buy_orders[pricepoint]) #quantity before order limit, order quantity remaining, quantity avaliable, 
                
                # Update portfolio
                portfolio.quantity[product] -= fulfilled_amount
                buy_orders[pricepoint] -= fulfilled_amount
                portfolio.cash += fulfilled_amount * buy_orders[pricepoint]

                outstanding_quantity += fulfilled_amount
                #print(f"selling {fulfilled_amount} at {buy_prices[i]}")
        
            if outstanding_quantity == 0 or pricepoint < limit_price:
                break