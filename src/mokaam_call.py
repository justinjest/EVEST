#!/usr/bin/env python3

import requests
import json
import sqlite3
import os
from preferences import get_preference
from pydantic import BaseModel, Field, TypeAdapter, field_validator
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

    @field_validator("last_data", mode="before")
    @classmethod
    def parse_last_data(cls, v: Any) -> Optional[date]:
        if v in ("Null", "ERROR: 404", "ERROR: 400", None):
            return None
        try:
            return date.fromisoformat(v)
        except Exception:
            raise ValueError(f"Invalid date value: {v}")

    def as_post_data(self) -> dict:
        return build_historical_post_data(self)


def build_historical_post_data(stats: TypeStats) -> dict:
    return {
        "typeid": stats.typeid,
        "last_data": stats.last_data,
        "vol_yesterday": stats.vol_yesterday,
        "vol_week": stats.vol_week,
        "vol_month": stats.vol_month,
        "vol_quarter": stats.vol_quarter,
        "vol_year": stats.vol_year,
        "avg_price_yesterday": stats.avg_price_yesterday,
        "avg_price_week": stats.avg_price_week,
        "avg_price_month": stats.avg_price_month,
        "avg_price_quarter": stats.avg_price_quarter,
        "avg_price_year": stats.avg_price_year,
        "order_count_yesterday": stats.order_count_yesterday,
        "order_count_week": stats.order_count_week,
        "order_count_month": stats.order_count_month,
        "order_count_quarter": stats.order_count_quarter,
        "order_count_year": stats.order_count_year,
        "size_yesterday": stats.size_yesterday,
        "size_week": stats.size_week,
        "size_month": stats.size_month,
        "size_quarter": stats.size_quarter,
        "size_year": stats.size_year,
        "high_yesterday": stats.high_yesterday,
        "high_week": stats.high_week,
        "high_month": stats.high_month,
        "high_quarter": stats.high_quarter,
        "high_year": stats.high_year,
        "ab_high_yesterday": stats.ab_high_yesterday,
        "ab_high_week": stats.ab_high_week,
        "ab_high_month": stats.ab_high_month,
        "ab_high_quarter": stats.ab_high_quarter,
        "ab_high_year": stats.ab_high_year,
        "low_yesterday": stats.low_yesterday,
        "low_week": stats.low_week,
        "low_month": stats.low_month,
        "low_quarter": stats.low_quarter,
        "low_year": stats.low_year,
        "ab_low_yesterday": stats.ab_low_yesterday,
        "ab_low_week": stats.ab_low_week,
        "ab_low_month": stats.ab_low_month,
        "ab_low_quarter": stats.ab_low_quarter,
        "ab_low_year": stats.ab_low_year,
        "spread_yesterday": stats.spread_yesterday,
        "spread_week": stats.spread_week,
        "spread_month": stats.spread_month,
        "spread_quarter": stats.spread_quarter,
        "spread_year": stats.spread_year,
        "vwap_week": stats.vwap_week,
        "vwap_month": stats.vwap_month,
        "vwap_quarter": stats.vwap_quarter,
        "vwap_year": stats.vwap_year,
        "_52w_low": stats.w52_low,  # Note alias used here
        "_52w_high": stats.w52_high,
        "std_dev_week": stats.std_dev_week,
        "std_dev_month": stats.std_dev_month,
        "std_dev_quarter": stats.std_dev_quarter,
        "std_dev_year": stats.std_dev_year,
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


def mokaam_call() -> Response:
    region_id = get_preference("region_id")
    market_size = get_preference("market_size")
    market_volume = get_preference("market_volume")
    api_url = f"https://mokaam.dk/API/market/query?type=items&regionid={region_id}&query=size_month>{market_size}&query=volume_month>{market_volume}"
    res = Response()
    print(f"Pulling Mokaam API for region {region_id}")

    response = requests.get(api_url)
    print("Received data from API")
    if response.status_code == 200:
        try:
            raw_data = response.json()
            print("Received raw JSON data")
            data = {item["typeid"]: item for item in raw_data}
            print("Transformed data to dictionary")

            adapter = TypeAdapter(dict[int, TypeStats])
            try:
                res.response = adapter.validate_python(data)
                output_json = "./data/mokaam.json"
                with open(output_json, "w") as outfile:
                    json.dump(data, outfile, indent=4)
                print(f"Validated data has been written to {output_json}")
            except Exception as e:
                print("Validation error:", e)
        except json.JSONDecodeError as e:
            print("Failed to parse JSON response:", e)
    else:
        res.error = response.status_code
        print(f"Error: {response.status_code}")
    return res


if __name__ == "__main__":
    res = mokaam_call()
    val = res.get_val()
    if res.error is not None:
        raise exception("Failed to load mokaam data")
    print(f"{res.response}")
