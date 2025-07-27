#!/usr/bin/env python3

import sqlite3
from datetime import datetime, timedelta, timezone
from functools import wraps
import os
import time
from fuzzworks_call import BuySellStats, fuzzworks_call
from mokaam_call import mokaam_call
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
    try:
        with sqlite3.connect(database_path) as conn:
            cursor = conn.cursor()
            cursor.execute(schema)
            conn.commit()
            print(f"Table {table_name} created successfully")
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)


def drop_db(database_path, table_name):
    schema = f"DROP TABLE IF EXISTS {table_name}"
    try:
        with sqlite3.connect(database_path) as conn:
            cursor = conn.cursor()
            cursor.execute(schema)
            conn.commit()
            print(f"Table {table_name} dropped")
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)


def post_live_data(live_db_path, stats: BuySellStats):
    schema = f"""INSERT INTO live_db(
        typeid, buy_weighted_average, buy_max, buy_min, buy_stddev, buy_median, 
        buy_volume, buy_order_count, buy_percentile, sell_weighted_average, 
        sell_max, sell_min, sell_stddev, sell_median, sell_volume, sell_order_count, 
        sell_percentile
    ) VALUES (
        {stats.typeid}, {stats.buy.weightedAverage}, {stats.buy.max}, {stats.buy.min}, {stats.buy.stddev}, 
        {stats.buy.median}, {stats.buy.volume}, {stats.buy.orderCount}, {stats.buy.percentile},
        {stats.sell.weightedAverage}, {stats.sell.max}, {stats.sell.min}, {stats.sell.stddev}, 
        {stats.sell.median}, {stats.sell.volume}, {stats.sell.orderCount}, {stats.sell.percentile}
    )"""
    try:
        with sqlite3.connect(live_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(schema)
            conn.commit()
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)


def post_historical_data(
    historical_db_path,
    typeid,
    last_data,
    vol_yesterday,
    vol_week,
    vol_month,
    vol_quarter,
    vol_year,
    avg_price_yesterday,
    avg_price_week,
    avg_price_month,
    avg_price_quarter,
    avg_price_year,
    order_count_yesterday,
    order_count_week,
    order_count_month,
    order_count_quarter,
    order_count_year,
    size_yesterday,
    size_week,
    size_month,
    size_quarter,
    size_year,
    high_yesterday,
    high_week,
    high_month,
    high_quarter,
    high_year,
    ab_high_yesterday,
    ab_high_week,
    ab_high_month,
    ab_high_quarter,
    ab_high_year,
    low_yesterday,
    low_week,
    low_month,
    low_quarter,
    low_year,
    ab_low_yesterday,
    ab_low_week,
    ab_low_month,
    ab_low_quarter,
    ab_low_year,
    spread_yesterday,
    spread_week,
    spread_month,
    spread_quarter,
    spread_year,
    vwap_week,
    vwap_month,
    vwap_quarter,
    vwap_year,
    _52w_low,
    _52w_high,
    std_dev_week,
    std_dev_month,
    std_dev_quarter,
    std_dev_year,
):
    schema = f"""INSERT INTO historical_db(
        last_updated, typeid, last_data,
        vol_yesterday, vol_week, vol_month, vol_quarter, vol_year,
        avg_price_yesterday, avg_price_week, avg_price_month, avg_price_quarter, avg_price_year,
        order_count_yesterday, order_count_week, order_count_month, order_count_quarter, order_count_year,
        size_yesterday, size_week, size_month, size_quarter, size_year,
        high_yesterday, high_week, high_month, high_quarter, high_year,
        ab_high_yesterday, ab_high_week, ab_high_month, ab_high_quarter, ab_high_year,
        low_yesterday, low_week, low_month, low_quarter, low_year,
        ab_low_yesterday, ab_low_week, ab_low_month, ab_low_quarter, ab_low_year,
        spread_yesterday, spread_week, spread_month, spread_quarter, spread_year,
        vwap_week, vwap_month, vwap_quarter, vwap_year,
        _52w_low, _52w_high, std_dev_week, std_dev_month, std_dev_quarter, std_dev_year
    ) VALUES (
        '{datetime.now()}', {typeid}, '{last_data}',
        {vol_yesterday}, {vol_week}, {vol_month}, {vol_quarter}, {vol_year},
        {avg_price_yesterday}, {avg_price_week}, {avg_price_month}, {avg_price_quarter}, {avg_price_year},
        {order_count_yesterday}, {order_count_week}, {order_count_month}, {order_count_quarter}, {order_count_year},
        {size_yesterday}, {size_week}, {size_month}, {size_quarter}, {size_year},
        {high_yesterday}, {high_week}, {high_month}, {high_quarter}, {high_year},
        {ab_high_yesterday}, {ab_high_week}, {ab_high_month}, {ab_high_quarter}, {ab_high_year},
        {low_yesterday}, {low_week}, {low_month}, {low_quarter}, {low_year},
        {ab_low_yesterday}, {ab_low_week}, {ab_low_month}, {ab_low_quarter}, {ab_low_year},
        {spread_yesterday}, {spread_week}, {spread_month}, {spread_quarter}, {spread_year},
        {vwap_week}, {vwap_month}, {vwap_quarter}, {vwap_year},
        {_52w_low}, {_52w_high}, {std_dev_week}, {std_dev_month}, {std_dev_quarter}, {std_dev_year}
    )"""

    try:
        with sqlite3.connect(historical_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(schema)
            conn.commit()
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)


