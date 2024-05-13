---
theme: air
toc: true
---

````js
import proj4 from "npm:proj4";
import {legend, color_mapping, add_color_to_data} from "./components/legends.js"
````

<div style="width: 80%; background-color: #F0F0F0; padding : 15px; padding-left: 25px">
<h1>Verkeersongelukken</h1>
<p style="font-size: 12px">Door Robbe Van Rijsselberghe, Emma Neirinck & Jef Roosens</p>
<div style = "width: 100%">
Helaas blijven er jaarlijks nog steeds tal van ongevallen plaatsvinden. StatBel, het Belgische statistiekbureau, biedt een <a href="https://statbel.fgov.be/nl/open-data/geolocalisatie-van-de-verkeersongevallen-2017-2022">dataset</a> aan die verkeersongevallen van 2017 tot 2022 opsomt. Deze dataset is samengesteld op basis van ongevallen geregistreerd door de federale politie, maar het is belangrijk om te vermelden dat de dataset enkel ongevallen bevat waar doden of gewonden waren. Het doel van deze visualisatie is meer inzicht creëren in de data, en aantonen waar eventueel veiligere situaties moeten voorzien worden.
</div>

</div>
<br>
<br>

```js
const ongevallen_per_jaar = await FileAttachment("data/ongevallen_gewonden_jaar.json").json();
```


### Aantal ongevallen met gewonden of doden per jaar
<div style="width: 80%;">
    Een opvallende trend wordt direct duidelijk in de eerste grafiek: aanzienlijk minder ongevallen in 2020. De verklaring hiervoor is eenvoudig: de coronapandemie. Mensen werden aangemoedigd om zoveel mogelijk thuis te blijven en vanuit huis te werken. Hierdoor waren er veel minder voertuigen op de weg, wat resulteerde in aanzienlijk minder ongevallen.
</div>

```js
Plot.plot({
    x: {grid: true, domain: [0, 43000], label: "Aantal ongevallen"},
    y: {label: "Jaar", tickFormat: ""},
    height: 300,
    marginTop: 0,
    marginLeft: 50,
    color: {scheme: "spectral", type: "ordinal"},
    marks: [
        Plot.barX(
            ongevallen_per_jaar,
            {x: "value", y:"year", tip:true, fill: "year"}
        ),
        Plot.ruleX([0])
    ]
})
```
<br>
<br>

### Aantal ongevallen met gewonden of doden per maand per jaar

```js
const ongevallen_per_maand_jaar = await FileAttachment("data/ongevallen_gewonden_maand_jaar.json").json();

const months = ["Jan", "Feb", "Mrt", "Apr", "Mei", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dec"];

const colorScheme = [
'#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080'
];
```
<div style="display:flex; width: 80%">
  <div style="flex: 0 0 60%">
  <br>
  <br>
  De volgende visualisatie presenteert het aantal ongevallen per maand over de jaren heen. Voor deze weergave hebben we geopteerd voor een heatmap, waardoor de relatieve frequenties van ongevallen in verschillende periodes in één oogopslag kunnen worden vergeleken.

  Opmerkelijk is dat 2020 aanzienlijk minder ongevallen kent dan andere jaren, waarbij april 2020 veruit het laagste aantal ongevallen registreerde. Dit valt samen met het begin van de Covid-19-pandemie, toen mensen strikt de regels volgden en alleen naar buiten gingen wanneer dit absoluut noodzakelijk was.

  Verder valt ook op dat er een duidelijke daling te zien is in het aantal ongevallen vanaf juli en augustus, gedurende alle jaren. Deze neerwaartse trend kan worden toegeschreven aan de zomervakantieperiode, waarin veel mensen ervoor kiezen om hun vakantiedagen op te nemen. Het gevolg hiervan is dat er minder verkeer op de wegen is, waardoor het risico op ongevallen aanzienlijk vermindert.

  </div>
  <div>
    ${Plot.plot({
       width: 350,
      height: 600,
      color: {legend: true, scheme: "Oranges"},
      marginTop: 0,
      aspectRatio: 1,
      xscale: "band",
      x: {type: "band", label: "Jaar", tickFormat: ""},
      y: {
          domain: months,
          label: "Maand"},
      marks: [
          Plot.cell(
              ongevallen_per_maand_jaar,
              {x: "year", y: "month", fill: "value", tip: {format: {x: (y) => `${y}`, y: true, value: true}}}
          )
      ]
    })}
  </div>
</div>

<br>
<br>

### Geolocaties ongevallen

