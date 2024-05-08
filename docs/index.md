---
theme: light
toc: true
---
````js
import proj4 from "npm:proj4";
import {legend, color_mapping, add_color_to_data} from "./components/legends.js"
````

# Verkeersongelukken
---

````js
const rawdata = await FileAttachment("data/OPENDATA_MAP_2017-2022.csv").csv()
````

## Heatmap: Gekende ongevallen met gewonden per maand per jaar

```js
const ongevallen_per_maand_jaar = await FileAttachment("data/ongevallen_gewonden_maand_jaar.json").json();

const months = ["Jan", "Feb", "Mrt", "Apr", "Mei", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dec"];

const colorScheme = [
'#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080'
];
```

````js
Plot.plot({
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
            {x: "year", y: "month", fill: "value", tip: true}
        )
    ]
})
````

## Waffle chart: Aantal ongevallen met gewonden per provincie 

````js
const ongevallen_per_provincie = await FileAttachment("data/ongevallen_per_provincie.json").json();

let units = ongevallen_per_provincie
    .map((v) => ({group: v.provincie, label: v.provincie, freq: v.value}))
    .flatMap(d => d3.range(Math.round(d.freq / 1000)).map(() => d))
    .sort( (d1, d2) => d2.freq - d1.freq);
````

<div style="display:flex; height: 400px">
  <div style="flex: 0 0 60%">
    ${Plot.plot({
    aspectRatio: 1,
    insetRight: 50,
  marks: [
    Plot.cell(
        units,
      Plot.stackX({
        y: (_, i) => Math.floor(i/20),
        fill: "label",
        title: "group"
      })
    )
  ],
  x: { axis: null },
  y: { axis: null },
  color: { values: colorScheme }
})}
  </div>
  <div style="flex: 0 0 20%">
  <h3>1 unit = 1000 accidents</h3>
    ${legend(color_mapping([...new Set(ongevallen_per_provincie.map(d => d.provincie))], colorScheme))}
  </div>
</div>

## Heatmap: Ongevallen per betrokken weggebruiker / obstakel
### logaritmische kleurschaal
```js
const ongevallen_per_weggebruiker = await FileAttachment("data/ongevallen_per_betrokken_weggebruiker.json").json();
```

<div>
${Plot.plot({
    color: {legend: true, scheme: "Oranges", type: "log"},
    aspectRatio: 2.5,
    marginTop: 0,
    marginLeft: 300,
    marginBottom: 120,
    marginRight: 100,
    xscale: {type: "band"},
    x: {type: "band", label: "Weggebruiker 1", tickRotate: 45},
    y: {label: "Weggebruiker 2"},
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
})}
</div>


## Line chart: Type slachtoffer in ongevallen met gewonden

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
    ${view(select_input)}
    <div style="padding-top: 20px;"></div>
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
    ${legend(legend_selector[value_select])}
  </div>
</div>



## Kaart: Type slachtoffer met locatie

```js
const belgium = await FileAttachment("data/Gemeenten_Fusies.json").json()

const geolocations = rawdata.map(d => ({
    x: parseFloat(d.MS_X_COORD),
    y: parseFloat(d.MS_Y_COORD),
    type: d.TX_CLASS_ACCIDENTS_NL.toLowerCase()
})).filter(d => isFinite(d.x) && isFinite(d.y));
```

```js
proj4.defs("EPSG:31370", "+proj=lcc +lat_0=90 +lon_0=4.36748666666667 +lat_1=51.1666672333333 +lat_2=49.8333339 +x_0=150000.013 +y_0=5400088.438 +ellps=intl +towgs84=-106.8686,52.2978,-103.7239,-0.3366,0.457,-1.8422,-1.2747 +units=m +no_defs +type=crs");
const geographic_coordinates = geolocations.map(d => {
    const transformedCoordinates = proj4('EPSG:31370', 'EPSG:4326', [d.x, d.y]);
    return { coordinates: transformedCoordinates, type: d.type };
    });
```

```js
const colorScale = d3.scaleOrdinal()
        .domain(geographic_coordinates.map(d => d.type))
        .range(d3.schemeCategory10);
```

```js
function map(value) {
  const width = 1000;
  const height = 800;
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
    
    // Filter geographic coordinates based on the provided value
    let filteredCoordinates = geographic_coordinates.filter(d => value.includes(d.type));
    
    // Draw filtered coordinates
    for (const obj of filteredCoordinates.reverse()) {
      context.beginPath();
      context.fillStyle = colorScale(obj.type);
      const [x, y] = obj.coordinates.values();
      const [proj_x, proj_y] = projection([x, y]);
      context.moveTo(proj_x + r, proj_y);
      context.arc(proj_x, proj_y, r, 0, 2 * Math.PI);
      context.fill();
    }
    context.restore();
  }

  zoomed(d3.zoomIdentity);
  
  return context.canvas;
}
```

```js
const distinct_types = [...new Set(geolocations.map(d => d.type))];
```

```js
const input = view(Inputs.checkbox(distinct_types, {
  description: 'Choose the type to display on the map',
  value: distinct_types
}));
```

```js
view(map(input));
```


## TODO: Correlatiematrix?