def create_live_table():
    live_scheme = """typeid INTEGER PRIMARY KEY,
    buy_weighted_average FLOAT,
    buy_max FLOAT,
    buy_min FLOAT,
    buy_stddev FLOAT,
    buy_median FLOAT,
    buy_volume FLOAT,
    buy_order_count INTEGER,
    buy_percentile FLOAT,
    sell_weighted_average FLOAT,
    sell_max FLOAT,
    sell_min FLOAT,
    sell_stddev FLOAT,
    sell_median FLOAT,
    sell_volume FLOAT,
    sell_order_count INTEGER,
    sell_percentile FLOAT"""

    create_db(live_db_path, "live_db", live_scheme)



def create_historical_table():
    historical_scheme = """
    typeid INTEGER PRIMARY KEY,
    last_updated DATETIME,
    last_data TEXT,
    vol_yesterday FLOAT,
    vol_week FLOAT,
    vol_month FLOAT,
    vol_quarter FLOAT,
    vol_year FLOAT,
    avg_price_yesterday FLOAT,
    avg_price_week FLOAT,
    avg_price_month FLOAT,
    avg_price_quarter FLOAT,
    avg_price_year FLOAT,
    order_count_yesterday FLOAT,
    order_count_week FLOAT,
    order_count_month FLOAT,
    order_count_quarter FLOAT,
    order_count_year FLOAT,
    size_yesterday FLOAT,
    size_week FLOAT,
    size_month FLOAT,
    size_quarter FLOAT,
    size_year FLOAT,
    high_yesterday FLOAT,
    high_week FLOAT,
    high_month FLOAT,
    high_quarter FLOAT,
    high_year FLOAT,
    ab_high_yesterday FLOAT,
    ab_high_week FLOAT,
    ab_high_month FLOAT,
    ab_high_quarter FLOAT,
    ab_high_year FLOAT,
    low_yesterday FLOAT,
    low_week FLOAT,
    low_month FLOAT,
    low_quarter FLOAT,
    low_year FLOAT,
    ab_low_yesterday FLOAT,
    ab_low_week FLOAT,
    ab_low_month FLOAT,
    ab_low_quarter FLOAT,
    ab_low_year FLOAT,
    spread_yesterday FLOAT,
    spread_week FLOAT,
    spread_month FLOAT,
    spread_quarter FLOAT,
    spread_year FLOAT,
    vwap_week FLOAT,
    vwap_month FLOAT,
    vwap_quarter FLOAT,
    vwap_year FLOAT,
    _52w_low FLOAT,
    _52w_high FLOAT,
    std_dev_week FLOAT,
    std_dev_month FLOAT,
    std_dev_quarter FLOAT,
    std_dev_year FLOAT"""
    create_db(historical_db_path, "historical_db", historical_scheme)


