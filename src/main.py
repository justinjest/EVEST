#!/usr/bin/env python3

import os
from preferences import save_preferences, load_preferences

if not os.path.exists("../data/preferences.ini"):
    preferences = {
        "region_id": "10000002",
        "station_id": "30000142",
        "time": "month",
        "market_size": "1000000000",
        "market_volume": "300",
    }
    save_preferences("../data/preferences.ini", preferences)
else:
    print("Preferences loaded.")


def __main__():
    print("Hello, world")
