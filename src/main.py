#!/usr/bin/env python3

import os
from preferences import save_preferences, load_preferences
from db_middleware import create_live_table, create_historical_table

def init():
    if not os.path.exists("./data/preferences.ini"):
        preferences = {
            "region_id": "10000002",
            "station_id": "30000142",
            "time": "month",
            "market_size": "1000000000",
            "market_volume": "300",
            "sales_tax": "0.033",
            "buy_broker_fee": "0.015",
            "sell_broker_fee": "0.015",
        }
        save_preferences("./data/preferences.ini", preferences)
        print("Preferences created")
    else:
        load_preferences("./data/preferences.ini")
        print("Preferences loaded.")

def startup_databases():
    if not os.path.exists("./data/live.db"):
        print("Unable to find live table, now creating")
        create_live_table()
    else:
        print("Live table found")
    if not os.path.exists("./data/historical.db"):
        print("Unable to find historical table, now creating")
        create_historical_table()
    else:
        print("Historical table found")



def __main__():
    init()
    startup_databases()
    print("Hello, world")


if __name__ == "__main__":
    __main__()
