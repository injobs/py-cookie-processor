from datetime import date
from typing import Iterable

from base.datasource import AbstractDatasource
from base.errors import ProgramError


class CookieProcessor:
    """
    Class to process cookie list
    """

    def __init__(self, datasource: AbstractDatasource):
        assert datasource, 'Data is not provided'

        self._ds = datasource
        self._ds.validate()

    def get_most_active_cookies(self, day: str) -> Iterable[str]:
        """
        Find a list of cookies that occurred most in given day.

        :param day:
        :return:
        """
        dt = self._parse_date_str(day)
        rows = self._collect_rows_for_date(self._ds.get_rows(), dt)
        count_dict = self._aggr_cookie(rows)

        return self._find_most_freq_cookies(count_dict)

    @staticmethod
    def _collect_rows_for_date(rows: Iterable[dict], dt: date):
        for row in rows:
            date_ = row['timestamp'].date()

            if date_ > dt:
                continue

            if date_ < dt:
                # Since the records are sorted by datetime, we don't need data below the given date.
                break

            yield row

    @staticmethod
    def _aggr_cookie(rows: Iterable[dict]) -> dict:
        """
        Aggregates cookie for the given date and build a dict where keys are number of times a cookie occurred and
        value is set of cookies.

        :return:
            dict: {COUNTER: set([Cookie])}
        """
        cookie_dict = {}
        count_dict = {}

        for row in rows:
            cookie = row['cookie']

            cookie_dict.setdefault(cookie, 0)
            cookie_dict[cookie] += 1

            count = cookie_dict[cookie]
            if count_dict.get(count, None) is None:
                count_dict.setdefault(count, {cookie})
            else:
                count_dict[count].add(cookie)

            # Remove cookie from previous counter to save some memory
            if count > 1:
                count_dict[count - 1].remove(cookie)

        return count_dict

    @staticmethod
    def _find_most_freq_cookies(count_dict) -> Iterable[str]:
        try:
            max_cnt = max(count_dict.keys())
        except ValueError:
            return set()

        return count_dict.get(max_cnt, set())

    @staticmethod
    def _parse_date_str(date_str: str) -> date:
        """
        Parse ISO date string to date object

        :param date_str:
        :return date:
        """
        try:
            return date.fromisoformat(date_str)
        except (ValueError, TypeError) as exc:
            raise ProgramError('Cannot parse date: %s', date_str) from exc
