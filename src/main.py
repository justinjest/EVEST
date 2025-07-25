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
    }
    save_preferences("../data/preferences.ini", preferences)
else:
    if os.path.exists("./data") == False:
        os.mkdir("./data")
        save_preferences("./data/preferences.ini", preferences)
    print("Preferences loaded.")


def __main__():

    bot_init()
    print("Hello, world")


if __name__ == __main__():
    __main__()
