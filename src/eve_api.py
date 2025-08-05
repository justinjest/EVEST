#!/usr/bin/env python3

import requests
import json
from secret import eveToken, charToken


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


import requests

def create_db(database_path, table_name, database_scheme):
    schema = f"CREATE TABLE IF NOT EXISTS {table_name}(\n{database_scheme});"
    try:
        with sqlite3.connect(database_path) as conn:
            cursor = conn.cursor()
            cursor.execute(schema)
            conn.commit()
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)


if __name__ == "__main__":
    create_db("./data/test.db", "test", scheme)

url = "https://esi.evetech.net/markets/10000003/orders"

querystring = {"order_type":"buy"}

headers = {
"Accept-Language": "",
"If-None-Match": "",
"X-Compatibility-Date": "2020-01-01",
"X-Tenant": "",
"Accept": "application/json"
}
data = []
response = requests.get(url, headers=headers, params=querystring)
if response.status_code == 200:
    raw_data = response.json()
    if not raw_data:
        print("Raw data is empty")

    for json in raw_data:
        data.append(json)
    print(data)
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

    insert_sql = """INSERT INTO test (
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
