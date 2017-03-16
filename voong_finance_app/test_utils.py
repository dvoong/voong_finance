import datetime
from unittest import TestCase
from voong_finance_app.utils import date_range

class TestDateRange(TestCase):

    def test(self):

        expected = [datetime.date(2017, 3, 1),
                    datetime.date(2017, 3, 2), 
                    datetime.date(2017, 3, 3), 
                    datetime.date(2017, 3, 4), 
                    datetime.date(2017, 3, 5), 
                    datetime.date(2017, 3, 6), 
                    datetime.date(2017, 3, 7)]

        dates = date_range(datetime.date(2017, 3, 1), datetime.date(2017, 3, 8))

        self.assertEqual(dates, expected)
