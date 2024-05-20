# Data-visualisatie - Groep 3

* Emma Neirinck
* Robbe Van Rijsselberghe
* Jef Roosens

## Introductie

Deze repository bevat onze visualisatie van de dataset [*Geolocalisatie van de
verkeersongevallen
2017-2022*](https://statbel.fgov.be/nl/open-data/geolocalisatie-van-de-verkeersongevallen-2017-2022).
De dataset bevat ongevallen met lichamelijke letsels, geregistreerd door de
federale politie tussen 2017 en 2022.

## Project

Voor dit project hebben we gebruik gemaakt van [Observable
Framework](https://observablehq.com/framework), een JavaScript framework die
toelaat interactieve webpagina's op te bouwen gevuld met visualisaties voor een
dataset.

Aangezien de originele dataset aangeboden werd als een Excel-bestand hebben we
dit eerst omgezet naar een CSV. De Gzip-compressed versie van dit bestand kan
gedownload worden op <http://r8r.be/dv_dataset>. Dit bestand moet geplaatst
worden in `docs/data/OPENDATA_MAP_2017-2022.csv.gz`

Hierna kan de lokale development server opgestart worden. Hiervoor moet men
enkel dit uitvoeren:

```
npm run dev
```

Hierna is het project lokaal beschikbaar op <http://localhost:3000>. Voor meer
informatie over hoe Observable werkt kan mijn de [Getting
Started](https://observablehq.com/framework/getting-started) pagina bekijken.
