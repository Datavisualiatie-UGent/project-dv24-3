import csv
import json
import sys
import gzip

ongevallen = {}

with gzip.open("docs/data/OPENDATA_MAP_2017-2022.csv.gz", mode="rt", newline='') as f:
    csv_reader = csv.DictReader(f, delimiter=',', quotechar='"')

    i = 0
    for row in csv_reader:
        key = (row['TX_ROAD_USR_TYPE1_NL'].capitalize(), row['TX_ROAD_USR_TYPE2_NL'].capitalize())

        if "Onbekend" not in key:
            ongevallen[key] = ongevallen.get(key, 0) + 1

ongevallen_json = list(map(lambda kv: {"gebruiker_1": kv[0][0], "gebruiker_2": kv[0][1], "value": kv[1]}, ongevallen.items()))
json.dump(ongevallen_json, sys.stdout)
