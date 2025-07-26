#!/usr/bin/env python3

import requests
import json
import sqlite3

def old_type_id():
    api_url = "https://mokaam.dk/API/market/type_ids"

    print(f"Pulling Mokaam type_ids")

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        output_json = "../data/typeids.json"
        with open(output_json, "w") as outfile:
            json.dump(data, outfile, indent=4)
        print(f"Data has been written to {output_json}")
    else:
        print(f"Error: {response.status_code}")


def lookup_type_id(typeId: int):
    database_path = "./static/inv.db"
    if not isinstance(typeId, int):
        raise Exception("Can't lookup value of non int")
    querey = f"SELECT typeName from invTypes where typeID = {typeId}"
    try:
        with sqlite3.connect(database_path) as conn:
            print(f"Opened SQLite database with version {sqlite3.sqlite_version}")
            cursor = conn.cursor()
            result = cursor.execute(querey)

            if result.fetchone():
                return result.fetchone()[0]
            else:
                return "Not Found"
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

if __name__ == "__main__":
    print(lookup_type_id(0))
