import csv
import json
import sys

licht = {}

with open("docs/data/OPENDATA_MAP_2017-2022.csv", newline='') as f:
    csv_reader = csv.DictReader(f, delimiter=',', quotechar='"')

    i = 0
    for row in csv_reader:
        key = (row['TX_LIGHT_CONDITION_NL'], row['DT_YEAR_COLLISION'])

        if key == '':
            key = "unknown"

        licht[key] = licht.get(key, 0) + 1

licht_json = list(map(lambda kv: {"light": kv[0][0].lower(), "year": int(kv[0][1]), "count": kv[1]}, licht.items()))
json.dump(licht_json, sys.stdout)