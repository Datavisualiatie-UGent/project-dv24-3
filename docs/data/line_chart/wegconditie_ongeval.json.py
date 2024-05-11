import csv
import json
import sys

weg = {}

group = {
    "droog": "droog",
    "onbekend": "onbekend",
    "nat, plassen": "nat, plassen",
    "ijzel, sneeuw": "ijzel, sneeuw",
    "proper": "proper",
    "droog+proper": "droog + proper",
    "droog+vuil (zand, grint, bladeren,...)": "droog + vuil",
    "nat, plassen+proper": "nat, plassen + proper",
    "nat, plassen+ijzel of sneeuw": "nat, plassen + ijzel of sneeuw",
    "nat, plassen+vuil (zand, grint, bladeren,...)": "nat, plassen + vuil",
    "vuil (zand, grint, bladeren,...)": "vuil",
    "ijzel, sneeuw+ roper": "ijzel, sneeuw + proper",
    "ijzel, sneeuw+vuil (zand, grint, bladeren,...)": "ijzel, sneeuw + vuil"
}

with open("docs/data/OPENDATA_MAP_2017-2022.csv", newline='') as f:
    csv_reader = csv.DictReader(f, delimiter=',', quotechar='"')

    i = 0
    for row in csv_reader:
        key = (group[row['TX_ROAD_CONDITION_NL'].lower()], row['DT_YEAR_COLLISION'])

        if key == '':
            key = "unknown"

        weg[key] = weg.get(key, 0) + 1

weg_json = list(map(lambda kv: {"cond": kv[0][0].lower(), "year": int(kv[0][1]), "count": kv[1]}, weg.items()))
json.dump(weg_json, sys.stdout)