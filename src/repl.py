#!/usr/bin/env python3

menu_actions = {
    "1": update_dbs,
    "2": output_order_sheet,
    "3": update_player,
    "4": quit_program}

def repl_loop():
    while True:
        print("\n=== EVEST Main Menu ===")
        print("1) Update database")
        print("2) Output buy and sell sheet")
        print("3) Make transactions")
        print("4) Quit")
        choice = input("Choose an option: ").strip()

        if action:
            try:
                action()
            except Exception as e:
                print(f"[ERROR] Something went wrong: {e}")
        else:
            print("Invalid option, please try again.")
