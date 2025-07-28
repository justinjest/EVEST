#!/usr/bin/env python3

from db_middleware import update_dbs
from buy_sell import output_order_sheet, flag_create
from profit_tracker import Player, update_player, print_player
from set_preferences import setup_preferences
from typeids import lookup_type_id
from clipboard import to_clipboard

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
    order_repl(buy, sell)


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
            print(f"Historical db last updated at {last_run} EvE Time")
    if os.path.exists(live_timestamp):
        with open(live_timestamp, "r") as file:
            last_run = file.read().strip()
            print(f"Live db last updated at {last_run} EvE Time")


def repl_loop(p):
    clear_screen()
    print_timestamps()
    menu_actions = {
        "1": update_database,
        "2": produce_order_sheet,
        "3": lambda: player_orders(p),
        "4": update_preferences,
        "5": quit_program,
    }

    while True:
        print("\n=== EVEST Main Menu ===")
        print("1) Update database")
        print("2) Display market opportunities")
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


def order_repl(buy, sell):
    menu_actions = {"1": lambda: to_clipboard(buy), "2": lambda: to_clipboard(sell)}
    while True:
        print("=== Order Book ===")
        print("1) Copy buy items to clipboard")
        print("2) Copy sell items to clipboard")
        print("3) Exit to main menu")
        choice = input("Choose an option: ").strip()
        action = menu_actions.get(choice)
        if choice == "3":
            break
        if menu_actions:
            try:
                action()
            except Exception as e:
                print(f"[ERROR] Something went wrong: {e}")
            else:
                print("Invalid option, please try again.")
