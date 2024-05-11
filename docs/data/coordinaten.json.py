import csv
import json
import sys
import gzip

coordinates = {}

with gzip.open("docs/data/OPENDATA_MAP_2017-2022.csv.gz", mode="rt", newline='') as f:
    csv_reader = csv.DictReader(f, delimiter=',', quotechar='"')

    for row in csv_reader:
        ongeval_type = row['TX_CLASS_ACCIDENTS_NL'].lower()

        x, y = row['MS_X_COORD'], row['MS_Y_COORD']

        if not (x and y):
            continue

        data = {
            'x': float(x),
            'y': float(y)
        }

        if ongeval_type not in coordinates:
            coordinates[ongeval_type] = []

        coordinates[ongeval_type].append({
            'x': float(row['MS_X_COORD']),
            'y': float(row['MS_Y_COORD'])
        })

json.dump({
    "distinct_types": list(coordinates.keys()),
    "coordinates": coordinates
}, sys.stdout)