<div style="width: 80%">
Hier presenteren we op een kaart alle locaties waar ongevallen met gewonden hebben plaatsgevonden. Aangezien personenwagens verantwoordelijk zijn voor het merendeel van deze ongevallen, is het niet verrassend dat de datapunten een gedetailleerd beeld vormen van het Belgische wegennet.
Aangezien de weergave van alle ongevallen op één kaart wellicht wat overweldigend kan zijn, bieden we de mogelijkheid om specifieke categorieën van slachtoffers in of uit te schakelen.
</div>

```js
const belgium = await FileAttachment("data/Gemeenten_Fusies.json").json()
const coordinates = await FileAttachment("data/coordinaten.json").json()
```

```js
proj4.defs("EPSG:31370", "+proj=lcc +lat_0=90 +lon_0=4.36748666666667 +lat_1=51.1666672333333 +lat_2=49.8333339 +x_0=150000.013 +y_0=5400088.438 +ellps=intl +towgs84=-106.8686,52.2978,-103.7239,-0.3366,0.457,-1.8422,-1.2747 +units=m +no_defs +type=crs");

for (const type of coordinates.distinct_types) {
    coordinates.coordinates[type] = coordinates.coordinates[type].map(d => {
        const transformed = proj4('EPSG:31370', 'EPSG:4326', [d.x, d.y]);

        return {x: transformed[0], y: transformed[1]};
    });
}
```

```js
const colorScale = d3.scaleOrdinal()
        .domain(coordinates.distinct_types)
        .range(d3.schemeCategory10);
console.log(colorScale)
const legend_map = color_mapping(coordinates.distinct_types, d3.schemeCategory10);
```


```js
function map(value) {
  const width = 800;
  const height = 600;
  const r = 1.5;
  const projection = d3.geoMercator().fitSize([width, height], topojson.feature(belgium, belgium.objects.Gemeenten));
  const canvas = d3.create("canvas")
      .attr("width", width)
      .attr("height", height);
  const context = canvas.node().getContext('2d');
  const path = d3.geoPath(null, context).projection(projection);

  d3.select(context.canvas).call(d3.zoom()
      .scaleExtent([1, 8])
      .on("zoom", ({transform}) => zoomed(transform)));

  function zoomed(transform) {
    context.save();
    context.clearRect(0, 0, width, height);
    context.fillStyle = "#F0F0F0";
    context.fillRect(0, 0, width, height);
    context.translate(transform.x, transform.y);
    context.scale(transform.k, transform.k);
    context.canvas.style.maxWidth = "100%";
    context.lineJoin = "round";
    context.lineCap = "round";

    context.beginPath();
    path(topojson.feature(belgium, belgium.objects.Gemeenten));
    context.fillStyle = "lightgray";
    context.fill();

    context.beginPath();
    path(topojson.feature(belgium, belgium.objects.Gemeenten, (a, b) => a !== b ));
    context.lineWidth = 0.5;
    context.strokeStyle = "white";
    context.stroke();

    for (const type of coordinates.distinct_types) {
        if (value.includes(type)) {
            for (const obj of coordinates.coordinates[type]) {
                context.beginPath();
                context.fillStyle = colorScale(type);
                const [proj_x, proj_y] = projection([obj.x, obj.y]);
                context.moveTo(proj_x + r, proj_y);
                context.arc(proj_x, proj_y, r, 0, 2 * Math.PI);
                context.fill();
            }
        }
    }
    
    context.restore();
  }

  zoomed(d3.zoomIdentity);

  return context.canvas;
}
```

```js
const input = view(Inputs.checkbox(coordinates.distinct_types, {
  description: 'Choose the type to display on the map',
  value: coordinates.distinct_types
}));
```

<div style="display:flex">
  <div style="flex: 0 0 80%">
    ${view(map(input))}
  </div>
  <div style="flex: 0 0 20%; padding-left: 30px">
    <b>Legende</b>
    ${legend(legend_map)}
  </div>
</div>

<br>
<br>

### Aantal ongevallen per provincie 

<div style="width: 80%">
Hier tonen we de verdeling van het totale aantal ongevallen over de verschillende provincies, relatief ten opzichte van het aantal inwoners. Opmerkelijk is dat Oost-Vlaanderen gemiddeld het hoogste aantal ongevallen per inwoner heeft.
<br>
Over het algemeen lijkt het er ook op dat de Waalse provincies het beter doen dan de Vlaamse. Dit fenomeen kan mogelijk worden verklaard door de aanwezigheid van meer uitgestrekte landelijke gebieden in Wallonië in vergelijking met de meer stedelijke omgevingen in Vlaanderen. Daarom is het aannemelijk dat de lagere bevolkingsdichtheid in combinatie met andere factoren, zoals infrastructuur in Wallonië een rol speelt bij het verminderen van het aantal ongevallen.
</div>
<br>

