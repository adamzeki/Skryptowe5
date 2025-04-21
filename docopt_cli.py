"""
Air Quality Station Data Analysis Program

Usage:
  docopt_cli.py <measure> <frequency> <start_date> <end_date> station
  docopt_cli.py <measure> <frequency> <start_date> <end_date> stats <station_code>

Arguments:
  -h --help         Show this screen.
  <measure>         Measured quantity (CO, C6H6, NO, NO2, NOx, O3, PM10, PM2.5, SO2)
  <frequency>       Measurement frequency (1g for hourly, 24g for daily averages)
  <start_date>      Start date in format YYYY-MM-DD
  <end_date>        End date in format YYYY-MM-DD
  <station_code>    Station code (only required for 'stats' command)

Subcommands:
  station           Print random station meeting the criteria
  stats             Calculates avg and std for inputted station
"""


from docopt import docopt
from datetime import datetime, timedelta

from cli_utils import print_random_station_generic, mean_and_std_generic


def main():
    args = docopt(__doc__)
    try:
        start_dt = datetime.strptime(args['<start_date>'], '%Y-%m-%d')
        end_dt = datetime.strptime(args['<end_date>'], '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)

        if start_dt > end_dt:
            print("Błąd: Data początkowa nie może być późniejsza niż końcowa.")
            return
    except ValueError:
        print("Błąd: Niepoprawny format daty.")
        return

    if args['station']:
        print_random_station_generic(args['<measure>'], args['<frequency>'], start_dt, end_dt)
    elif args['stats']:
        mean_and_std_generic(args['<measure>'], args['<frequency>'], start_dt, end_dt, args['<station_code>'])

if __name__ == "__main__":
    main()
