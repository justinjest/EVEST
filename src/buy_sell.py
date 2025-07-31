#!/usr/bin/env python3
#
import sqlite3
from preferences import get_preference
from typeids import lookup_type_id
from db_middleware import get_live_item, get_historical_item

historical_db_path = "./data/historical.db"
live_db_path = "./data/live.db"
preference_path = "./data/preference.ini"


def get_type_ids():
    request = "SELECT typeid from historical_db"
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


def process_data_to_array(vals):
    val = []
    for i in vals:
        val.append(i[0])
    return val


def flag_create():
    sales_tax = float(get_preference("sales_tax"))
    buy_fee = float(get_preference("buy_broker_fee"))
    sell_fee = float(get_preference("sell_broker_fee"))

    # Column names
    timeframe = get_preference("time")
    avg_min_col = f"low_{timeframe}"
    avg_max_col = f"high_{timeframe}"
    std_dev_col = f"std_dev_{timeframe}"
    avg_spread_col = f"spread_{timeframe}"

    item_ids = process_data_to_array(get_type_ids())
    buy = []
    sell = []
    for typeid in item_ids:
        historical = get_historical_item(typeid)
        live = get_live_item(typeid)
        hist_std_dev = historical[std_dev_col]
        hist_spread = historical[avg_spread_col]
        hist_sell = historical[avg_max_col]
        hist_buy = historical[avg_min_col]

        spread = float(live["sell_percentile"]) - float(live["buy_percentile"])
        buy_pct_now = live["buy_percentile"]
        sell_pct_now = live["sell_percentile"]
        buy_flag = (
            float(buy_pct_now * (1.0 + buy_fee)) < (hist_buy - hist_std_dev) * 0.9
            and spread > hist_spread
            and float(live["buy_stddev"]) < (hist_std_dev * 1.5)
            and float(live["buy_volume"]) > (float(live["sell_volume"]) / 5)
            and (
                sell_pct_now * (1.0 - sell_fee - sales_tax)
                - buy_pct_now * (1.0 + buy_fee)
            )
            / buy_pct_now
            * 100
            > 5.0
        )

        sell_flag = (
            float(sell_pct_now * (1.0 - sell_fee - sales_tax))
            >= (hist_sell + hist_std_dev) * 1.2
            and spread > hist_spread
            and float(live["sell_volume"]) > (float(live["buy_volume"]) / 5)
        )

        if buy_flag and sell_flag:
            continue

        if buy_flag:
            buy.append(live["typeid"])

        if sell_flag:
            sell.append(live["typeid"])

    return buy, sell


def output_order_sheet(buy, sell):
    buy_names = []
    sell_names = []
    print("=========BUY OPPORTUNITIES=========")
    for i in buy:
        name = lookup_type_id(i)
        print(f"{name}")
        buy_names.append(name)
    print("\n=========SELL OPPORTUNITIES=========")
    for i in sell:
        name = lookup_type_id(i)
        print(f"{name}")
        sell_names.append(name)

    return buy_names, sell_names