````js
const ongevallen_per_provincie = await FileAttachment("data/ongevallen_per_provincie.json").json();

let sorted_provincies = ongevallen_per_provincie.absoluut
    .map(d => d.provincie)
    .sort((p1, p2) => p1.localeCompare(p2)
);
let units = ongevallen_per_provincie.absoluut
    .flatMap(d => d3.range(Math.round(d.value / 1000)).map(() => d))
    .sort((d1, d2) => d2.value - d1.value);
const mapped_colors = color_mapping(sorted_provincies, colorScheme);
````

<div style="display:flex; height: 400px">
  <div style="flex: 0 0 60%">
    ${Plot.plot({
    aspectRatio: 1,
  marks: [
    Plot.cell(
        units,
      Plot.stackX({
        y: (_, i) => Math.floor(i/20),
        fill: "provincie",
        title: "provincie"
      })
    )
  ],
  x: { axis: null },
  y: { axis: null },
  color: {sorted_provincies, type: "categorical", range: colorScheme }
})}
  </div>
  <div style="flex: 0 0 20%">
    <b>Legende</b>
    ${legend(mapped_colors)}
  </div>
</div>

<br>
<br>

### Ongevallen per capita
<div style="width: 80%">
Bovenstaande waffle chart toont de absolute aantallen van ongevallen verdeeld
over de verschillende provincies. Dit kan echter een vertekend beeld geven,
aangezien niet elke provincie even groot is, waardoor grotere provincies er dus
slechter kunnen uitzien door het hogere aantal ongevallen.
<br>
<br>
Onderstaande grafiek vergelijkt de ongevallen per capita, verrekend met de
bevolkingsaantallen van elke provincie voor het jaar 2021. Hier zien we wederom
de duidelijke daling in ongevallen in het jaar 2020. Wat we echter ook kunnen
waarnemen is dat Oost- en West-Vlaanderen en Antwerpen beduidend meer
ongevallen per capita hebben dan de andere provincies. Henegeouwen bijvoorbeeld
was volgende de absolute aantallen de slechtste leerling na de drie grote
provincies, maar per capita is het samen met Vlaams- en Waals-Brabant een van
de laagst-scorende provincies.
</div>

```js
Plot.plot({
  width: 800,
  marginBottom: 50,
  marginRight: 50,
  x: {axis: null},
  fx: {tickRotate: 15, label: ""},
  y: {grid: true},
  color: {scheme: "spectral", legend: true, type: "ordinal"},
  marks: [
    Plot.barY(ongevallen_per_provincie.capita, {
        x: "jaar",
        y: "value",
        fill: "jaar",
        fx: "provincie",
        sort: {x: null, color: null, fx: {value: "-y", reduce: "sum"}},
        tip: true
    }),
    Plot.ruleY([0])
  ]
})
```

<br>
<br>

### Ongevallen per betrokken weggebruiker / obstakel
<div style="width: 80%">
De dataset bevat voor elk ongeval ook informatie over de twee betrokken
partijen. Met onderstaande heatmap visualiseren we welke combinaties van
partijen er het vaakst voorkomen in de dataset. Op de X as staat de primaire bestuurder.
Dit is de bestuurder die een ongeval heeft gehad. Op de Y as staan andere betrokken bestuurders of obstakels.
Het kleur geeft aan hoeveel zo een type ongeval is geregistreerd. Opgelet: het is een logaritmische kleurschaal.
<br>
<br>
Hier zien we dat de personenwagen veruit de grootste partij is, gecombineerd
met een andere personenwagen, een fietser, of een hindernis. Dit laatste
betekent dat de personenwagen niet tegen een ander voertuig is gereden, maar
tegen een object of gebouw.
Daarnaast is het ook zichtbaar dat fietsers een grote groep van primaire bestuurders zijn.
Deze hebben dan hoofdzakelijk ongevallen met personenwagens en andere fietsers
</div>

```js
const ongevallen_per_weggebruiker = await FileAttachment("data/ongevallen_per_betrokken_weggebruiker.json").json();
```

