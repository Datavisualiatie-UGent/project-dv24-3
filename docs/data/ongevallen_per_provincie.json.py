import csv
import json
import sys
import gzip

ongevallen_absoluut = {}
ongevallen_per_jaar = {}
bewoners = {
    "Antwerpen": 1869730,
    "Vlaams-Brabant": 1155843,
    "Waals-Brabant": 406019,
    "West-Vlaanderen": 1200945,
    "Oost-Vlaanderen": 1525255,
    "Henegouwen": 1346840,
    "Luik": 1109800,
    "Limburg": 877370,
    "Luxemburg": 286752,
    "Namen": 495832,
}

with gzip.open("docs/data/OPENDATA_MAP_2017-2022.csv.gz", mode="rt", newline='') as f:
    csv_reader = csv.DictReader(f, delimiter=',', quotechar='"')

    for row in csv_reader:
        key = row['TX_PROV_COLLISION_NL']

        if key == '':
            key = "Unknown"

        else:
            # Provincie prefix weghalen
            key = key.split(' ')[1]

        ongevallen_absoluut[key] = ongevallen_absoluut.get(key, 0) + 1

        if key != 'Unknown':
            key = (key, row['DT_YEAR_COLLISION'])
            ongevallen_per_jaar[key] = ongevallen_per_jaar.get(key, 0) + 1

json.dump({
    "provincies": list(ongevallen_absoluut.keys()),
    "absoluut": [
        {"provincie": kv[0], "value": kv[1]}
        for kv in ongevallen_absoluut.items()
    ],
    "capita": [
        {"provincie": prov, "jaar": year, "value": value / bewoners[prov]}
        for ((prov, year), value) in sorted(ongevallen_per_jaar.items())
    ],
}, sys.stdout)
