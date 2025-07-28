#!/usr/bin/env python3

import os
from datetime import datetime
from time import sleep
from fuzzworks_call import fuzzworks_call
from preferences import save_preferences, load_preferences
from db_middleware import *
from mokaam_call import mokaam_call
from buy_sell import flag_create, output_order_sheet
from typeids import lookup_type_id
from profit_tracker import (
    Player,
    create_transaction_database,
    print_player,
    update_player,
)
from set_preferences import setup_preferences
from repl import repl_loop
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
        setup_preferences()
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


def main():
    init()
    startup_databases()
    p = Player()
    print("Import complete")
    print("In main loop")
    repl_loop(p)
if __name__ == "__main__":
    main()
