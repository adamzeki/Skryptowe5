from pathlib import Path
import re
from data_parser import *
from utils import create_path

def get_addresses(path, city):
    path = create_path(path)


    if not path.is_file():
        print("Path doesnt lead to a file")
        return None

    data = parse_metafile(path)
    pattern = re.compile(r"""
    ^(?P<street>.+?) #matching all signs from the beginning of the string until the final space
    \s+ #ensuring theres at least one space
    (?P<number>
        \d+ #the number has to start with 1 or more digits
        \s? #may be followed by a single space
        [a-zA-Z]{0,3} #it may be followed by up to 3 letters
        (?:/\d+[A-Za-z]{0,3})? #then it may also be followed by a slash, 1 or more digits and up to 3 letters
    )
    $""", re.VERBOSE)

    result = []

    for _, row in data.iterrows():
        if row['Miejscowość'].strip().lower() == city.strip().lower():
            voi = row['Województwo'].strip()
            match = pattern.match(row['Adres'])
            street, number = match.group('street'), match.group('number')
            result.append((voi, city, street, number))

    return result

result = get_addresses('data_S5/stacje.csv', 'Lublin')
for i in result:
    print(i)