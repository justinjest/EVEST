#!/usr/bin/env python3

import os
from preferences import save_preferences, load_preferences
from discordInit import bot_init

if not os.path.exists("./data"):
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
    save_preferences("../data/preferences.ini", preferences)
else:
    load_preferences("../data/preferences.ini")
    print("Preferences loaded.")


def __main__():
    bot_init()
    print("Hello, world")


if __name__ == __main__():
    __main__()
