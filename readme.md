# Durham University Finance Society trading simulator

This project aims to aid the education of DUFS Quant Fund members in financial markets by providing users an OOP environment to create strategies and test them on artificial market data.

Please pip install all the packages if your IDE tells you to.

To backtest your strategy, run main.py after writing your algo in examplealgo.py


### Accessing Market Data:
Each product has an order book, this will change every timestep. To access the order book for `Underlying`, the code would be as follows
```
state.orderbook[product] # dict of buy order book dict and sell order book dict
state.orderbook[product]["BUY"] # dict of buy orders in the form {price: quantity}
state.orderbook[product]["SELL"] # dict of sell orders in the form {price: quantity}
```

### Sending orders:
On each timestep, `Trader.run()` returns a list of orders. Each order in this list is an object of the class `Order`. The `Order` class requires a product, price, and quantity in the form `Order(product, price, quantity)`. Orders are "bids" (buying) when the quantity is positive, or "asks" (selling) when the quantity is negative. e.g to place an order to buy 1 unit of a call option at price 10, you should create an Order using `Order("Call", 10, 1)`.
