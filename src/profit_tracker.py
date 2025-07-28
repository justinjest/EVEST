#!/usr/bin/env python3
import sqlite3
import datetime
from typeids import lookup_type_id
from preferences import get_preference
from db_middleware import drop_db, get_live_item


class Player:
    def __init__(self, starting_funds=1000000000, personal_risk=0.01):
        self.funds = starting_funds
        self.items = {}
        self.risk = personal_risk
        self.bankrupt = False
        self.buy_fee = float(get_preference("buy_broker_fee"))
        self.sell_fee = float(get_preference("sell_broker_fee"))
        self.sales_tax = float(get_preference("sales_tax"))

    def buy_item(self, item_id, price):
        units = self.decide_buy_amount(price)
        if units != 0:
            cost = price * units
            if self.funds >= cost:
                self.funds -= cost
                if item_id in self.items:
                    old_price, old_units = self.items[item_id]
                    total_units = old_units + units
                    avg_price = (
                        (old_price * old_units) + (price * units)
                    ) / total_units
                    self.items[item_id] = (avg_price, total_units)
                else:
                    self.items[item_id] = (price, units)
                self.log_transaction("buy", item_id, price, units)
            else:
                print("Insufficient funds to buy.")

    def sell_item(self, item_id, price):
        if item_id in self.items:
            _, units = self.items.pop(item_id)
            revenue = price * units
            self.funds += revenue
            self.log_transaction("sell", item_id, price, units)

    def decide_buy_amount(self, price):
        if price == 0:
            raise ExceptionError("Price can not be zero")
        amt = round(self.funds * self.risk)
        units = round(amt / price)
        return units

    def is_bankrupt(self):
        self.bankrupt = self.funds <= 0 and self.items == None

    def log_transaction(
        self, action, item_id, price, units, db_path="./data/transactions.db"
    ):
        total = price * units
        timestamp = datetime.datetime.now().replace(tzinfo=None).isoformat()
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO transactions (timestamp, action, item_id, price, units, total, funds_after)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (timestamp, action, item_id, price, units, total, self.funds),
            )


def create_transaction_database(db_path="./data/transactions.db"):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                action TEXT,
                item_id INTEGER,
                price REAL,
                units INTEGER,
                total REAL,
                funds_after REAL
            )
        """)


def print_player(p):
    print(f"User currently has: {round(p.funds, 2)} isk")
    items = p.items
    for item in items:
        print(f"{lookup_type_id(item)}")
        print(f"Avg buy price: {round(items[item][0], 2)}")
        print(f"Num in inventory: {items[item][1]}")
    print(f"User currently has: {round(p.funds, 2)} isk")


def update_player(buy, sell, p):
    for i in buy:
        data = get_live_item(i)
        p.buy_item(i, data["buy_weighted_average"])
    for i in sell:
        data = get_live_item(i)
        p.sell_item(i, data["sell_weighted_average"])


