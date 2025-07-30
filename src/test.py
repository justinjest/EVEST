#!/usr/bin/env python3

import unittest
from fuzzworks_call import *
import sqlite3
import tempfile
from pydantic import TypeAdapter
from unittest.mock import patch, MagicMock

class TestBuildLivePostData(unittest.TestCase):
    def test_build_post_data_structure_success(self):
        stats = BuySellStats(
            typeid=123,
            buy=MarketStats(
                weightedAverage=1.2, max=2.0, min=1.0, stddev=0.5,
                median=1.5, volume=1000.0, orderCount=10, percentile=0.9
            ),
            sell=MarketStats(
                weightedAverage=2.2, max=3.0, min=2.0, stddev=0.3,
                median=2.5, volume=2000.0, orderCount=20, percentile=0.8
            )
        )
        post_data = build_live_post_data(stats)
        self.assertEqual(post_data["typeid"], 123)
        self.assertEqual(post_data["buyWeightedAverage"], 1.2)
        self.assertEqual(post_data["sellMax"], 3.0)

    def test_build_post_data_structure_mallformed_typeid(self):
        stats = BuySellStats(
            typeid="123",
            buy=MarketStats(
                weightedAverage=1.2, max=2.0, min=1.0, stddev=0.5,
                median=1.5, volume=1000.0, orderCount=10, percentile=0.9
            ),
            sell=MarketStats(
                weightedAverage=2.2, max=3.0, min=2.0, stddev=0.3,
                median=2.5, volume=2000.0, orderCount=20, percentile=0.8
            )
        )
        post_data = build_live_post_data(stats)
        self.assertEqual(post_data["typeid"], 123)
        self.assertEqual(post_data["buyWeightedAverage"], 1.2)
        self.assertEqual(post_data["sellMax"], 3.0)



class TestGetTypeidsAsList(unittest.TestCase):
    def test_typeid_list_extraction(self):
        with tempfile.NamedTemporaryFile() as tmp:
            conn = sqlite3.connect(tmp.name)
            cur = conn.cursor()
            cur.execute("CREATE TABLE historical_db (typeid INTEGER);")
            cur.executemany("INSERT INTO historical_db (typeid) VALUES (?)", [(34,), (45,)])
            conn.commit()
            conn.close()

            result = get_typeids_as_list(tmp.name)
            self.assertEqual(result, [34, 45])

    def test_typeid_list_extraction_bad_id(self):
        with tempfile.NamedTemporaryFile() as tmp:
            conn = sqlite3.connect(tmp.name)
            cur = conn.cursor()
            cur.execute("CREATE TABLE historical_db (typeid INTEGER);")
            cur.executemany("INSERT INTO historical_db (typeid) VALUES (?)", [(0,), (34,)])
            conn.commit()
            conn.close()

            result = get_typeids_as_list(tmp.name)
            self.assertRaises(ValueError)

class TestValidation(unittest.TestCase):
    def test_validation_success(self):
        raw_data = {
            123: {
                "typeid": 123,
                "buy": {
                    "weightedAverage": 1.1, "max": 2.2, "min": 1.0, "stddev": 0.1,
                    "median": 1.5, "volume": 1000.0, "orderCount": 5, "percentile": 0.8
                },
                "sell": {
                    "weightedAverage": 2.1, "max": 3.2, "min": 2.0, "stddev": 0.3,
                    "median": 2.5, "volume": 2000.0, "orderCount": 10, "percentile": 0.9
                }
            }
        }

        adapter = TypeAdapter(dict[int, BuySellStats])
        parsed = adapter.validate_python(raw_data)
        self.assertIsInstance(parsed[123], BuySellStats)
        self.assertEqual(parsed[123].buy.volume, 1000.0)


class TestFuzzworksCall(unittest.TestCase):
    @patch("fuzzworks_call.requests.get")
    @patch("fuzzworks_call.get_typeids_as_list", return_value=[1])
    @patch("fuzzworks_call.get_preference", return_value="60003760")
    @patch("builtins.open")  # Prevent file write
    def test_fuzzworks_success(self, mock_open, mock_get_pref, mock_typeids, mock_requests):
        # Prepare mock response
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "1": {
                "buy": {
                    "weightedAverage": 1.0, "max": 1.1, "min": 0.9, "stddev": 0.05,
                    "median": 1.0, "volume": 1000, "orderCount": 10, "percentile": 0.95
                },
                "sell": {
                    "weightedAverage": 2.0, "max": 2.1, "min": 1.9, "stddev": 0.05,
                    "median": 2.0, "volume": 2000, "orderCount": 20, "percentile": 0.9
                }
            }
        }
        print("Mock created")
        mock_requests.return_value = mock_resp
        print("Mock sent")
        result = fuzzworks_call().get_val()
        self.assertIn(1, result)
        self.assertIsInstance(result[1], BuySellStats)
        self.assertEqual(result[1].buy.orderCount, 10)
