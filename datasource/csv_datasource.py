import csv
from datetime import datetime
from typing import Generator

from base.datasource import AbstractDatasource
from base.errors import ProgramError


class CSVDatasource(AbstractDatasource):
    """
    Class to parse csv file and retrieve records
    """
    # The csv file must have this columns
    expected_columns = ['cookie', 'timestamp']

    def __init__(self, filepath: str, **kwargs):
        """
        :param filepath:
        :param ignore_error: Ignores only row level errors; meaning if a row data cannot be parsed, it can continue
        processing next row if this is True
        """
        self._file = filepath

        super().__init__(**kwargs)

    def validate(self):
        """
        Validates CSV file format. Primarily these things
        - File exist and readable
        - File has expected columns
        """
        try:
            with open(self._file) as fp:
                csvreader = csv.DictReader(fp, dialect='excel')

                # this can be None if file is empty
                cols = csvreader.fieldnames or []
                column_exist = all(col in cols for col in self.expected_columns)

                if not column_exist:
                    raise ProgramError('CSV file does not contain expected columns: %s' % self.expected_columns)
        except FileNotFoundError as exc:
            raise ProgramError('File not found at: %s' % self._file) from exc
        except UnicodeError as exc:
            raise ProgramError('Malformed CSV file.') from exc

    def get_rows(self) -> Generator[dict, None, None]:
        """
        Get rows of give date. Assume the given file is sorted timestamp in descending order.

        :return:
        """
        with open(self._file) as f:
            csvreader = csv.DictReader(f)

            for row in csvreader:
                try:
                    validated_data = self._validate_row(row)
                    yield validated_data
                except ProgramError:
                    if self._ignore_error:
                        continue
                    else:
                        raise

    @classmethod
    def _validate_row(cls, row: dict) -> dict:
        """
        Validates and returns value in native data type

        :param dict row:
        :return dict:
        """
        tt_str = row.get('timestamp')
        tt_dt = cls._validate_timestamp(tt_str)

        cookie = row.get('cookie')
        valid_cookie = cls._validate_cookie(cookie)

        return {
            'cookie': valid_cookie,
            'timestamp': tt_dt
        }

    @classmethod
    def _validate_timestamp(cls, dt_str: str) -> datetime:
        try:
            # %z parses "+00:00" timezone offset in Python >= 3.7
            return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S%z')
        except ValueError as exc:
            raise ProgramError('Cannot parse timestamp: %s' % dt_str) from exc

    @classmethod
    def _validate_cookie(cls, cookie: str) -> str:
        cookie = cookie.strip()

        if not cookie:
            raise ProgramError('Cookie value cannot be an empty string')

        return cookie
