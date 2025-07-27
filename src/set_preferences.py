from preferences import save_preferences

station_to_region = {
    "Jita": {"station_id": 60003760, "region_id": 10000002},
    "Dodixie": {"station_id": 60011866, "region_id": 10000032},
    "Amarr VIII": {"station_id": 60008494, "region_id": 10000043},
}

time_options = {
    "One week": "week",
    "One month": "month",
    "One quarter": "quarter",
    "One year": "year",
}


def input_percentage(prompt):
    res = None
    while res is None:
        percent = input(prompt).strip().replace("%", "")
        try:
            return float(percent) / 100
        except:
            pass


def setup_preferences():
    choice = None
    while choice is None:
        print("In which station will you be trading?")
        for i, name in enumerate(station_to_region):
            print(f"{i + 1}. {name}")
        try:
            tmp = int(input("enter choice number: "))
            if tmp in range(1, len(station_to_region) + 1):
                choice = tmp
        except ValueError:
            pass
    station_name = list(station_to_region.keys())[choice - 1]
    station_info = station_to_region[station_name]

    time_options = ["week", "month", "quarter", "year"]
    time = None
    while time is None:
        print(
            "How far back do you want to calculate market history for price comparisons?"
        )
        for i, time in enumerate(time_options):
            print(f"{i + 1}. {time}")
        try:
            tmp = int(input("enter choice number: "))
            if tmp in range(1, len(time_options) + 1):
                choice = tmp
        except ValueError:
            pass
        time = list(time_options)[choice - 1]

    market_size = None
    while market_size is None:
        tmp = input(
            f"Market size (only show items that move this much ISK per {time}): "
        ).strip()
        try:
            int(tmp)
            market_size = tmp
        except:
            continue

    market_volume = None
    while market_volume is None:
        tmp = input(
            f"Minimum market volume filter (only show an item when it has moved this many items moved per {time}): "
        ).strip()
        try:
            int(tmp)
            market_volume = tmp
        except:
            continue

    sales_tax = input_percentage("Sales tax (e.g. 3.5%): ")
    buy_broker_fee = input_percentage("Buy broker fee (e.g. 2.5%): ")
    sell_broker_fee = input_percentage("Sell broker fee (e.g. 3.0%): ")

    preferences = {
        "region_id": str(station_info["region_id"]),
        "station_id": str(station_info["station_id"]),
        "time": time,
        "market_size": market_size,
        "market_volume": market_volume,
        "sales_tax": str(sales_tax),
        "buy_broker_fee": str(buy_broker_fee),
        "sell_broker_fee": str(sell_broker_fee),
    }

    save_preferences("./data/preferences.ini", preferences)


if __name__ == "__main__":
    setup_preferences()
