#!/usr/bin/env python3

import requests
import json
from secret import eveToken, charToken

def eve_inventory_call():

    url = f"https://esi.evetech.net/characters/{charToken}/assets"

    headers = {
        "Accept-Language": "",
        "If-None-Match": "",
        "X-Compatibility-Date": "2020-01-01",
        "X-Tenant": "",
        "Accept": "application/json",
        "Authorization": eveToken
    }

    response = requests.get(url, headers=headers)

    print(response.json())
    if response.status_code == 200:
        print(response.json())
    else:
        print("Unable to load data")

def return_items_at_station(station_id, eve_inventory_json):
    print (eve_inventory_json)

