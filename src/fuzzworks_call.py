#!/usr/bin/env python3

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

    time = get_preference("time", "./data/preferences.ini")
    print(time)
    cursor.execute(f"SELECT typeid FROM historical_db;")

    typeids = cursor.fetchall()

    conn.close()

    typeid_list = [(row[0]) for row in typeids]

    return typeid_list


def fuzzworks_call() -> Response:
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
        temparray = clean_type_ids[o : o + chunk_size]
        time.sleep(0.1)
        types = ",".join(map(str, temparray))
        api_url = api_url_base + types

        print(f"Pulling Fuzzwork API for station {station_id} with type_ids: {types}")

        response = requests.get(api_url)

        if response.status_code == 200:
            try:
                raw_data = response.json()
                print("Received raw JSON data")
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
                    print("Added data to dictionary")
                else:
                    print("Raw data is not a dictionary")
                    res.error = "Unexpected response format"
                    return res
            except json.JSONDecodeError as e:
                print("Failed to parse JSON response:", e)
                res.error = str(e)
                return res

    if all_data:
        for item in all_data:
            print(f"typeid: {item['typeid']} (type: {type(item['typeid'])})")
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
            print(f"Validated data has been written to {output_json}")
        except Exception as e:
            print("Validation error:", e)
            res.error = str(e)

    return res


if __name__ == "__main__":
    dat = get_typeids_as_list(historical_db_path)
    print(dat)
    res = fuzzworks_call()
    print(res)
    print(res.get_val())

