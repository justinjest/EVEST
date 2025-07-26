#!/usr/bin/env python3

import requests
import json
import sqlite3
from preferences import get_preference
from pydantic import BaseModel, Field, parse_obj_as, validator
from typing import Optional, Any
from datetime import date


class TypeStats(BaseModel):
    typeid: int
    last_data: Optional[date]

    vol_yesterday: float
    vol_week: float
    vol_month: float
    vol_quarter: float
    vol_year: float

    avg_price_yesterday: float
    avg_price_week: float
    avg_price_month: float
    avg_price_quarter: float
    avg_price_year: float

    order_count_yesterday: float
    order_count_week: float
    order_count_month: float
    order_count_quarter: float
    order_count_year: float

    size_yesterday: float
    size_week: float
    size_month: float
    size_quarter: float
    size_year: float

    high_yesterday: float
    high_week: float
    high_month: float
    high_quarter: float
    high_year: float

    ab_high_yesterday: float
    ab_high_week: float
    ab_high_month: float
    ab_high_quarter: float
    ab_high_year: float

    low_yesterday: float
    low_week: float
    low_month: float
    low_quarter: float
    low_year: float

    ab_low_yesterday: float
    ab_low_week: float
    ab_low_month: float
    ab_low_quarter: float
    ab_low_year: float

    spread_yesterday: float
    spread_week: float
    spread_month: float
    spread_quarter: float
    spread_year: float

    vwap_week: float
    vwap_month: float
    vwap_quarter: float
    vwap_year: float

    w52_low: float = Field(alias="_52w_low")
    w52_high: float = Field(alias="_52w_high")

    std_dev_week: float
    std_dev_month: float
    std_dev_quarter: float
    std_dev_year: float

    @validator("last_data", pre=True)
    def parse_last_data(cls, v: Any) -> Optional[date]:
        if v in ("Null", "ERROR: 404", "ERROR: 400", None):
            return None
        try:
            return date.fromisoformat(v)
        except Exception:
            raise ValueError(f"Invalid date value: {v}")


class Response():
    def __init__(self, response = None, error = None):
        self.response = response
        self.error = error
    def get_val(self):
        if self.error != None:
            return self.error
        if self.response != None:
            return self.response
        # Neither an error or a response, must be handlded
        raise Exception("InvalidResponse")


def mokaam_call() -> Response:
    region_id = get_preference("region_id")
    api_url = f"https://mokaam.dk/API/market/all?regionid={region_id}"
    res = Response()
    print(f"Pulling Mokaam API for region {region_id}")

    response = requests.get(api_url)
    print("Received data from api")

    if response.status_code == 200:
        data = response.json()
        res.response = parse_obj_as(dict[int, TypeStats], data)
        output_json = "./data/mokaam.json"
        with open(output_json, "w") as outfile:
            json.dump(data, outfile, indent=4)
        print(f"Data has been written to {output_json}")
    else:
        res.error = respionse.status_code
        print(f"Error: {response.status_code}")

    return res

if __name__ == "__main__":
    res = mokaam_call()
    val = res.get_val()
    if res.error != None:
        raise exception("Failed to load mokaam data")
    print(f"{res.response}")
