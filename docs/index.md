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

## Heatmap: Gekende ongevallen met gewonden per maand per jaar

```js
const ongevallen_per_maand_jaar = await FileAttachment("data/ongevallen_gewonden_maand_jaar.json").json();
```

````js
Plot.plot({
    width: 350,
    height: 600,
    color: {legend: true, scheme: "Oranges"},
    marginTop: 0,
    aspectRatio: 1,
    xscale: "band",
    x: {type: "band", label: "Jaar"},
    y: {
        tickFormat: Plot.formatMonth("nl", "short"), 
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
### 1 unit = 1000 accidents
````js
Plot.plot({
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
  color: { scheme: "Sinebow", legend: true}
})
````

## Heatmap: Ongevallen per betrokken weggebruiker / obstakel
### logaritmische kleurschaal
```js
const ongevallen_per_weggebruiker = await FileAttachment("data/ongevallen_per_betrokken_weggebruiker.json").json();
```

````js
Plot.plot({
    color: {legend: true, scheme: "Oranges", type: "log"},
    aspectRatio: 1.4,
    marginTop: 0,
    marginLeft: 200,
    marginBottom: 120,
    xscale: {type: "band"},
    x: {type: "band", label: "Weggebruiker 1", tickRotate: 55},
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
})
````


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
let colorScheme = [...new Array(20)].map(() => d3.interpolateSpectral(Math.random())).map(d => d3.color(d).formatHex());

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
    "Type gewonde": {"key" : "class", "data": type_victim_data, "distinct": distinct_type_victim},
    "Bebouwde kom": {"key" : "area", "data": build_area_data, "distinct" : distinct_build_area},
    "Kruispunt" : {"key" : "cross", "data" : crossway_data, "distinct" : distinct_crossway},
    "Weersomstandigheden" : {"key" : "weather", "data": weather_data, "distinct" : distinct_weather},
    "Conditie van de weg" : {"key" : "cond", "data" : cond_data, "distinct" : distinct_cond},
    "Lichtgestelheid" : {"key" : "light", "data" : light_data, "distinct" : distinct_light},
    "Type weg" : {"key" : "road", "data" : road_data, "distinct" : distinct_road}
    }

````

```js
const select_input = Inputs.select(["Type gewonde", "Bebouwde kom", "Kruispunt", "Weersomstandigheden", "Conditie van de weg", "Lichtgestelheid", "Type weg"], {value:"Type gewonde", width: 120});
const value_select = Generators.input(select_input);
```

````js
const checkbox_input = Inputs.checkbox(selector[value_select].distinct, {value: selector[value_select].distinct});
const values_checkbox = Generators.input(checkbox_input);
````

<div style="display:flex">
  <div style="flex: 0 0 20%; padding-right: 20px;">
    ${view(select_input)}
    <div style="padding-top: 20px;"></div>
    ${view(checkbox_input)}
  </div>
  <div> 
    ${legend(legend_selector[value_select])}
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
</div>


## Kaart: Type slachtoffer met locatie

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

```js
view(map(input));
```


## TODO: Correlatiematrix?

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