```js
Plot.plot({
    color: {legend: true, scheme: "Oranges", type: "log"},
    aspectRatio: 2.5,
    marginTop: 0,
    marginLeft: 300,
    marginBottom: 120,
    marginRight: 100,
    xscale: {type: "band"},
    x: {type: "band", label: "Primaire bestuurder", tickRotate: 55},
    y: {label: "Obstakel of ander voertuig"},
    style: {
        fontSize: 12,
    },
    //title: "Ongevallen per betrokken bestuurders",
    marks: [
        Plot.cell(
            ongevallen_per_weggebruiker,
            {x: "gebruiker_1", y: "gebruiker_2", fill: "value", tip: true}
        )
    ]
})
```

<br>
<br>

### Explore it yourself
<div style="width: 80%">
De volgende visualisatie is interactief: je hebt de mogelijkheid om een onderwerp te kiezen, zoals gewonden of kruispunten, en vervolgens de beschikbare gegevens hierover te verkennen. Een interessante observatie is bijvoorbeeld dat het merendeel van de ongevallen plaatsvindt op gewestwegen of gemeentewegen, en niet op autosnelwegen!
<br>
Aangezien sommige onderwerpen een groot aantal categorieën hebben, bieden we de optie om specifieke waarden uit te schakelen, waardoor het eenvoudiger wordt om verschillen te identificeren.
</div>

```js
const type_gewonden_ongeval = await FileAttachment("data/line_chart/type_gewonden_ongeval.json").json();
const distinct_type_victim = [...new Set(type_gewonden_ongeval.map(d => d.class))];

const bebouwde_kom_ongeval = await FileAttachment("data/line_chart/bebouwde_kom_ongeval.json").json();
const distinct_build_area = [...new Set(bebouwde_kom_ongeval.map(d => d.area))];

const kruispunt_ongeval = await FileAttachment("data/line_chart/kruispunt_ongeval.json").json();
const distinct_crossway = [...new Set(kruispunt_ongeval.map(d => d.cross))];

const weersomstandigheden_ongeval = await FileAttachment("data/line_chart/weersomstandigheden_ongeval.json").json();
const distinct_weather = [...new Set(weersomstandigheden_ongeval.map(d => d.weather))];

const wegconditie_ongeval = await FileAttachment("data/line_chart/wegconditie_ongeval.json").json();
const distinct_cond = [...new Set(wegconditie_ongeval.map(d => d.cond))];

const lichtgesteldheid_ongeval = await FileAttachment("data/line_chart/lichtgesteldheid_ongeval.json").json();
const distinct_light = [...new Set(lichtgesteldheid_ongeval.map(d => d.light))];

const type_weg_ongeval = await FileAttachment("data/line_chart/type_weg_ongeval.json").json();
const distinct_road = [...new Set(type_weg_ongeval.map(d => d.road))];
```

````js
const type_victim_colors_mapped = color_mapping(distinct_type_victim, colorScheme);
const type_victim_data = add_color_to_data(type_gewonden_ongeval, type_victim_colors_mapped, "class");

const build_area_colors_mapped = color_mapping(distinct_build_area, colorScheme);
const build_area_data = add_color_to_data(bebouwde_kom_ongeval, build_area_colors_mapped, "area");

const crossway_colors_mapped = color_mapping(distinct_crossway, colorScheme);
const crossway_data = add_color_to_data(kruispunt_ongeval, crossway_colors_mapped, "cross");

const weather_colors_mapped = color_mapping(distinct_weather, colorScheme);
const weather_data = add_color_to_data(weersomstandigheden_ongeval, weather_colors_mapped, "weather");

const cond_colors_mapped = color_mapping(distinct_cond, colorScheme);
const cond_data = add_color_to_data(wegconditie_ongeval, cond_colors_mapped, "cond");

const light_colors_mapped = color_mapping(distinct_light, colorScheme);
const light_data = add_color_to_data(lichtgesteldheid_ongeval, light_colors_mapped, "light");

const road_colors_mapped = color_mapping(distinct_road, colorScheme);
const road_data = add_color_to_data(type_weg_ongeval, road_colors_mapped, "road");

const legend_selector = {
    "Type gewonde" : color_mapping(distinct_type_victim, colorScheme),
    "Bebouwde kom" : color_mapping(distinct_build_area, colorScheme),
    "Kruispunt" : color_mapping(distinct_crossway, colorScheme),
    "Weersomstandigheden" : color_mapping(distinct_weather, colorScheme),
    "Conditie van de weg" : color_mapping(distinct_cond, colorScheme),
    "Lichtgestelheid" : color_mapping(distinct_light, colorScheme),
    "Type weg" : color_mapping(distinct_road, colorScheme),
    };
