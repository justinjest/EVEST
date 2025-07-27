#!/usr/bin/env python3

import sqlite3
from preferences import get_preference

from db_middleware import get_live_item, get_historical_item

historical_db_path = "./data/historical.db"
live_db_path = "./data/live.db"
preference_path = "./data/preference.ini"


def get_mokaam_data():
    time = get_preference("time")
    request = f"SELECT typeid, low_{time} from historical_db"

    try:
        with sqlite3.connect(historical_db_path) as conn:
            cursor = conn.cursor()
            res = cursor.execute(request)
            row = res.fetchall()
            if row:
                return row
            else:
                return "Not found"
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

def get_live_data():
    request = f"SELECT typeid from live_db"

    try:
        with sqlite3.connect(live_db_path) as conn:
            cursor = conn.cursor()
            res = cursor.execute(request)
            row = res.fetchall()
            if row:
                return row
            else:
                return "Not found"
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

def process_data(vals):
    val = {}
    for i in vals:
        print(i)
        val[i[0]]= i[1]
    return val

def process_data_to_array(vals):
    val = []
    for i in vals:
        val.append(i[0])
    return val

def create_buy_list():
    tmp = get_mokaam_data()
    his_data = process_data(tmp)
    tmp = get_live_data()
    liv_data = process_data(tmp)
    buy_list = []
    for i in liv_data.keys():
        if i in his_data:
            if liv_data[i] < his_data[i] * 0.85:
                buy_list.append(i)
    return buy_list

def flag_create():
    item_ids = process_data_to_array(get_live_data())
    buy = []
    sell = []
    for typeid in item_ids:
        historical = get_historical_item(typeid)
        live = get_live_item(typeid)
        # Historical references
        avg_price = historical["avg_price_month"]
        std_dev = historical["std_dev_month"]
        avg_spread = historical["spread_month"]
        avg_vol = historical["vol_week"] / 7

        spread = float(live["sell_min"]) - float(live["buy_weighted_average"])

        buy_flag = (
            float(live["buy_weighted_average"]) < avg_price - std_dev and
            spread > avg_spread and
            float(live["buy_volume"]) > avg_vol and
            float(live["buy_stddev"]) < std_dev * 1.5
        )

        sell_flag = (
            float(live["sell_weighted_average"]) > avg_price + std_dev and
            float(live["sell_weighted_average"]) - float(live["buy_max"]) > avg_spread and
            float(live["sell_volume"]) > avg_vol and
            float(live["sell_stddev"]) < std_dev * 1.5
        )

        if buy_flag:
            buy.append(typeid)

        if sell_flag:
            sell.append(typeid)
    print(f"Buy: {buy}")
    print(f"Sell: {sell}")

if __name__ == "__main__":
    flag_create()
    buy_list = create_buy_list()
    print(buy_list)
