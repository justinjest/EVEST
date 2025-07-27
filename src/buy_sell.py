#!/usr/bin/env python3
#
import sqlite3
from preferences import get_preference
from typeids import lookup_type_id
from db_middleware import get_live_item, get_historical_item

historical_db_path = "./data/historical.db"
live_db_path = "./data/live.db"
preference_path = "./data/preference.ini"


def get_live_data():
    request = f"SELECT typeid, buy_weighted_average from live_db"
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


def process_data_to_array(vals):
    val = []
    for i in vals:
        val.append(i[0])
    return val


def flag_create():
    sales_tax = float(get_preference("sales_tax"))
    buy_fee = float(get_preference("buy_broker_fee"))
    sell_fee = float(get_preference("sell_broker_fee"))

    item_ids = process_data_to_array(get_live_data())
    buy = []
    sell = []
    for typeid in item_ids:
        historical = get_historical_item(typeid)
        live = get_live_item(typeid)
        avg_price = historical["avg_price_month"]
        std_dev = historical["std_dev_month"]
        avg_spread = historical["spread_month"]
        avg_vol = historical["vol_week"] / 7

        spread = float(live["sell_min"]) - float(live["buy_weighted_average"])
        buy_avg = live["buy_weighted_average"]
        sell_avg = live["sell_weighted_average"]
        buy_flag = (
            float(buy_avg * (1.0 + buy_fee)) < avg_price - std_dev
            and spread > avg_spread
            and float(live["buy_volume"]) > avg_vol
            and float(live["buy_stddev"]) < std_dev * 1.5
        )

        sell_flag = (
            float(sell_avg * (1.0 - sell_fee - sales_tax)) > avg_price + std_dev
            and spread > avg_spread
            and float(live["sell_volume"]) > avg_vol
            and float(live["sell_stddev"]) < std_dev * 1.5
        )

        if buy_flag and sell_flag:
            continue

        if buy_flag:
            buy.append(live["typeid"])

        if sell_flag:
            sell.append(live["typeid"])

    return buy, sell


def output_order_sheet(buy, sell):
    print("=========BUY OPPORTUNITIES=========")
    for i in buy:
        print(f"{lookup_type_id(i)}")
    print("=========SELL OPPORTUNITIES=========")
    for i in sell:
        print(f"{lookup_type_id(i)}")
