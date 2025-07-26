#!/usr/bin/env python3

import sqlite3
from preferences import get_preference

historical_db_path = "./data/historical.db"
live_db_path = "./data/live.db"
preference_path = "./data/preference.ini"


def get_mokaam_data():
    time = get_preference("time")
    request = f"SELECT typeid, avg_price_{time} from historical_db"

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

def process_data(vals):
    val = {}
    for i in vals:
        val[i[0]]= i[1]
    return val

def create_buy_list():
    his_data = process_data(get_mokaam_data())
    liv_data = process_data(get_live_data())
    buy_list = []
    for i in liv_data.keys():
        if i in his_data:
            if liv_data[i] < his_data[i] * 0.90:
                buy_list.append(i)
                print(f"Buy: {i} price: {his_data[i] / liv_data[i]}")
    return buy_list

if __name__ == "__main__":
    buy_list = create_buy_list()
    print(buy_list)