def get_historical_item(typeId: int):
    if not isinstance(typeId, int):
        raise ValueError("Can't lookup value of non int")
    query = f"SELECT * from historical_db where typeID = {typeId}"
    try:
        with sqlite3.connect(historical_db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            result = cursor.execute(query)
            row = result.fetchone()
            if row:
                return dict(row)
            else:
                return "Not Found"
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

def get_live_item(typeId: int):
    if not isinstance(typeId, int):
        raise ValueError("Can't lookup value of non int")
    query = f"SELECT * from live_db where typeID = {typeId}"
    try:
        with sqlite3.connect(live_db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            result = cursor.execute(query)
            row = result.fetchone()
            if row:
                return dict(row)
            else:
                return "Not Found"
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)



def get_db_size(database_path, database_name) -> int:
    querey = f"SELECT count(typeID) from {database_name}"
    try:
        with sqlite3.connect(database_path) as conn:
            print(f"Opened SQLite database with version {sqlite3.sqlite_version}")
            cursor = conn.cursor()
            result = cursor.execute(querey)
            print(result)
            row = result.fetchone()
            if row:
                return row[0]
            else:
                return "Not Found"
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

    return 0


if __name__ == "__main__":
    drop_db(historical_db_path, "historical_db")
    drop_db(live_db_path, "live_db")

    create_live_table()
    create_historical_table()
    post_live_data(
        live_db_path,
        typeid=1,
        buy_weighted_average=0.0,
        buy_max=0.0,
        buy_min=0.0,
        buy_stddev=0.0,
        buy_median=0.0,
        buy_volume=0.0,
        buy_order_count=0,
        buy_percentile=0.0,
        sell_weighted_average=0.0,
        sell_max=0.0,
        sell_min=0.0,
        sell_stddev=0.0,
        sell_median=0.0,
        sell_volume=0.0,
        sell_order_count=0,
        sell_percentile=0.0,
    )
    post_live_data(
        live_db_path,
        typeid=2,
        buy_weighted_average=0.0,
        buy_max=0.0,
        buy_min=0.0,
        buy_stddev=0.0,
        buy_median=0.0,
        buy_volume=0.0,
        buy_order_count=0,
        buy_percentile=0.0,
        sell_weighted_average=0.0,
        sell_max=0.0,
        sell_min=0.0,
        sell_stddev=0.0,
        sell_median=0.0,
        sell_volume=0.0,
        sell_order_count=0,
        sell_percentile=0.0,
    )
    post_live_data(
        live_db_path,
        typeid=3,
        buy_weighted_average=0.0,
        buy_max=0.0,
        buy_min=0.0,
        buy_stddev=0.0,
        buy_median=0.0,
        buy_volume=0.0,
        buy_order_count=0,
        buy_percentile=0.0,
        sell_weighted_average=0.0,
        sell_max=0.0,
        sell_min=0.0,
        sell_stddev=0.0,
        sell_median=0.0,
        sell_volume=0.0,
        sell_order_count=0,
        sell_percentile=0.0,
    )
    post_historical_data(
        historical_db_path,
        typeid=0,
        last_data="Test Data",
        vol_yesterday=0.0,
        vol_week=0.0,
        vol_month=0.0,
        vol_quarter=0.0,
        vol_year=0.0,
        avg_price_yesterday=0.0,
        avg_price_week=0.0,
        avg_price_month=0.0,
        avg_price_quarter=0.0,
        avg_price_year=0.0,
        order_count_yesterday=0.0,
        order_count_week=0.0,
        order_count_month=0.0,
        order_count_quarter=0.0,
        order_count_year=0.0,
        size_yesterday=0.0,
        size_week=0.0,
        size_month=0.0,
        size_quarter=0.0,
        size_year=0.0,
        high_yesterday=0.0,
        high_week=0.0,
        high_month=0.0,
        high_quarter=0.0,
        high_year=0.0,
        ab_high_yesterday=0.0,
        ab_high_week=0.0,
        ab_high_month=0.0,
        ab_high_quarter=0.0,
        ab_high_year=0.0,
        low_yesterday=0.0,
        low_week=0.0,
        low_month=0.0,
        low_quarter=0.0,
        low_year=0.0,
        ab_low_yesterday=0.0,
        ab_low_week=0.0,
        ab_low_month=0.0,
        ab_low_quarter=0.0,
        ab_low_year=0.0,
        spread_yesterday=0.0,
        spread_week=0.0,
        spread_month=0.0,
        spread_quarter=0.0,
        spread_year=0.0,
        vwap_week=0.0,
        vwap_month=0.0,
        vwap_quarter=0.0,
        vwap_year=0.0,
        _52w_low=0.0,
        _52w_high=0.0,
        std_dev_week=0.0,
        std_dev_month=0.0,
        std_dev_quarter=0.0,
        std_dev_year=0.0,
    )
    post_historical_data(
        historical_db_path,
        typeid=1,
        last_data="Test Data",
        vol_yesterday=0.0,
        vol_week=0.0,
        vol_month=0.0,
        vol_quarter=0.0,
        vol_year=0.0,
        avg_price_yesterday=0.0,
        avg_price_week=0.0,
        avg_price_month=0.0,
        avg_price_quarter=0.0,
        avg_price_year=0.0,
        order_count_yesterday=0.0,
        order_count_week=0.0,
        order_count_month=0.0,
        order_count_quarter=0.0,
        order_count_year=0.0,
        size_yesterday=0.0,
        size_week=0.0,
        size_month=0.0,
        size_quarter=0.0,
        size_year=0.0,
        high_yesterday=0.0,
        high_week=0.0,
        high_month=0.0,
        high_quarter=0.0,
        high_year=0.0,
        ab_high_yesterday=0.0,
        ab_high_week=0.0,
        ab_high_month=0.0,
        ab_high_quarter=0.0,
        ab_high_year=0.0,
        low_yesterday=0.0,
        low_week=0.0,
        low_month=0.0,
        low_quarter=0.0,
        low_year=0.0,
        ab_low_yesterday=0.0,
        ab_low_week=0.0,
        ab_low_month=0.0,
        ab_low_quarter=0.0,
        ab_low_year=0.0,
        spread_yesterday=0.0,
        spread_week=0.0,
        spread_month=0.0,
        spread_quarter=0.0,
        spread_year=0.0,
        vwap_week=0.0,
        vwap_month=0.0,
        vwap_quarter=0.0,
        vwap_year=0.0,
        _52w_low=0.0,
        _52w_high=0.0,
        std_dev_week=0.0,
        std_dev_month=0.0,
        std_dev_quarter=0.0,
        std_dev_year=0.0,
    )
    post_historical_data(
        historical_db_path,
        typeid=2,
        last_data="Test Data",
        vol_yesterday=0.0,
        vol_week=0.0,
        vol_month=0.0,
        vol_quarter=0.0,
        vol_year=0.0,
        avg_price_yesterday=0.0,
        avg_price_week=0.0,
        avg_price_month=0.0,
        avg_price_quarter=0.0,
        avg_price_year=0.0,
        order_count_yesterday=0.0,
        order_count_week=0.0,
        order_count_month=0.0,
        order_count_quarter=0.0,
        order_count_year=0.0,
        size_yesterday=0.0,
        size_week=0.0,
        size_month=0.0,
        size_quarter=0.0,
        size_year=0.0,
        high_yesterday=0.0,
        high_week=0.0,
        high_month=0.0,
        high_quarter=0.0,
        high_year=0.0,
        ab_high_yesterday=0.0,
        ab_high_week=0.0,
        ab_high_month=0.0,
        ab_high_quarter=0.0,
        ab_high_year=0.0,
        low_yesterday=0.0,
        low_week=0.0,
        low_month=0.0,
        low_quarter=0.0,
        low_year=0.0,
        ab_low_yesterday=0.0,
        ab_low_week=0.0,
        ab_low_month=0.0,
        ab_low_quarter=0.0,
        ab_low_year=0.0,
        spread_yesterday=0.0,
        spread_week=0.0,
        spread_month=0.0,
        spread_quarter=0.0,
        spread_year=0.0,
        vwap_week=0.0,
        vwap_month=0.0,
        vwap_quarter=0.0,
        vwap_year=0.0,
        _52w_low=0.0,
        _52w_high=0.0,
        std_dev_week=0.0,
        std_dev_month=0.0,
        std_dev_quarter=0.0,
        std_dev_year=0.0,
    )


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

def timestamp_guard(timestamp_path, cooldown = timedelta(days=1)):
    # Historical start up
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = datetime.now(timezone.utc)
            if os.path.exists(timestamp_path):
                with open(timestamp_path, "r") as file:
                    try:
                        last_run_str = file.read().strip()
                        last_run = datetime.fromisoformat(last_run_str)
                        print(last_run_str)
                        print(last_run)
                        print(now)
                        print("Cooldown:", cooldown)
                        if last_run.tzinfo == None:
                            last_run = last_run.replace(tzinfo=timezone.utc)
                        print("Diff:", now - last_run)
                        if now - last_run < cooldown:
                            print(f"Unable to run: {func.__name__} too soon")
                            return
                    except Exception as e:
                        print (f"Failed to parse timestamp, rerunning. Reason {e}")
            result = func(*args, **kwargs)
            with open(timestamp_path, "w") as file:
                file.write(now.isoformat())
            return result
        return wrapper
    return decorator

@timestamp_guard("./data/timestamp_hist")
def hist_update(path):
    if os.path.exists(path):
        drop_db(path, "historical_db")
    create_historical_table()
    populate_historical_database()

@timestamp_guard("./data/timestamp_live", cooldown=timedelta(minutes=15))
def live_update(path):
    if os.path.exists(path):
        drop_db(path, "live_db")
    create_live_table()
    populate_live_database()

def update_dbs(hist_path = historical_db_path, live_path = live_db_path):
    hist_update(hist_path)
    live_update(live_path)

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
        post_live_data(live_db_path, res.response[key])
