import csv
import json
import sys

weer = {}

group = {'normaal': 'normaal', 
         'onbekend': 'onbekend', 
         'sneeuwval': 'sneeuwval', 
         'regenval': 'regenval', 
         'hagelbui': 'hagelbui', 
         'mist (zichtbaarheid minder dan 100m)': 'mist', 
         'sneeuwval+hagelbui': 'sneeuwval + hagelbui', 
         'andere (dikke rook,...)': 'andere', 
         'sterke wind, rukwind+sneeuwval': 'sterke wind + sneeuwval', 
         'regenval+sneeuwval': 'regenval + sneeuwval', 
         'sterke wind, rukwind': 'sterke wind', 
         'regenval+sterke wind, rukwind': 'regenval + sterke wind', 
         'regenval+mist (zichtbaarheid minder dan 100m)': 'regenval + mist', 
         'regenval+hagelbui': 'regenval + hagelbui', 
         'regenval+andere (dikke rook,...)': 'regenval + andere', 
         'sterke wind, rukwind+hagelbui' : 'sterke wind + hagelbui'
         }

with open("docs/data/OPENDATA_MAP_2017-2022.csv", newline='') as f:
    csv_reader = csv.DictReader(f, delimiter=',', quotechar='"')

    i = 0
    for row in csv_reader:
        key = (group[row['TX_WEATHER_NL'].lower()], row['DT_YEAR_COLLISION'])

        if key == '':
            key = "unknown"

        weer[key] = weer.get(key, 0) + 1

weer_json = list(map(lambda kv: {"weather": kv[0][0].lower(), "year": int(kv[0][1]), "count": kv[1]}, weer.items()))
json.dump(weer_json, sys.stdout)