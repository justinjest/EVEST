#!/usr/bin/env python3

import sqlite3
import datetime
import os

"""
CREATE TABLE IF NOT EXISTS {database_name} (\n{database_scheme});
"""
historical_db = "historical.db"
live_db = "live.db"
data_folder = "./data/"
historical_db_path = os.path.join(data_folder, historical_db)
live_db_path = os.path.join(data_folder, live_db)

os.makedirs(data_folder, exist_ok=True)


def create_db(database_path, table_name, database_scheme):
    schema = f"CREATE TABLE IF NOT EXISTS {table_name}(\n{database_scheme});"
    print(schema)
    try:
        with sqlite3.connect(database_path) as conn:
            print(
                f"Opened SQLite database with version {sqlite3.sqlite_version} successfully."
            )
            cursor = conn.cursor()
            cursor.execute(schema)
            conn.commit()
            print("Table created successfully")
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)


def drop_db(database_path, table_name):
    schema = f"DROP TABLE IF EXISTS {table_name}"
    try:
        with sqlite3.connect(database_path) as conn:
            cursor = conn.cursor()
            cursor.execute(schema)
            conn.commit()
            print("Table dropped")
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)


def post_live_data(
    live_db_path, item_num, lowest_price, highest_price, buy_vol, sell_vol
):
    schema = f"""INSERT INTO live_db(item_num, lowest_price, highest_price, last_updated, buy_vol, sell_vol)
    VALUES({item_num},{lowest_price},{highest_price},'{datetime.datetime.now()}',{buy_vol},{sell_vol})"""
    print(schema)
    try:
        with sqlite3.connect(live_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(schema)
            conn.commit()
            print("Table updated")
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)


def post_historical_data(historical_db_path, item_num, avg_price, avg_vol):
    schema = f"""INSERT INTO historical_db(item_num, avg_price, avg_vol, last_updated)
    VALUES({item_num},{avg_price},{avg_vol},'{datetime.datetime.now()}')"""
    print(schema)
    try:
        with sqlite3.connect(historical_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(schema)
            conn.commit()
            print("Table updated")
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)


def create_live_table():
    live_scheme = """id INTEGER PRIMARY KEY,
    item_num INTEGER NOT NULL,
    lowest_price FLOAT,
    highest_price FLOAT,
    last_updated DATETIME,
    buy_vol INTEGER,
    sell_vol INTEGER"""
    create_db(live_db_path, "live_db", live_scheme)


def create_historical_table():
    historical_scheme = """
    id INTEGER PRIMARY KEY,
    item_num INTEGER NOT NULL,
    avg_price FLOAT,
    avg_vol FLOAT,
    last_updated DATETIME"""
    create_db(historical_db_path, "historical_db", historical_scheme)


if __name__ == "__main__":
    drop_db(historical_db_path, "historical_db")
    drop_db(live_db_path, "live_db")

    create_live_table()
    create_historical_table()
    post_live_data(live_db_path, 0, 0.0, 0.0, 0, 0)
    post_live_data(live_db_path, 1, 0.0, 0.0, 0, 0)
    post_live_data(live_db_path, 2, 0.0, 0.0, 0, 0)
    post_historical_data(historical_db_path, 0, 0.0, 0.0)
    post_historical_data(historical_db_path, 1, 0.0, 0.0)
    post_historical_data(historical_db_path, 2, 0.0, 0.0)
