"""Tests functions of github_requests.py"""

import json
import unittest
from definitions import TEST_FILE_PATH

from network.gpa.gpa_fetcher import GpaFetcher, Semester


class TestGpaFetcher(unittest.TestCase):
    def test_fix_year_winter_semester(self):
        """Tests function that converts UIUC Semester year into Wade's semester format"""
        gpa_fetcher = GpaFetcher()
        self.assertEqual(gpa_fetcher._fix_year_winter_semester(2020), "2019_2020")

    def test_get_github_link(self):
        """Tests that Github links are properly generated"""
        gpa_fetcher = GpaFetcher()
        self.assertEqual(
            gpa_fetcher._get_github_link(
                "fa", "2020", "wadefagen", "datasets", "gpa/raw"
            ),
            "https://raw.githubusercontent.com/wadefagen/datasets/master/gpa/raw/fa2020.csv",
        )
        self.assertEqual(
            gpa_fetcher._get_github_link(
                "wi", "2020", "wadefagen", "datasets", "gpa/raw"
            ),
            "https://raw.githubusercontent.com/wadefagen/datasets/master/gpa/raw/wi2019_2020.csv",
        )

    def test_get_github_headers_json(self):
        """Tests that github json request header is properly retruned"""
        gpa_fetcher = GpaFetcher()
        header = gpa_fetcher._get_github_headers_json()
        self.assertEqual(header["Accept"], "application/vnd.github+json")

    def test_class_csv_to_dict(self):
        gpa_fetcher = GpaFetcher()
        json_file = open(f"{TEST_FILE_PATH}/fa2014.json")
        expected = json.load(json_file)
        with open(f"{TEST_FILE_PATH}/fa2014.csv", "r") as test_file:
            actual = gpa_fetcher._class_csv_to_dict(test_file)
            self.assertEqual(expected, actual)
        json_file.close
