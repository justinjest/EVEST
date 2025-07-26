#!/usr/bin/env python3

import os
from preferences import save_preferences, load_preferences
from db_middleware import create_live_table, create_historical_table, post_historical_data
from mokaam_call import mokaam_call


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
        print("Live table found")
    if not os.path.exists(historical_db_path):
        print("Unable to find historical table, now creating")
        create_historical_table()
    else:
        print("Historical table found")

def create_historical_database():
    res = mokaam_call()
    if res.error != None:
        raise Exception(f"{res.error}")
    for key in res.response:
        # We need to call the insert val into database here
        print(f"{res.response[key].as_post_data()}")
        post_historical_data(historical_db_path,
                             **res.response[key].as_post_data())

def __main__():
    init()
    startup_databases()
    create_historical_database()
    print("Hello, world")


if __name__ == "__main__":
    __main__()
