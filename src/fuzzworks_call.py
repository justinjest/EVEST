#!/usr/bin/env python3

import requests
import json
import sqlite3
from preferences import get_preference

station_id = get_preference("station_id")
region_id = get_preference("region_id")
type_ids = "34,35,36,37,38,39,40"  # TK import from somewhere else

api_url = (
    f"https://market.fuzzwork.co.uk/aggregates/?region={region_id}&types={type_ids}"
)

print(f"Pulling Fuzzwork API for station {station_id}")

response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    output_json = "../data/fuzzworks.json"
    with open(output_json, "w") as outfile:
        json.dump(data, outfile, indent=4)
    print(f"Data has been written to {output_json}")
else:
    print(f"Error: {response.status_code}")
