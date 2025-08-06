#!/usr/bin/env python3

from api_middleware import retry_api_call
import requests
import json
import sqlite3
import time
from preferences import get_preference
from pydantic import BaseModel, TypeAdapter
from typing import Optional, Any
from datetime import date

historical_db_path = "./data/historical.db"


class MarketStats(BaseModel):
    weightedAverage: float
    max: float
    min: float
    stddev: float
    median: float
    volume: float
    orderCount: int
    percentile: float


class BuySellStats(BaseModel):
    typeid: int
    buy: MarketStats
    sell: MarketStats

    def as_post_data(self) -> dict:
        return build_live_post_data(self)


def build_live_post_data(stats: BuySellStats) -> dict:
    return {
        "typeid": stats.typeid,
        "buyWeightedAverage": stats.buy.weightedAverage,
        "buyMax": stats.buy.max,
        "buyMin": stats.buy.min,
        "buyStdDev": stats.buy.stddev,
        "buyMedian": stats.buy.median,
        "buyVolume": stats.buy.volume,
        "buyOrderCount": stats.buy.orderCount,
        "buyPercentile": stats.buy.percentile,
        "sellWeightedAverage": stats.sell.weightedAverage,
        "sellMax": stats.sell.max,
        "sellMin": stats.sell.min,
        "sellStdDev": stats.sell.stddev,
        "sellMedian": stats.sell.median,
        "sellVolume": stats.sell.volume,
        "sellOrderCount": stats.sell.orderCount,
        "sellPercentile": stats.sell.percentile,
    }


class Response:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error

    def get_val(self):
        if self.error is not None:
            return self.error
        if self.response is not None:
            return self.response
        # Neither an error or a response, must be handlded
        raise Exception("InvalidResponse")


def get_typeids_as_list(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"SELECT typeid FROM historical_db;")

    typeids = cursor.fetchall()

    conn.close()

    typeid_list = [(row[0]) for row in typeids]

    return typeid_list


@retry_api_call()
def fuzzworks_call() -> Response:
    print("Pulling live data...")
    res = Response()
    station_id = get_preference("station_id")

    typeid_list = get_typeids_as_list(historical_db_path)
    clean_type_ids = list(set(typeid_list))  # Remove duplicates

    api_url_base = (
        f"https://market.fuzzwork.co.uk/aggregates/?station={station_id}&types="
    )
    chunk_size = 100

    all_data = []

    for o in range(0, len(clean_type_ids), chunk_size):
        temparray = clean_type_ids[o : min((o + chunk_size), len(typeid_list))]
        time.sleep(0.001)
        types = ",".join(map(str, temparray))
        api_url = api_url_base + types

        response = requests.get(api_url)

        if response.status_code == 200:
            try:
                raw_data = response.json()
                if not raw_data:
                    print("Raw data is empty")
                    res.error = "Empty response from API"
                    return res

                if isinstance(raw_data, dict):
                    for typeid, stats in raw_data.items():
                        all_data.append(
                            {
                                "typeid": int(typeid),  # Convert typeid to integer
                                "buy": stats["buy"],
                                "sell": stats["sell"],
                            }
                        )
                else:
                    print("Raw data is not a dictionary")
                    res.error = "Unexpected response format"
                    return res
            except json.JSONDecodeError as e:
                print("Failed to parse JSON response:", e)
                res.error = str(e)
                return res

    if all_data:
        adapter = TypeAdapter(dict[int, BuySellStats])
        try:
            res.response = adapter.validate_python(
                {item["typeid"]: item for item in all_data}
            )
            output_json = "./data/fuzzworks.json"
            with open(output_json, "w") as outfile:
                json.dump(
                    {item["typeid"]: item for item in all_data}, outfile, indent=4
                )
        except Exception as e:
            print("Validation error:", e)
            res.error = str(e)

    print("Live data loaded!")
    return res


if __name__ == "__main__":
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
