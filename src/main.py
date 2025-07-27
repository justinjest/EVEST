#!/usr/bin/env python3

import os
from datetime import datetime
from time import sleep
from fuzzworks_call import fuzzworks_call
from preferences import save_preferences, load_preferences
from db_middleware import *
from db_middleware import get_historical_item, get_db_size
from mokaam_call import mokaam_call
from buy_list import create_buy_list
from buy_list import flag_create
from sell_list import create_sell_list
from typeids import lookup_type_id
from profit_tracker import Player, create_transaction_database
from set_preferences import setup_preferences
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
transaction_db_path = os.path.join(data_folder, transactions)

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
    timestamp_hist = "./data/lastrun_hist.txt"
    timestamp_live = "./data/lastrun_live.txt"

    update_dbs()

    # Transaction startup
    if not os.path.exists(transaction_db_path):
        print("Unable to find transaction table, now creating")
        create_transaction_database(transaction_db_path)
    else:
        print("Clearing transaction table data.")
        drop_db(transaction_db_path, "transaction_db")
        create_transaction_database(transaction_db_path)
        print("Transaction table cleared.")

def loop(p):
    print("Flag create")
    buy, sell = flag_create()
    print("udpate dbs")
    update_dbs()
    print("Update player")
    update_player(buy, sell, p)
    print_player(p)
    print("Update order_sheet")
    output_order_sheet(buy, sell)

def output_order_sheet(buy, sell):
    print("Buy")
    for i in buy:
        print(f"{lookup_type_id(i)}")
    print("Sell")
    for i in sell:
        print(f"{lookup_type_id(i)}")

def update_player(buy, sell, p):
    for i in buy:
        data = get_live_item(i)
        p.buy_item(i, data["buy_weighted_average"])
    for i in sell:
        data = get_live_item(i)
        p.sell_item(i, data["sell_weighted_average"])

def print_player(p):
    print(f"User currently has: {round(p.funds, 2)} isk")
    items = p.items
    for item in items:
        print(f"{lookup_type_id(item)}")
        print(f"Avg buy price: {round(items[item][0], 2)}")
        print(f"Num in inventory: {items[item][1]}")

def main():
    setup_preferences()
    init()
    startup_databases()
    p = Player()
    print("Import complete")
    print("In main loop")
    while True:
        loop(p)
        sleep(60*30)

if __name__ == "__main__":
    main()
