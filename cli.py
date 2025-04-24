import argparse
import logging
import sys
from datetime import datetime, timedelta
from group_measures import group_measurement_files_by_key
from cli_utils import print_random_station_generic, mean_and_std_generic, anomaly_detection_generic

formatter = logging.Formatter('%(levelname)s: %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)
stdout_handler.setFormatter(formatter)

stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.ERROR)
stderr_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)


def print_random_station(args):
    print_random_station_generic(args.measure, args.frequency, args.start_date, args.end_date)


def mean_and_std(args):
    mean_and_std_generic(args.measure, args.frequency, args.start_date, args.end_date, args.station_code)

def anomaly_detection(args):
    anomaly_detection_generic(args.measure, args.frequency, args.start_date, args.end_date, args.threshold)


def create_parser():
    parser = argparse.ArgumentParser(description="Program for analyzing measurement station data.")

    # Main arguments
    parser.add_argument('-m', '--measure', type=str, required=True, help="Measured parameter")
    parser.add_argument('-f', '--frequency', type=str, required=True, choices=['1g', '24g'],
                        help="Measurement frequency")
    parser.add_argument('-s', '--start-date', type=str, required=True,
                        help="Start of the time interval in the format YYYY-MM-DD")
    parser.add_argument('-e', '--end-date', type=str, required=True,
                        help="End of the time interval in the format YYYY-MM-DD")

    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_station = subparsers.add_parser('station',
                                           description="Prints a random measurement station conducting measurements of the given parameter within the specified time frame")

    parser_station.set_defaults(func=print_random_station)

    parser_stats = subparsers.add_parser('stats',
                                         description="Calculates the average and standard deviation for a given parameter within a specified time interval for a given station.")
    parser_stats.add_argument('-s', '--station-code', type=str, required=True, help="Kod stacji")
    parser_stats.set_defaults(func=mean_and_std)

    parser_anomalies = subparsers.add_parser('anomalies',
                                             description='Wykrywa stacje z anomalnymi odczytami danej wielkości w danych ramach czasowych')
    parser_anomalies.add_argument('-th', '--threshold', type=int, required=True, help='Próg alarmowy odczytu')
    parser_anomalies.set_defaults(func=anomaly_detection)

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    logger.debug(f"CLI input length: {len(' '.join(sys.argv))} bytes.")

    # Walidacja pomiaru
    grouped_measures = group_measurement_files_by_key('data_S5/measurements')

    if not any(args.measure in key for key in grouped_measures.keys()):
        logger.warning(f"No data for measure '{args.measure}'.")

    # Walidacja dat
    try:
        args.start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        args.end_date = datetime.strptime(args.end_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(
            seconds=1)  # Łapiemy cały dzień godzinowo
        if args.start_date > args.end_date:
            logger.warning("Start date must be before end date.")
    except ValueError:
        logger.error("Incorrect data format. Use YYYY-MM-DD.")
        return

    # Uruchomienie odpowiedniej funkcji w zależności od podkomendy
    args.func(args)


if __name__ == "__main__":
    main()
