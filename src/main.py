#!/usr/bin/env python3

import os
from datetime import datetime
from fuzzworks_call import fuzzworks_call
from preferences import save_preferences, load_preferences
from db_middleware import (
    create_live_table,
    create_historical_table,
    post_historical_data,
    drop_db,
)
from db_middleware import get_historical_item, get_db_size
from mokaam_call import mokaam_call
# from discordInit import bot_init


# Magic paths etc live here
historical_db = "historical.db"
live_db = "live.db"
preferences = "preferences.ini"

data_folder = "./data/"

historical_db_path = os.path.join(data_folder, historical_db)
live_db_path = os.path.join(data_folder, live_db)
preference_path = os.path.join(data_folder, preferences)

os.makedirs(data_folder, exist_ok=True)


# End of magic values
#
def init():
    if not os.path.exists(preference_path):
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
        save_preferences(preference_path, preferences)
        print("Preferences created")
    else:
        try:
            load_preferences(preference_path)
        except:
            # TK this needs to be narrowed down to a smaller error size
            # The specific error I was thinikng of was when you have a
            # preferences file but it has wrong values
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
            save_preferences(preference_path, preferences)
        print("Preferences created")

        print("Preferences loaded.")


def startup_databases():
    if not os.path.exists(live_db_path):
        print("Unable to find live table, now creating")
        create_live_table()
    else:
        print("Live table found. Clearing live table data.")
        drop_db(live_db_path, "live_db")
        create_live_table()
        print("Live table cleared.")
    if not os.path.exists(historical_db_path):
        print("Unable to find historical table, now creating")
        create_historical_table()
    else:
        print("Historical table found. Clearing historical table data.")
        drop_db(historical_db_path, "historical_db")
        create_historical_table()
        print("Historical table cleared.")


def create_historical_database():
    timestamp = "./data/lastrun.txt"
    today = datetime.now().date()
    if os.path.exists(timestamp):
        with open(timestamp, "r") as file:
            last_run_date = file.read().strip()
            if last_run_date == str(today):
                print("Price history data is already up-to-date.")
                return
    else:
        with open(timestamp, "w") as file:
            file.write(str(today))

    res = mokaam_call()
    if res.error is not None:
        raise Exception(f"{res.error}")
    for key in res.response:
        # We need to call the insert val into database here
        # TK this needs to be batched in a loop into an object and then post to the db all at once.
        print(f"{res.response[key].as_post_data()}")
        post_historical_data(historical_db_path, **res.response[key].as_post_data())

    with open(timestamp, "w") as file:
        file.write(str(today))


# def create_live_database():
#     res = fuzzworks_call()
#     if res.error is not None:
#         raise Exception(f"{res.error}")
#     for key in res.response:
#         # We need to call the insert val into database here
#         # TK this needs to be batched in a loop into an object and then post to the db all at once.
#         print(f"{res.response[key].as_post_data()}")
#         post_historical_data(live_db_path, **res.response[key].as_post_data())


def __main__():
    init()
    startup_databases()
    create_historical_database()
    create_live_database()
    historical_size = get_db_size(historical_db_path, "historical_db")
    for i in range(0, historical_size):
        res = get_historical_item(i)
        if res != "Not Found":
            print(res)
    print("Hello, world")


if __name__ == "__main__":
    __main__()
