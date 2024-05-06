import csv
import json
import sys

bebouwde_kom = {}

with open("docs/data/OPENDATA_MAP_2017-2022.csv", newline='') as f:
    csv_reader = csv.DictReader(f, delimiter=',', quotechar='"')

    i = 0
    for row in csv_reader:
        key = (row['TX_BUILD_UP_AREA_NL'], row['DT_YEAR_COLLISION'])

        if key == '':
            key = "unknown"

        bebouwde_kom[key] = bebouwde_kom.get(key, 0) + 1

bebouwde_kom_json = list(map(lambda kv: {"area": kv[0][0].lower(), "year": int(kv[0][1]), "count": kv[1]}, bebouwde_kom.items()))
json.dump(bebouwde_kom_json, sys.stdout)