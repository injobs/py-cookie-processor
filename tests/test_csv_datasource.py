import os.path
import unittest
from datetime import datetime

from base.errors import ProgramError
from datasource.csv_datasource import CSVDatasource


class TestCSVDatasource(unittest.TestCase):
    fixture_path = os.path.dirname(__file__) + '/fixtures'

    def test_file_exist(self):
        """ Ensure invalid path would raise ProgramError """
        csv_ds = CSVDatasource('/path/invalid')

        self.assertRaises(ProgramError, csv_ds.validate)

    def test_malformed_file(self):
        """ Ensure other than CSV would raise ProgramError """
        csv_ds = CSVDatasource(self.fixture_path + '/sample_invalid.csv')

        self.assertRaises(ProgramError, csv_ds.validate)

    def test_invalid_datetime_validation(self):
        """ Ensure invalid cookie raise raise ProgramError """

        self.assertRaises(ProgramError, CSVDatasource._validate_timestamp, '2020-26-26T00:00:00+00:00')

    def test_valid_datetime_validation(self):
        self.assertIsInstance(CSVDatasource._validate_timestamp('2020-12-26T00:00:00+00:00'), datetime)

    def test_invalid_cookie_validation(self):
        """ Ensure invalid cookie raise raise ProgramError """

        self.assertRaises(ProgramError, CSVDatasource._validate_cookie, ' ')

    def test_valid_cookie_validation(self):
        self.assertEqual(CSVDatasource._validate_cookie('random '), 'random')

    def test_valid_file(self):
        """ Ensures it doesn't raise any error upon valid file """

        csv_ds = CSVDatasource(self.fixture_path + '/sample.csv')

        rows = list(csv_ds.get_rows())

        self.assertEqual(len(rows), 8)
        self.assertIsInstance(rows[0]['timestamp'], datetime)
        self.assertIsInstance(rows[0]['cookie'], str)
