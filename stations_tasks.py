import re

from data_parser import parse_metafile


def extract_dates(df):
    dates_combined = df['Data uruchomienia'].astype(str) + ' ' + df['Data zamknięcia'].astype(str)
    pattern = r'\b\d{4}-\d{2}-\d{2}'

    all_dates = []

    for date in dates_combined:
        found_date = re.findall(pattern, date)
        all_dates.extend(found_date) #extends old list with new elements

    return sorted(set(all_dates))

def extract_latitude_and_longitude(df):
    lengths_combined = df['WGS84 φ N'].astype(str) + ' ' + df['WGS84 λ E'].astype(str)
    pattern = r'\b\d+\.\d{6}\b'

    all_lengths = []

    for value in lengths_combined:
        found_length = re.findall(pattern, value)
        all_lengths.extend(found_length)

    return sorted(set(all_lengths))

def find_two_part_names(df):
    pattern = r'^[^-]+\s*-\s*[^-]+$'

    return find_names(df, pattern)

def replace_polish_chars(text):
    text = re.sub(r'ą', 'a', text)
    text = re.sub(r'ć', 'c', text)
    text = re.sub(r'ę', 'e', text)
    text = re.sub(r'ł', 'l', text)
    text = re.sub(r'ń', 'n', text)
    text = re.sub(r'ó', 'o', text)
    text = re.sub(r'ś', 's', text)
    text = re.sub(r'ź', 'z', text)
    text = re.sub(r'ż', 'z', text)
    text = re.sub(r'Ą', 'A', text)
    text = re.sub(r'Ć', 'C', text)
    text = re.sub(r'Ę', 'E', text)
    text = re.sub(r'Ł', 'L', text)
    text = re.sub(r'Ń', 'N', text)
    text = re.sub(r'Ó', 'O', text)
    text = re.sub(r'Ś', 'S', text)
    text = re.sub(r'Ź', 'Z', text)
    text = re.sub(r'Ż', 'Z', text)
    return text

def refactor_names(df):
    names_spaceless = df['Nazwa stacji'].str.replace(r'\s+', '_', regex=True)
    names_refactored = names_spaceless.apply(replace_polish_chars)

    return names_refactored

def verify_mobility(df):
    pattern = r'.*MOB$'

    for index, row in df.iterrows():
        station_code = row['Kod stacji']
        station_placement = row['Rodzaj stacji']

        if re.fullmatch(pattern, station_code.strip()):
            if not station_placement == 'mobilna':
                print(f"Index {index}: Station '{station_code}' is not mobile")
                return False

    print('All stations ending with "MOB" are mobile')
    return True


def find_three_part_names(df):
    pattern = r'^[^-]+\s*-\s*[^-]+\s*-\s*[^-]+$'

    return find_names(df, pattern)

def find_names_with_coma_and_street(df):
    pattern = r'.*,.*\s*(ul\.|al\.)\s*\w*'

    return find_names(df, pattern)

def find_names(df, pattern):
    names = df['Nazwa stacji'].astype(str)

    found_names = []

    for name in names:
        if re.fullmatch(pattern, name.strip()):
            found_names.append(name)

    return found_names

def main():
    stations = parse_metafile('data_S5/stacje.csv')

    # 1. Wyciągnięcie dat z pliku
    print("1. Wyodrębnione daty:")
    dates = extract_dates(stations)
    print(dates)
    print("\n")

    # 2. Wyciągnięcie szerokości i długości geograficznej
    print("2. Szerokości i długości geograficzne:")
    lat_lon = extract_latitude_and_longitude(stations)
    print(lat_lon)
    print("\n")

    # 3. Nazwy stacji składające się z dwóch części (myślnik w nazwie)
    print("3. Nazwy stacji składające się z dwóch części:")
    two_part_names = find_two_part_names(stations)
    print(two_part_names)
    print("\n")

    # 4. Refaktoryzacja nazw stacji (zamiana spacji na podłogę)
    print("4. Refaktoryzowane nazwy stacji (spacja na podłogę, brak polskich znaków):")
    refactored_names = refactor_names(stations).head(10)  # Wyświetlamy tylko pierwsze 10 wierszy
    print(refactored_names)
    print("\n")

    # 5. Weryfikacja mobilności
    print("5. Weryfikacja mobilności:")
    verify_mobility(stations)
    print("\n")

    # 6. Nazwy stacji składające się z trzech części
    print("6. Nazwy stacji składające się z trzech części:")
    three_part_names = find_three_part_names(stations)
    print(three_part_names)
    print("\n")

    # 7. Lokacje zawierające przecinek oraz nazwę ulicy lub alei
    print("7. Lokacje zawierające przecinek i nazwę ulicy (ul.) lub alei (al.):")
    names_with_coma_and_street = find_names_with_coma_and_street(stations)
    print(names_with_coma_and_street)
    print("\n")


if __name__ == '__main__':
    main()