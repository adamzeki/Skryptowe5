import pandas as pd
import re

def parse_metafile(path):
    meta_df = pd.read_csv(path, sep=',')
    for col in meta_df:
        if re.search('[dD]ata', col):
            meta_df[col] = pd.to_datetime(meta_df[col], format='%Y-%m-%d') #if column has data specified in name, change it to datetime

    return meta_df

def parse_measures(path):
    header_rows = pd.read_csv(path, nrows=5, header=None)
    unit = header_rows.iloc[4, 1]

    measure_df = pd.read_csv(path, header=5, sep=',') #the 5th row conatins all info, except for unit, which we extract earlier
    measure_df.rename(columns={measure_df.columns[0]: 'Timestamp'}, inplace=True)
    measure_df.iloc[:, 0] = pd.to_datetime(measure_df.iloc[:, 0], format='%m/%d/%y %H:%M')

    return measure_df, unit