#!/usr/bin/env python3

import requests
import json
import sqlite3
from preferences import get_preference
from pydantic import BaseModel, Field, parse_obj_as, validator
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
    buy: MarketStats
    sell: MarketStats


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


def get_typeids_as_string(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT typeid FROM historical_db")

    typeids = cursor.fetchall()

    conn.close()

    typeid_list = [str(row[0]) for row in typeids]
    typeid_string = ", ".join(typeid_list)

    return typeid_string


def fuzzworks_call() -> Response:
    res = Response()
    station_id = get_preference("station_id")
    type_ids = get_typeids_as_string(historical_db_path)
    print(type_ids)

    api_url = f"https://market.fuzzwork.co.uk/aggregates/?region={station_id}"

    print(f"Pulling Fuzzwork API for station {station_id}")

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        res.response = parse_obj_as(dict[int, BuySellStats], data)
        output_json = "./data/fuzzworks.json"
        with open(output_json, "w") as outfile:
            json.dump(data, outfile, indent=4)
        print(f"Data has been written to {output_json}")
    else:
        res.error = response.status_code
        print(f"Error: {response.status_code}")

    return res


if __name__ == "__main__":
    res = fuzzworks_call()
    print(res)
    print(res.get_val())

    # Your JSON as string
