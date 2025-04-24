import re
from pathlib import Path
import os
from utils import create_path

def group_measurement_files_by_key(path):
    path = create_path(path)

    if not path.is_dir():
        print("Path doesnt lead to a directory")
        return None

    pattern = re.compile(r'^(\d{4})_(.+)_(.+)\.csv$')
    grouped_files = {}

    for file in path.iterdir():
        if file.is_file():
            match = pattern.match(file.name)
            if match: #if pattern didnt match, match == None
                key = match.groups()
                grouped_files[key] = file

    return grouped_files

def main():
    result = group_measurement_files_by_key('data_S5/measurements')
    i=0
    for key in result:
        if i > 5:
            break
        i+=1
        print(key, result[key])

if __name__ == '__main__':
    main()