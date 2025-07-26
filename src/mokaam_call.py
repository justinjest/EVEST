#!/usr/bin/env python3

import requests
import json
import sqlite3
from preferences import get_preference

class Response():
    def __init__(self, response = None, error = None):
        self.response = response
        self.error = error

    def get_val(self):
        if self.error != None:
            return self.error
        if self.response != None:
            return self.response
        # Neither an error or a response, must be handlded
        raise Exception("InvalidResponse")


def mokaam_call() -> Response():
    region_id = get_preference("region_id")
    api_url = f"https://mokaam.dk/API/market/all?regionid={region_id}"
    res = Response(None, None)
    print(f"Pulling Mokaam API for region {region_id}")

    response = requests.get(api_url)
    print("Received data from api")

    if response.status_code == 200:
        data = response.json()
        res.response = data
        output_json = "./data/mokaam.json"
        with open(output_json, "w") as outfile:
            json.dump(data, outfile, indent=4)
        print(f"Data has been written to {output_json}")
    else:
        res.error = respionse.status_code
        print(f"Error: {response.status_code}")

    return res

if __name__ == "__main__":
    res = Response()
    res.error = 404
    val = res.get_val()
    print(res)
    print(val)
    res.error = None
    res.response = '{"Key": "10"}'
    val = res.get_val()
    print(res)
    print(val)
