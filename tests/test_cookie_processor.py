import datetime
import os
import unittest
from datetime import date

from base.errors import ProgramError
from datasource.csv_datasource import CSVDatasource
from lib.cookie_processor import CookieProcessor


class TestCookieProcessor(unittest.TestCase):
    fixture_file = os.path.dirname(__file__) + '/fixtures/sample.csv'

    fixture_most_active_cookie = {
        '2018-12-09': {'AtY0laUfhglK3lC7'},
        '2018-12-08': {'fbcn5UAVanZf6UtG', '4sMM2LxV07bPJzwf', 'SAZuXPGUrfbcn5UA'},
        '2018-12-07': {'4sMM2LxV07bPJzwf'},
    }

    def test_error_on_datasource(self):
        self.assertRaises(ProgramError, CookieProcessor, CSVDatasource(''))

    def test_collect_row(self):
        csv_ds = CSVDatasource(self.fixture_file)
        rows = list(CookieProcessor._collect_rows_for_date(csv_ds.get_rows(), date(2018, 12, 9)))

        expected_rows = ['AtY0laUfhglK3lC7', 'SAZuXPGUrfbcn5UA', '5UAVanZf6UtGyKVS', 'AtY0laUfhglK3lC7']

        self.assertListEqual([row['cookie'] for row in rows], expected_rows)

    def test_aggregate_cookie(self):
        cookies = [{'cookie': 'xyz', 'timestamp': datetime.datetime(2018, 1, 1, 5)},
                   {'cookie': 'xyz', 'timestamp': datetime.datetime(2018, 1, 1, 6)},
                   {'cookie': 'xyz', 'timestamp': datetime.datetime(2018, 1, 1, 6)},
                   {'cookie': 'xyz', 'timestamp': datetime.datetime(2018, 1, 1, 6)},
                   {'cookie': 'ope', 'timestamp': datetime.datetime(2018, 1, 1, 9)},
                   {'cookie': 'ope', 'timestamp': datetime.datetime(2018, 1, 1, 9)},
                   {'cookie': 'z', 'timestamp': datetime.datetime(2018, 1, 1, 9)},
                   {'cookie': 'z', 'timestamp': datetime.datetime(2018, 1, 1, 9)},
                   {'cookie': 'o', 'timestamp': datetime.datetime(2018, 1, 1, 9)},
                   {'cookie': 'z', 'timestamp': datetime.datetime(2018, 1, 1, 9)}]

        result = CookieProcessor._aggr_cookie(cookies)

        self.assertDictEqual(result, {1: {'o'}, 2: {'ope'}, 3: {'z'}, 4: {'xyz'}})

    def test_empty_set_find_most_freq_cookies(self):
        """ Ensures returns empty set on empty dict """

        self.assertEqual(CookieProcessor._find_most_freq_cookies({}), set())

    def test_find_most_freq_cookies(self):
        csv_ds = CSVDatasource(self.fixture_file)
        rows = list(CookieProcessor._collect_rows_for_date(csv_ds.get_rows(), date(2018, 12, 9)))
        count_dict = CookieProcessor._aggr_cookie(rows)

        self.assertEqual(CookieProcessor._find_most_freq_cookies(count_dict), {'AtY0laUfhglK3lC7'})

        count_dict = {5: {'abc'}, 10: {'xii', 'op', 'zk'}, 9: {'c', 'opz'}}
        self.assertEqual(CookieProcessor._find_most_freq_cookies(count_dict), {'xii', 'op', 'zk'})

    def test_error_on_parse_date_str(self):
        self.assertRaises(ProgramError, CookieProcessor._parse_date_str, '5489965')
        self.assertRaises(ProgramError, CookieProcessor._parse_date_str, '2012-02-33')

    def test_parse_date_str(self):
        self.assertEqual(CookieProcessor._parse_date_str('2012-02-03'), date(2012, 2, 3))

    def test_get_most_active_cookies(self):
        csv_ds = CSVDatasource(self.fixture_file)
        processor = CookieProcessor(csv_ds)

        for day, expected in self.fixture_most_active_cookie.items():
            result = processor.get_most_active_cookies(day)
            self.assertEqual(expected, result)
