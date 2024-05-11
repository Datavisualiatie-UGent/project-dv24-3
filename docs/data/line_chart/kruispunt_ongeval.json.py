import csv
import json
import sys
import gzip

kruispunt = {}

with gzip.open("docs/data/OPENDATA_MAP_2017-2022.csv.gz", mode="rt", newline='') as f:
    csv_reader = csv.DictReader(f, delimiter=',', quotechar='"')

    i = 0
    for row in csv_reader:
        key = (row['TX_CROSSWAY_NL'], row['DT_YEAR_COLLISION'])

        if key == '':
            key = "unknown"

        kruispunt[key] = kruispunt.get(key, 0) + 1

kruispunt_json = list(map(lambda kv: {"cross": kv[0][0].lower(), "year": int(kv[0][1]), "count": kv[1]}, kruispunt.items()))
json.dump(kruispunt_json, sys.stdout)
