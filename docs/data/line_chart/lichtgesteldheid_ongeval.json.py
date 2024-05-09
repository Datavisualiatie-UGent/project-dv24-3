import csv
import json
import sys

licht = {}

group = {'nacht, openbare verlichting aanwezig en ontstoken': 'nacht, verlichting aanwezig en ontstoken', 
         'onbekend': 'onbekend', 
         'dag': 'dag', 
         'dageraad - schemering': 'dageraad - scherming', 
         'nacht, geen openbare verlichting aanwezig': 'nacht, geen verlichting aanwezig', 
         'nacht, openb. verlicht. aanw., maar niet ontstoken': 'nacht, verlichting aanwezig en niet ontstoken'
}

with open("docs/data/OPENDATA_MAP_2017-2022.csv", newline='') as f:
    csv_reader = csv.DictReader(f, delimiter=',', quotechar='"')

    i = 0
    for row in csv_reader:
        key = (group[row['TX_LIGHT_CONDITION_NL'].lower()], row['DT_YEAR_COLLISION'])

        if key == '':
            key = "unknown"

        licht[key] = licht.get(key, 0) + 1

licht_json = list(map(lambda kv: {"light": kv[0][0].lower(), "year": int(kv[0][1]), "count": kv[1]}, licht.items()))
json.dump(licht_json, sys.stdout)