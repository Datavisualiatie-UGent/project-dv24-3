import csv
import json
import sys
import numpy as np

columns = [
    ('TX_CROSSWAY_NL', 'Kruispunt'),
    ('TX_WEATHER_NL', 'Weersomstandigheden'),
    ('TX_ROAD_CONDITION_NL', 'Wegconditie'),
    ('TX_BUILD_UP_AREA_NL', 'Bebouwde kom'),
    ('TX_LIGHT_CONDITION_NL', 'Lichtconditie'),
    ('TX_CLASS_ACCIDENTS_NL', 'Type ongeval'),
    ('CD_ROAD_TYPE_NL', 'Type weg'),
]

data = [[] for _ in columns]
possible_values = [[] for _ in columns]

with open("docs/data/OPENDATA_MAP_2017-2022.csv", newline='') as f:
    csv_reader = csv.DictReader(f, delimiter=',', quotechar='"')

    for row in csv_reader:
        for i, (key, _) in enumerate(columns):
            value = row[key]

            try:
                index = possible_values[i].index(value)

            except ValueError:
                index = len(possible_values[i])
                possible_values[i].append(value)

            data[i].append(index)

arr = np.array(data)
corr_matrix = np.corrcoef(arr)

output = []

for i, (_, k1) in enumerate(columns):
    for j, (_, k2) in enumerate(columns):
        output.append({
            "column_1": k1,
            "column_2": k2,
            "value": corr_matrix[i][j]
        })

json.dump(output, sys.stdout)
