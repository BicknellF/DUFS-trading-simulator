def match_order(order, orderbook, portfolio, product, pos_limit):
    if order.quantity > 0:
        match_buy_order(order, orderbook[1], portfolio, product, pos_limit[product])
    elif order.quantity < 0:
        match_sell_order(order, orderbook[0], portfolio, product, pos_limit[product])
    else:
        pass

def match_buy_order(order, sell_orders, portfolio, product, product_limit):
    limit_price = order.price
    outstanding_quantity = order.quantity
    for pricepoint in sell_orders:
        if sell_orders[pricepoint] > 0:
            if pricepoint >= order.price:
                fulfilled_amount = min(int(product_limit - portfolio.quantity.get(product, 0)), outstanding_quantity, sell_orders[pricepoint]) #quantity before order limit, order quantity remaining, quantity avaliable, 
                portfolio.quantity[product] -= fulfilled_amount
                sell_orders[pricepoint] -= fulfilled_amount
                portfolio.cash -= fulfilled_amount * sell_orders[pricepoint]
                outstanding_quantity -= fulfilled_amount
                #print(f"selling {fulfilled_amount} at {buy_prices[i]}")
        
            if outstanding_quantity == 0 or pricepoint < limit_price:
                break
    

def match_sell_order(order, buy_orders, portfolio, product, product_limit):
    limit_price = order.price
    outstanding_quantity = order.quantity
    for pricepoint in buy_orders:
        if buy_orders[pricepoint] > 0:
            if pricepoint <= order.price:
                fulfilled_amount = min(int(product_limit + portfolio.quantity.get(product, 0)), -outstanding_quantity, buy_orders[pricepoint]) #quantity before order limit, order quantity remaining, quantity avaliable, 
                portfolio.quantity[product] -= fulfilled_amount
                buy_orders[pricepoint] -= fulfilled_amount
                portfolio.cash += fulfilled_amount * buy_orders[pricepoint]
                outstanding_quantity += fulfilled_amount
                #print(f"selling {fulfilled_amount} at {buy_prices[i]}")
        
            if outstanding_quantity == 0 or pricepoint < limit_price:
                break