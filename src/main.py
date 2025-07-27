#!/usr/bin/env python3

import os
from datetime import datetime
from time import sleep
from fuzzworks_call import fuzzworks_call
from preferences import save_preferences, load_preferences
from db_middleware import (
    create_live_table,
    create_historical_table,
    post_live_data,
    post_historical_data,
    drop_db,
    get_live_item
)
from db_middleware import get_historical_item, get_db_size
from mokaam_call import mokaam_call
from buy_list import create_buy_list
from buy_list import flag_create
from sell_list import create_sell_list
from typeids import lookup_type_id
from profit_tracker import Player, create_transaction_database

# from discordInit import bot_init


# Magic paths etc live here
historical_db = "historical.db"
live_db = "live.db"
transactions = "transactions.db"
preferences = "preferences.ini"

data_folder = "./data/"

historical_db_path = os.path.join(data_folder, historical_db)
live_db_path = os.path.join(data_folder, live_db)
preference_path = os.path.join(data_folder, preferences)
transaction_path = os.path.join(data_folder, transactions)

os.makedirs(data_folder, exist_ok=True)


# End of magic values
#
def init():
    if not os.path.exists(preference_path):
        preferences = {
            "region_id": "10000002",
            "station_id": "60003760",
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
                "station_id": "60003760",
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
    timestamp = "./data/lastrun.txt"
    today = datetime.now().date()
    # live start up
    if not os.path.exists(live_db_path):
        print("Unable to find live table, now creating")
        create_live_table()
    else:
        print("Live table found. Clearing live table data.")
        drop_db(live_db_path, "live_db")
        create_live_table()

    # Historical start up
    if not os.path.exists(historical_db_path):
        print("Unable to find historical table, now creating")
        create_historical_table()
        populate_historical_database()
        with open(timestamp, "w") as file:
            file.write(str(today))
    else:
        if os.path.exists(timestamp):
            with open(timestamp, "r") as file:
                last_run_date = file.read().strip()
                if last_run_date == str(today):
                    print("Price history data is already up-to-date.")
                    return
        else:
            print("Clearing historical table data.")
            drop_db(historical_db_path, "historical_db")
            create_historical_table()
            print("Historical table cleared.")
            with open(timestamp, "w") as file:
                file.write(str(today))
            populate_historical_database()

    # Transaction startup
    if not os.path.exists(transaction_db_path):
        print("Unable to find transaction table, now creating")
        create_transaction_database(transaction_db_path)
    else:
        print("Clearing transaction table data.")
        drop_db(transaction_db_path, "transaction_db")
        create_transaction_database(transaction_db_path)
        print("Transaction table cleared.")


def populate_historical_database():
    res = mokaam_call()
    if res.error is not None:
        raise Exception(f"{res.error}")
    for key in res.response:
        # TK this needs to be batched in a loop into an object and then post to the db all at once.
        # print(f"{res.response[key].as_post_data()}")
        post_historical_data(historical_db_path, **res.response[key].as_post_data())


def populate_live_database():
    res = fuzzworks_call()
    if res.error is not None:
        raise Exception(f"{res.error}")
    for key in res.response:
        # We need to call the insert val into database here
        # TK this needs to be batched in a loop into an object and then post to the db all at once.
        print(f"{res.response[key].as_post_data()}")
        post_live_data(live_db_path, res.response[key])

def loop(buy, sell, p):
    new_buy, new_sell = flag_create()
    print("BUY:")
    for i in buy:
        item = get_live_item(i)
        p.buy_item(i, item["buy_weighted_average"])
        print(f"{lookup_type_id(i)}")
    print("SELL:")
    for i in sell:
        item = get_live_item(i)
        p.sell_item(i, item["sell_weighted_average"])
        print(f"{lookup_type_id(i)}")
    print("User currently has: {} isk", p.funds)
    items = p.items
    for item in items:
        print(f"{lookup_type_id(item)}")
        print(f"Avg buy price{item[0]}")
        print(f"Num in inventory{item[1]}")
    if buy != new_buy:
        print("Buy")
        for i in new_buy:
            print(f"{lookup_type_id(i)}")
        buy = new_buy
    else:
        print("no new buys")
    if sell != new_sell:
        print("Sell")
        for i in new_sell:
            print(f"{lookup_type_id(i)}")
        sell = new_sell
    else:
        print("no new sells")
    print("User currently has: {} isk", p.funds)
    items = p.items
    for item in items:
        print(f"{lookup_type_id(item)}")
        print(f"Avg buy price{item[0]}")
        print(f"Num in inventory{item[1]}")

    return new_buy, new_sell

def main():
    init()
    startup_databases()
    p = Player()
    print("Import complete")
    print("In main loop")
    buy = []
    sell = []
    while True:
        drop_db(live_db_path, "live_db")
        create_live_table()
        populate_live_database()
        buy, sell = loop(buy, sell, p)
        sleep(60*30)

if __name__ == "__main__":
    main()
