#!/usr/bin/env python3

import requests
import json
import sqlite3

region_id = 10000002
api_url = f"https://mokaam.dk/API/market/all?regionid={region_id}"

response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    output_json = "../data/mokaam.json"
    with open(output_json, "w") as outfile:
        json.dump(data, outfile, indent=4)
    print(f"Data has been written to {output_json}")
else:
    print(f"Error: {response.status_code}")
