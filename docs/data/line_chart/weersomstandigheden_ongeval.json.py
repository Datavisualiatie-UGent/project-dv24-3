import csv
import json
import sys

weer = {}

with open("docs/data/OPENDATA_MAP_2017-2022.csv", newline='') as f:
    csv_reader = csv.DictReader(f, delimiter=',', quotechar='"')

    i = 0
    for row in csv_reader:
        key = (row['TX_WEATHER_NL'], row['DT_YEAR_COLLISION'])

        if key == '':
            key = "unknown"

        weer[key] = weer.get(key, 0) + 1

weer_json = list(map(lambda kv: {"weather": kv[0][0].lower(), "year": int(kv[0][1]), "count": kv[1]}, weer.items()))
json.dump(weer_json, sys.stdout)