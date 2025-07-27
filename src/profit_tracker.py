#!/usr/bin/env python3
import sqlite3
import datetime
from preferences import get_preference
from db_middleware import drop_db

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
                    avg_price = ((old_price * old_units) + (price * units)) / total_units
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
        else:
            print("You don't own this item.")

    def decide_buy_amount(self, price):
        if price == 0:
            raise ExceptionError("Price can not be zero")
        amt = round(self.funds * self.risk)
        units = round(amt/price)
        return units

    def is_bankrupt(self):
        self.bankrupt = (self.funds <= 0 and self.items == None)

    def log_transaction(self, action, item_id, price, units, db_path="./data/transactions.db"):
        total = price * units
        timestamp = datetime.datetime.now().replace(tzinfo=None).isoformat()
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transactions (timestamp, action, item_id, price, units, total, funds_after)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (timestamp, action, item_id, price, units, total, self.funds))

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


if __name__ == "__main__":
    drop_db("./data/transactions.db", "transactions")
    init_db()
    p = Player()
    p.buy_item(item_id=34, price=100000)
    p.sell_item(item_id=34, price=120000)

    if p.is_bankrupt():
        print("Bankrupt")
    else:
        print(f"Funds: {p.funds}")
