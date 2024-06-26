import csv
import json
import sys
import gzip

type_ongeval = {}

with gzip.open("docs/data/OPENDATA_MAP_2017-2022.csv.gz", mode="rt", newline='') as f:
    csv_reader = csv.DictReader(f, delimiter=',', quotechar='"')

    i = 0
    for row in csv_reader:
        key = (row['TX_CLASS_ACCIDENTS_NL'], row['DT_YEAR_COLLISION'])

        if key == '':
            key = "unknown"

        type_ongeval[key] = type_ongeval.get(key, 0) + 1

type_ongeval_json = list(map(lambda kv: {"class": kv[0][0].lower(), "year": int(kv[0][1]), "count": kv[1]}, type_ongeval.items()))
json.dump(type_ongeval_json, sys.stdout)