const selector = {
    "Type gewonde": {"key" : "class", "data": type_victim_data, "distinct": distinct_type_victim, "default": distinct_type_victim},
    "Bebouwde kom": {"key" : "area", "data": build_area_data, "distinct" : distinct_build_area, "default": distinct_build_area},
    "Kruispunt" : {"key" : "cross", "data" : crossway_data, "distinct" : distinct_crossway, "default": distinct_crossway},
    "Weersomstandigheden" : {"key" : "weather", "data": weather_data, "distinct" : distinct_weather, "default": distinct_weather.filter(v => { return !["normaal", "onbekend", "regenval"].includes(v); })},
    "Conditie van de weg" : {"key" : "cond", "data" : cond_data, "distinct" : distinct_cond, "default": distinct_cond.filter(v => { return !["droog"].includes(v); })},
    "Lichtgestelheid" : {"key" : "light", "data" : light_data, "distinct" : distinct_light, "default": distinct_light.filter(v => { return !["dag", "nacht, verlichting aanwezig en ontstoken"].includes(v); })},
    "Type weg" : {"key" : "road", "data" : road_data, "distinct" : distinct_road, "default": distinct_road}
    }

````

```js
const select_input = Inputs.select(["Type gewonde", "Bebouwde kom", "Kruispunt", "Weersomstandigheden", "Conditie van de weg", "Lichtgestelheid", "Type weg"], {value:"Type gewonde", width: 120});
const value_select = Generators.input(select_input);
```

````js
const checkbox_input = Inputs.checkbox(selector[value_select].distinct, {value: selector[value_select].default});
const values_checkbox = Generators.input(checkbox_input);
````

<div style="display:flex; height: 500px; padding-top: 20px">
  <div style="flex: 0 0 20%; padding-right: 20px;">
    <b>Selecteer type metadata</b>
    ${view(select_input)}
    <div style="padding-top: 20px;"></div>
    <b>Kies zichtbare waarden</b>
    ${view(checkbox_input)}
  </div>
  <div style="flex: 1;">
    ${Plot.plot({
      x: {label: "Jaar", tickFormat: d3.format("d"), ticks: 6},
      y: {
          label: "Aantal ongevallen",
          grid: true
      },
      marks: [
          Plot.ruleY([0]),
          Plot.lineY(selector[value_select].data.filter(d => (values_checkbox.includes(d[selector[value_select].key]))), {x: "year", y: "count", z: selector[value_select].key, stroke: "color"}),
          Plot.dot(selector[value_select].data.filter(d => (values_checkbox.includes(d[selector[value_select].key]))), { x: "year", y: "count", z: selector[value_select].key, fill: "color", size: 3, tip: true })
      ]
    })}
  </div>
  <div style="flex: 0 0 20%; padding-left: 20px; padding-top: 20px">
    <b>Legende</b>
    ${legend(legend_selector[value_select])}
  </div>
</div>

<br>
<br>

### Verbanden tussen de attributen gekend bij ongeval
<div style="width: 80%">
Om verder inzicht te krijgen in de dataset hebben we ook een correlatiematrix
berekend voor de verschillende variabelen gegeven voor elk ongeval. Een
correlatiematrix is een manier om de mogelijke verbanden tussen parameters in
een dataset te visualiseren. Hoe dichter de waarde bij 1 of -1 ligt, hoe
sterker gecorreleerd de parameters zijn, en hoe meer ze elkaar beïnvloeden.
<br>
<br>
Hier zien we echter wel dat er zeer weinig correlatie is tussen de
verschillende parameters. De enige ietwat betekenisvolle correlatie die we
kunnen zien is deze tussen het type weg en of het ongeval plaatsvond in de
bebouwde kom. Dit kan verklaard worden doordat binnen de bebouwde kom er geen
snelwegen zijn, en voornamelijk gemeentewegen.
</div>

```js
const correlaties = await FileAttachment("data/correlaties.json").json();
```

````js
Plot.plot({
    color: {legend: true, scheme: "Oranges"},
    aspectRatio: 1.4,
    marginTop: 0,
    marginLeft: 200,
    marginBottom: 120,
    xscale: {type: "band"},
    x: {type: "band", label: "Attribuut 1", tickRotate: 55},
    y: {label: "Attribuut 2"},
    style: {
        fontSize: 12,
    },
    marks: [
        Plot.cell(
            correlaties,
            {x: "column_1", y: "column_2", fill: "value", tip: true}
        )
    ]
})
````
