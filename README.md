# Most Active Cookie

A command line program to process the log file and return the most active cookie for a specific day.

## Requires

- Python >= 3.7

## Usage

```shell
$ python most_active_cookies.py -h

usage: most_active_cookies.py [-h] -d DAY -f FILE [--ignore-error]

optional arguments:
  -h, --help            show this help message and exit
  -d DAY, --day DAY     Date to find the most active cookie for; in ISO format. Eg: 2020-02-24
  -f FILE, --file FILE  CSV file path. See ./tests/fixtures/sample.csv for example.
  --ignore-error        Continue processing for invalid rows. Default to True

$ python most_active_cookies.py -f /path/to/csv.csv -d 2018-12-09T07
```

### Sample output

```shell
$ python most_active_cookies.py -f /path/to/csv.csv -d 2018-12-09T07

AtY0laUfhglK3lC7
```

## Run test

```shell
python -m unittest
```
