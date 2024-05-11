import csv
import json
import sys
import gzip

ongevallen = {}
months = ["Jan", "Feb", "Mrt", "Apr", "Mei", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dec"]

with gzip.open("docs/data/OPENDATA_MAP_2017-2022.csv.gz", mode="rt", newline='') as f:
    csv_reader = csv.DictReader(f, delimiter=',', quotechar='"')

    i = 0
    for row in csv_reader:
        key = (int(row['DT_YEAR_COLLISION']), int(row['DT_MONTH_COLLISION']) - 1)

        ongevallen[key] = ongevallen.get(key, 0) + 1

ongevallen_json = list(map(lambda kv: {"year": kv[0][0], "month": months[kv[0][1]], "month_num": kv[0][1], "value": kv[1]}, ongevallen.items()))
json.dump(ongevallen_json, sys.stdout)
