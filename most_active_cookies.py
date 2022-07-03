import argparse

from datasource.csv_datasource import CSVDatasource
from lib.cookie_processor import CookieProcessor
from lib.output_util import OutputUtil

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--day', required=True,
                    help='Date to find the most active cookie for; in ISO format. Eg: 2020-02-24')
parser.add_argument('-f', '--file', required=True,
                    help='CSV file path. See ./tests/fixtures/sample.csv for example.')
parser.add_argument('--ignore-error', default=True, action='store_true',
                    help='Continue processing for invalid rows. Default to True')

args = parser.parse_args()

csv_datasource = CSVDatasource(args.file, ignore_error=args.ignore_error)
OutputUtil.write_new_line_to_console(
    CookieProcessor(csv_datasource).get_most_active_cookies(args.day)
)
