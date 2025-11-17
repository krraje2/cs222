import json
import unittest
from definitions import TEST_FILE_PATH
from network.course.course_schedule_fetcher import (
    ApiPathConfig,
    CourseScheduleFetcher,
    DetailMode,
)
import pytest


class TestGpaFetcher(unittest.TestCase):
    """tests CatalogFetcher Class"""

    # def test_ApiPathConfig_filled(self):
    #     expected = cf.ApiPathConfig(2021, "fa", "cs")

    # @pytest.fixture(autouse=True)
    # def before_each(self):
    #     """runs before each test"""
    #     csf = CourseScheduleFetcher()
    #     yield

    def test_set_mode_to_links(self):
        csf = CourseScheduleFetcher()
        links_mode = csf._set_mode({}, DetailMode.LINKS)
        self.assertEqual(links_mode["mode"], "links")

        summary_mode = csf._set_mode({}, DetailMode.SUMMARY)
        self.assertEqual(summary_mode["mode"], "summary")

        detail_mode = csf._set_mode({}, DetailMode.DETAIL)
        self.assertEqual(detail_mode["mode"], "detail")

        cascase_mode = csf._set_mode({}, DetailMode.CASCADE)
        self.assertEqual(cascase_mode["mode"], "cascade")

    def test_build_illinois_link(self):
        csf = CourseScheduleFetcher()
        actual = csf._build_illinois_link(
            "http://courses.illinois.edu/cisapp/explorer/schedule",
            ApiPathConfig(2014, "fall", "CS", 125, 35876),
            DetailMode.CASCADE,
        )
        expected = "http://courses.illinois.edu/cisapp/explorer/schedule/2014/fall/CS/125/35876.xml"
        self.assertEqual(expected, actual)

    def testing(self):
        csf = CourseScheduleFetcher()
        xml_path = str(TEST_FILE_PATH) + "/fa2014_schedule.xml"
        json_path = str(TEST_FILE_PATH) + "/fa2014_schedule.json"
        with open(xml_path, "rb") as xml_file:
            with open(json_path, "r") as json_file:
                actual = csf._xml_to_dict(xml_file)
                expected = json.load(json_file)
                self.assertEqual(actual, expected)
