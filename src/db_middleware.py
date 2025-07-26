#!/usr/bin/env python3

# Create db
# Create db schema
# Delete db
# Update db
# Select from db
#

import sqlite3
import datetime
'''
CREATE TABLE IF NOT EXISTS {database_name} (\n{database_scheme});
'''
def create_db(database_name, database_scheme):
    schema = f"CREATE TABLE IF NOT EXISTS {database_name}(\n{database_scheme});"
    print(schema)
    try:
        with sqlite3.connect(database_name) as conn:
            print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
            cursor = conn.cursor()
            cursor.execute(schema)
            conn.commit()
            print("Table created succesfully")

    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

def drop_db(database_name):
    schema = f"DROP TABLE IF EXISTS {database_name}"
    try:
        with sqlite3.connect(database_name) as conn:
            with sqlite3.connect(database_name) as conn:
                cursor = conn.cursor()
                cursor.execute(schema)
                conn.commit()
                print("Table dropped")
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

def post_live_data(item_num, lowest_price,
                         highest_price, buy_vol, sell_vol):
    schema = f"""INSERT INTO live_db(item_num, lowest_price, highest_price, last_updated, buy_vol, sell_vol)
    VALUES({item_num},{lowest_price},{highest_price},'{datetime.datetime.now()}',{buy_vol},{sell_vol})"""
    print(schema)
    try:
        with sqlite3.connect("live_db") as conn:
            with sqlite3.connect("live_db") as conn:
                cursor = conn.cursor()
                cursor.execute(schema)
                conn.commit()
                print("Table updated")
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

def post_historical_data(item_num, avg_price, avg_vol):
    schema = f"""INSERT INTO historical_db(item_num, avg_price, avg_vol, last_updated)
    VALUES({item_num},{avg_price},{avg_vol},'{datetime.datetime.now()}')"""
    print(schema)
    try:
        with sqlite3.connect("historical_db") as conn:
            with sqlite3.connect("historical_db") as conn:
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
    create_db("live_db", live_scheme)

def create_historical_table():
    historical_scheme= """
    id INTEGER PRIMARY KEY,
    item_num INTEGER NOT NULL,
    avg_price FLOAT,
    avg_vol FLOAT,
    last_updated DATETIME"""
    create_db("historical_db", historical_scheme)

if __name__ == "__main__":
    # Historic_price db
    drop_db("historical_db")
    drop_db("live_db")

    create_live_table()
    create_historical_table()
    post_live_data(0, 0.0, 0.0, 0, 0)
    post_live_data(1, 0.0, 0.0, 0, 0)
    post_live_data(2, 0.0, 0.0, 0, 0)
    post_historical_data(0, 0.0, 0.0)
    post_historical_data(1, 0.0, 0.0)
    post_historical_data(2, 0.0, 0.0)
