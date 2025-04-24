import argparse
import logging
import sys
from datetime import datetime, timedelta
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
    parser = argparse.ArgumentParser(description="Program do analizy danych stacji pomiarowych.")

    # Główne argumenty
    parser.add_argument('-m', '--measure', type=str, required=True, choices=['CO', 'C6H6', 'NO', 'NO2', 'NOx',
                                                                             'O3', 'PM10', 'PM2.5', 'SO2'],

                        help="Mierzona wielkość")
    parser.add_argument('-f', '--frequency', type=str, required=True, choices=['1g', '24g'],
                        help="Częstotliwość pomiaru")
    parser.add_argument('-s', '--start-date', type=str, required=True,
                        help="Początek przedziału czasowego w formacie rrrr-mm-dd")
    parser.add_argument('-e', '--end-date', type=str, required=True,
                        help="Koniec przedziału czasowego w formacie rrrr-mm-dd")

    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_station = subparsers.add_parser('station',
                                           description="Wypisuje losową stację pomiarową prowadzącą pomiar danej wielkości w danych ramach czasowych")
    parser_station.set_defaults(func=print_random_station)

    parser_stats = subparsers.add_parser('stats',
                                         description="Oblicza średnią i odchylenie standardowe dla danej wielkości w zadanym przedziale czasowym dla danej stacji")
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

    # Walidacja dat
    try:
        args.start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        args.end_date = datetime.strptime(args.end_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(
            seconds=1)  # Łapiemy cały dzień godzinowo
        if args.start_date > args.end_date:
            logger.warning("Data początkowa nie może być późniejsza niż data końcowa.")
    except ValueError:
        logger.error("Błąd: Niepoprawny format daty. Użyj formatu rrrr-mm-dd.")
        return

    # Uruchomienie odpowiedniej funkcji w zależności od podkomendy
    args.func(args)


if __name__ == "__main__":
    main()
