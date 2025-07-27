#!/usr/bin/env python3

from db_middleware import update_dbs
from buy_sell import output_order_sheet, flag_create
from profit_tracker import Player, update_player, print_player
from set_preferences import setup_preferences

import os

hist_timestamp = "./data/timestamp_hist"
live_timestamp = "./data/timestamp_live"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def update_database():
    update_dbs()

def produce_order_sheet():
    buy, sell = flag_create()
    output_order_sheet(buy, sell)

def player_orders(p):
    buy, sell = flag_create()
    update_player(buy, sell, p)
    print_player(p)

def update_preferences():
    setup_preferences()

def quit_program():
    exit(0)

def print_timestamps():
    if os.path.exists(hist_timestamp):
        with open(hist_timestamp, "r") as file:
            last_run = file.read().strip()
            print (f"Historical db last updated at {last_run} EvE Time")
    if os.path.exists(live_timestamp):
        with open(live_timestamp, "r") as file:
            last_run = file.read().strip()
            print (f"Historical db last updated at {last_run} EvE Time")


def repl_loop(p):
    clear_screen()
    print_timestamps()
    menu_actions = {
        "1": update_database,
        "2": produce_order_sheet,
        "3": lambda: player_orders(p),
        "4": update_preferences,
        "5": quit_program
    }


    while True:
        print("\n=== EVEST Main Menu ===")
        print("1) Update database")
        print("2) Output buy and sell sheet")
        print("3) Make transactions")
        print("4) Update preferences")
        print("5) Quit")
        choice = input("Choose an option: ").strip()
        action = menu_actions.get(choice)
        if action:
            clear_screen()
            try:
                action()
            except Exception as e:
                print(f"[ERROR] Something went wrong: {e}")
        else:
            print("Invalid option, please try again.")
