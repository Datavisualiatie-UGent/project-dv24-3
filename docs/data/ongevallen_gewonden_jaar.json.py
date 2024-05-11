import csv
import json
import sys

ongevallen = {}

with open("docs/data/OPENDATA_MAP_2017-2022.csv", newline='') as f:
    csv_reader = csv.DictReader(f, delimiter=',', quotechar='"')

    i = 0
    for row in csv_reader:
        key = int(row['DT_YEAR_COLLISION'])
        ongevallen[key] = ongevallen.get(key, 0) + 1
ongevallen_json = list(map(lambda kv: {"year": kv[0], "value": kv[1]}, ongevallen.items()))
json.dump(ongevallen_json, sys.stdout)
