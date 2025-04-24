import logging
import random

from data_parser_cli import parse_measures, parse_metafile

logger = logging.getLogger(__name__)

def prepare_df(measure, frequency, start_date, end_date):
    measure = 'PM25' if measure == 'PM2.5' else measure
    path = f'data_S5/measurements/2023_{measure}_{frequency}.csv'

    try:
        df, unit = parse_measures(path)
    except:
        logger.error(f'Missing file with measurements for measure {measure} for frequency {frequency}')
        return None, None

    df = df[(df['Timestamp'] >= start_date) & (df['Timestamp'] <= end_date)]
    return df, unit


def print_random_station_generic(measure, frequency, start_date, end_date):
    df, unit = prepare_df(measure, frequency, start_date, end_date)

    if df is None:
        return

    if df.empty:
        logger.error(f'No data found for measure {measure} for frequency {frequency} at {start_date} to {end_date}')
        return

    station_codes = df.columns[1:].tolist()
    random_station = random.choice(station_codes).split('-')[0]

    df_stations = parse_metafile('data_S5/stacje.csv')
    result = df_stations[df_stations['Kod stacji'] == random_station][['Nazwa stacji', 'Adres']]

    if not result.empty:
        name = result.iloc[0]['Nazwa stacji']
        address = result.iloc[0]['Adres']
        print(f'Selected station:\nStation name: {name}\nAddress: {address}\nMeasured parameter: {measure}')
    else:
        logger.error('Unexpected error: no data found')


def mean_and_std_generic(measure, frequency, start_date, end_date, station_code):
    df, unit = prepare_df(measure, frequency, start_date, end_date)
    if df is None:
        return

    matching_columns = [col for col in df.columns if col.split('-')[0] == station_code]
    if not matching_columns:
        print(f"No data for station with code:{station_code}")
        return

    column = matching_columns[0]
    values = df[column].dropna()
    if values.empty:
        print("No available measurements in the specified time interval.")
        return

    mean = values.mean()
    std = values.std()

    print(f'Stats for station{station_code} ({column}):')
    print(f'  Mean: {mean:.2f} {unit}')
    print(f'  Standard deviation: {std:.2f} {unit}')