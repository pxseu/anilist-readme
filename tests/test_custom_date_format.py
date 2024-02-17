import unittest
from dateutil import tz
from datetime import datetime
from anilist_readme.list_activity import custom_datetime_format


class TestCustomDatetimeFormat(unittest.TestCase):
    def test_custom_datetime_format_with_tz(self):
        date = datetime.fromtimestamp(1667059380, tz.gettz("Europe/Warsaw"))

        self.assertEqual(
            custom_datetime_format(date, "{h}:{m} {D} {MW} {Y}"),
            "18:03 29 October 2022",
        )

        self.assertEqual(
            custom_datetime_format(date, "{h}:{m} {D}/{M}/{Y}"),
            "18:03 29/10/2022",
        )

    def test_custom_datetime_format_without_tz(self):
        date = datetime.fromtimestamp(1667059380, tz.gettz("UTC"))

        self.assertEqual(
            custom_datetime_format(date, "{h}:{m} {D} {MW} {Y}"),
            "16:03 29 October 2022",
        )
