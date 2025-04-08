import re
from pathlib import Path
import os

def group_measurement_files_by_key(path):
    if not os.path.isdir(path):
        print("Path doesnt lead to a directory")
        return None

    pattern = re.compile(r'^(\d{4})_(.+)_(.+)\.csv$')
    grouped_files = {}
    path = Path(path)

    for file in path.iterdir():
        if file.is_file():
            match = pattern.match(file.name)
            if match: #if pattern didnt match, match = None
                key = match.groups()
                grouped_files[key] = file

    return grouped_files

result = group_measurement_files_by_key('data_S5/measurements')
i=0
for key in result:
    if i > 5:
        break
    i+=1
    print(key, result[key])