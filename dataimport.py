import pandas as pd
from typing import Tuple, Dict, List

def read_file(file_path: str) -> Tuple[List[str], int, pd.DataFrame]:
    df = pd.read_csv(file_path)
    products = df["product"].unique().tolist()
    ticks = df["timestamp"].nunique()
    return products, ticks, df

def extract_orders(df: pd.DataFrame, tick: int, product: str) -> Dict[str, Dict[float, int]]:
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

def extract_bot_orders(df: pd.DataFrame, tick: int, product: str) -> Dict[str, Dict[float, int]]:
    row = df[df["timestamp"] == tick*100]
    row = row[row["product"] == product]
    bid_orders = {}  # price:quantity 
    ask_orders = {}  # price:quantity 
    
    bid_price = row["bid_price_1"].iloc[0]
    bid_volume = row["bid_volume_1"].iloc[0]
    if bid_volume > 0:
        bid_orders[bid_price] = bid_volume

    ask_price = row["ask_price_1"].iloc[0]
    ask_volume = row["ask_volume_1"].iloc[0]
    if ask_volume > 0:
        ask_orders[ask_price] = ask_volume
    
    return {"BUY": bid_orders, 
            "SELL": ask_orders}