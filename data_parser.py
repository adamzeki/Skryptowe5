import pandas as pd
import re
import os
#r before '' designates a raw string - you dont have to escape backslashes abd other special chars

def parse_metafile(path):
    if not os.path.exists(path):
        print("Path doesnt exist")
        return None

    meta_df = pd.read_csv(path, sep=',')
    for col in meta_df:
        if re.search(r'[dD]ata', col):
            meta_df[col] = pd.to_datetime(meta_df[col], format='%Y-%m-%d') #if column has data specified in name, change it to datetime

    return meta_df

def parse_measures(path):
    if not os.path.exists(path):
        print("Path doesnt exist")
        return None

    header_rows = pd.read_csv(path, nrows=5, header=None)
    unit = header_rows.iloc[4, 1]

    measure_df = pd.read_csv(path, header=5, sep=',') #the 5th row conatins all info, except for unit, which we extract earlier
    measure_df.rename(columns={measure_df.columns[0]: 'Timestamp'}, inplace=True)
    measure_df.iloc[:, 0] = pd.to_datetime(measure_df.iloc[:, 0], format='%m/%d/%y %H:%M')

    return measure_df, unit

#print(parse_measures('data_S5/measurements/2023_BkF(PM10)_24g.csv')[0].iloc[145, 1]) #test for 7.00E-02 - works properly