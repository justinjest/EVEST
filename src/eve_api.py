#!/usr/bin/env python3

import requests
import json
import sqlite3
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime as dt
from db_middleware import live_db_path, post_live_data

def eve_inventory_call():

    url = f"https://esi.evetech.net/characters/{charToken}/assets"

    headers = {
        "Accept-Language": "",
        "If-None-Match": "",
        "X-Compatibility-Date": "2020-01-01",
        "X-Tenant": "",
        "Accept": "application/json",
        "Authorization": eveToken,
    }

    response = requests.get(url, headers=headers)

    print(response.json())
    if response.status_code == 200:
        print(response.json())
    else:
        print("Unable to load data")


def return_items_at_station(station_id, eve_inventory_json):
    print(eve_inventory_json)


def create_db(database_path, table_name, database_scheme):
    schema = f"CREATE TABLE IF NOT EXISTS {table_name}(\n{database_scheme});"
    try:
        with sqlite3.connect(database_path) as conn:
            cursor = conn.cursor()
            cursor.execute(schema)
            conn.commit()
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

def get_live_data():
    print("Getting live data")
    url = "https://esi.evetech.net/markets/10000002/orders"
    headers = {
    "Accept-Language": "",
    "If-None-Match": "",
    "X-Compatibility-Date": "2020-01-01",
    "X-Tenant": "",
    "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    num_pages = response.headers.get("X-Pages", 1)
    data = response.json()

    def fetch_page(page):
        params = {"page": page}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()


    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(fetch_page, page) for page in range(2, int(num_pages) + 1)]
        for future in as_completed(futures):
            try:
                data.extend(future.result())
            except Exception as e:
                print(f"Error fetching page: {e}")

    return data

def  live_data_db(data):
    # Insert into db
    scheme = """order_id INTEGER PRIMARY KEY,
    duration INTEGER,
    is_buy_order BOOL,
    issued DATETIME,
    location_id INTEGER,
    min_volume INTEGER,
    price FLOAT,
    range INTEGER,
    system_id INTEGER,
    type_id INTEGER,
    volume_remain INTEGER,
    volume_total INTEGER
    """
    create_db("./data/test.db", "test", scheme)

    insert_sql = """INSERT OR REPLACE INTO test (
    order_id, duration, is_buy_order, issued, location_id, min_volume, price,
    range, system_id, type_id, volume_remain, volume_total
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    values = [
        (datum["order_id"],
            datum["duration"],
            datum["is_buy_order"],
            datum["issued"],
            datum["location_id"],
            datum["min_volume"],
            datum["price"],
            datum["range"],
            datum["system_id"],
            datum["type_id"],
            datum["volume_remain"],
            datum["volume_total"])
        for datum in data
    ]

    try:
        with sqlite3.connect("./data/test.db") as conn:
            cursor = conn.cursor()
            cursor.executemany(insert_sql, values)
            conn.commit()
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

def generate_sell(df):
    grouped = df.groupby('type_id')
    summary = grouped.agg(
       sell_max=('price', 'max'),
       sell_min=('price', 'min'),
       sell_vwap=('price', lambda x: (x * df.loc[x.index, 'volume_remain']).sum() / df.loc[x.index, 'volume_remain'].sum()),
       sell_median=('price', 'median'),
       sell_stddev=('price', 'std'),
       sell_volume=('volume_remain', 'sum'),
       sell_order_count=('price', 'count')
   )

    def compute_5_percent_avg(group):
        group = group.sort_values(by='price', ascending=True)
        total_volume = group['volume_remain'].sum()
        cutoff = total_volume * 0.05

        cum_volume = 0
        weighted_total = 0
        prices = group['price'].values
        volumes = group['volume_remain'].values

        for price, volume in zip(prices, volumes):
            if cum_volume + volume <= cutoff:
                weighted_total += price * volume
                cum_volume += volume
            else:
                remaining = cutoff - cum_volume
                weighted_total += price * remaining
                break

        return weighted_total / cutoff if cutoff > 0 else None

    five_percent_sell_avg = grouped.apply(compute_5_percent_avg, include_groups=False)
    five_percent_sell_avg.name = "five_percent_sell_avg"

    # Combine
    final_df = pd.concat([summary, five_percent_sell_avg], axis=1)
    return final_df


def generate_buy(df):
    grouped = df.groupby('type_id')
    summary = grouped.agg(
       buy_max=('price', 'max'),
       buy_min=('price', 'min'),
       buy_vwap=('price', lambda x: (x * df.loc[x.index, 'volume_remain']).sum() / df.loc[x.index, 'volume_remain'].sum()),
       buy_median=('price', 'median'),
       buy_stddev=('price', 'std'),
       buy_volume=('volume_remain', 'sum'),
       buy_order_count=('price', 'count')
   )


    def compute_5_percent_avg(group):
        group = group.sort_values(by='price', ascending=False)
        total_volume = group['volume_remain'].sum()
        cutoff = total_volume * 0.05

        cum_volume = 0
        weighted_total = 0
        prices = group['price'].values
        volumes = group['volume_remain'].values

        for price, volume in zip(prices, volumes):
            if cum_volume + volume <= cutoff:
                weighted_total += price * volume
                cum_volume += volume
            else:
                remaining = cutoff - cum_volume
                weighted_total += price * remaining
                break

        return weighted_total / cutoff if cutoff > 0 else None

    five_percent_buy_avg = grouped.apply(compute_5_percent_avg, include_groups=False)
    five_percent_buy_avg.name = "five_percent_buy_avg"

    # Combine
    final_df = pd.concat([summary, five_percent_buy_avg], axis=1)
    return final_df

def generate_buy_sell(data: json):
   df = pd.DataFrame(data)
   buy_data = df[(df['is_buy_order'] == True)]
   sell_data = df[(df['is_buy_order'] == False)]
   buy = generate_buy(buy_data)
   sell = generate_sell(sell_data)
   buy_sell = buy.join(sell)
   conn = sqlite3.connect(live_db_path)
   buy_sell.to_sql('orders', conn, if_exists='replace', index=True)
   conn.close()


if __name__ == "__main__":
    start_api = dt.now()
    data = get_live_data()
    print("Time elapsed for api: ", dt.now() - start_api)
    start_db = dt.now()
    live_data_db(data)
    print("DB insertion: ", dt.now() - start_db)
    generate_buy_sell(data)
    print("Total: ", dt.now() - start_api)
