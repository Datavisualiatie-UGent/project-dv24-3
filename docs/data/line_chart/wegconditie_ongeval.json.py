import csv
import json
import sys

weg = {}

with open("docs/data/OPENDATA_MAP_2017-2022.csv", newline='') as f:
    csv_reader = csv.DictReader(f, delimiter=',', quotechar='"')

    i = 0
    for row in csv_reader:
        key = (row['TX_ROAD_CONDITION_NL'], row['DT_YEAR_COLLISION'])

        if key == '':
            key = "unknown"

        weg[key] = weg.get(key, 0) + 1

weg_json = list(map(lambda kv: {"cond": kv[0][0].lower(), "year": int(kv[0][1]), "count": kv[1]}, weg.items()))
json.dump(weg_json, sys.stdout)