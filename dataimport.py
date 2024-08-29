import pandas as pd

def read_file(file_path):
    df = pd.read_csv(file_path)
    products = df["product"].unique()
    ticks = df["timestamp"].nunique()
    return products, ticks, df

def extract_orders(df, tick, product):
    row = df[df["timestamp"] == tick*100]
    row = row[row["product"] == product]
    bid_orders = {} #price:quantity 
    ask_orders = {} #price:quantity 
    for i in range(1, 4):
        price = row[f"bid_price_{i}"].iloc[0]
        bid_orders[price] = row[f"bid_volume_{i}"].iloc[0]
    for i in range(1, 4):
        price = row[f"ask_price_{i}"].iloc[0]
        ask_orders[price] = row[f"ask_volume_{i}"].iloc[0]
    
    return {"BUY": bid_orders, 
            "SELL": ask_orders}