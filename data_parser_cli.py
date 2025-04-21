import csv
import re

import pandas as pd

from utils import create_path
import logging

logger = logging.getLogger(__name__)


def parse_metafile(path):
    path = create_path(path)

    if not path.exists():
        logger.error(f"File at {path} doesn't exist.")
        return None

    logger.info(f"Opening file {path} for reading metadata.")

    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    logger.info(f"File {path} closed after reading metadata.")

    meta_df = pd.DataFrame(data)

    for col in meta_df:
        if re.search(r'[dD]ata', col):
            meta_df[col] = pd.to_datetime(meta_df[col],
                                          format='%Y-%m-%d')  # if column has data specified in name, change it to datetime

    return meta_df


def parse_measures(path):
    path = create_path(path)

    if not path.exists():
        logger.error(f"File at {path} doesn't exist.")
        return None

    logger.info(f"Opening file {path} for reading metadata.")

    header_rows = pd.read_csv(path, nrows=5, header=None)

    unit = header_rows.iloc[4, 1]

    measure_df = pd.read_csv(path, header=5,
                             sep=',')  # the 5th row conatins all info, except for unit, which we extract earlier

    logger.info(f"File {path} closed after reading metadata.")

    measure_df.rename(columns={measure_df.columns[0]: 'Timestamp'}, inplace=True)
    measure_df.iloc[:, 0] = pd.to_datetime(measure_df.iloc[:, 0], format='%m/%d/%y %H:%M')

    return measure_df, unit


'''def parse_metafile(path):
    path = create_path(path)

    if not path.exists():
        logger.error(f"File at {path} doesn't exist.")
        return None

    logger.info(f"Opening file {path} for reading metadata.")
    rows = []
    header = None

    with open(path, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)

        # Read the file and accumulate data
        for i, row in enumerate(csv_reader):
            logger.debug(f"Read {len(str(row))} bytes from line {i + 1}.")
            if i == 0:
                # Assuming the header is in the first row
                header = row
            else:
                rows.append(row)

    logger.info(f"File {path} closed after reading metadata.")

    meta_df = pd.DataFrame(rows, columns=header)

    for col in meta_df:
        if re.search(r'[dD]ata', col):
            meta_df[col] = pd.to_datetime(meta_df[col], format='%Y-%m-%d')

    return meta_df'''