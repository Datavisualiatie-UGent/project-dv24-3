---
theme: dark
toc: true
---

# Verkeersongelukken

Introstukje

## Title 1

````js
const rawdata = await FileAttachment("data/OPENDATA_MAP_2017-2022.csv").csv()
const data = rawdata.map((d, i) => {
    d.DT_YEAR_COLLISION = d.DT_YEAR_COLLISION;
    d.DT_MONTH_COLLISION = parseInt(d.DT_MONTH_COLLISION);
    return d;
})
/*    .filter((d, i) => d.CD_ROAD_USR_TYPE1 < 99 && d.CD_ROAD_USR_TYPE2 < 99).map((d, i) => {
    d.DT_YEAR_COLLISION = d.DT_YEAR_COLLISION;
    d.DT_MONTH_COLLISION = parseInt(d.DT_MONTH_COLLISION);
    return d;
}) */
````

````js
Plot.plot({
    color: {legend: true, scheme: "Oranges"},
    marginTop: 0,
    insetRight: 0,
    xscale: "band",
    x: {type: "band"},
    y: {},
    title: "Gekende ongevallen met gewonden per maand per jaar",
    marks: [
        Plot.cell(
            data,
            Plot.group(
                {fill: "count"},
                {x: "DT_YEAR_COLLISION", y: "DT_MONTH_COLLISION", tip: true}
            )
        )
    ]
})
````

````js
const slider = view(Inputs.range([2017, 2022], {value: 5, step: 1, label: "Jaar"}))
// html`<p>slider</p>`
// view(sliderb = html`<input type="range" value=42 min=0 max=23 step=1></input>`)
// html`<p>${slider}</p>`
````

````js
view(slider)
````

## waffle chart

````js
const provdata = data.map((d,i) => d.TX_PROV_COLLISION_NL)
let provuniqedata = {}
provdata.forEach((d, i) => provuniqedata[d] = (provuniqedata[d] || 0) + 1)
let units = [];
Object.keys(provuniqedata).forEach((key, index) => {
    let label = key
    if (key == ""){
        label = "unknown"
    }
    units.push({group: label, label: label, freq: provuniqedata[key]})
})
console.log(units)
units = units.flatMap(d => d3.range(Math.round(d.freq / 1000)).map(() => d))
units = units.sort( (d1, d2) => d2.freq - d1.freq)
console.log(units)
````
### 1 unit = 1000 accidents
````js
Plot.plot({
  marks: [
    Plot.cell(
        units,
      Plot.stackX({
        y: (_, i) => Math.floor(i/10),
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

## Type bestuurders dat ongevallen hebben
# logaritmische kleurschaal
````js
Plot.plot({
    color: {legend: true, scheme: "Oranges", type: "log"},
    marginTop: 0,
    insetRight: 0,
    xscale: "band",
    x: {type: "band"},
    y: {},
    title: "ongevallen per betrokken bestuurders",
    marks: [
        Plot.cell(
            data,
            Plot.group(
                {fill: "count"},
                {x: "TX_ROAD_USR_TYPE1_NL", y: "TX_ROAD_USR_TYPE2_NL", tip: true}
            )
        )
    ]
})
````


## Title 2

````js
Plot.plot({
    y: {grid: true},
    color: {legend: true},
    marks: [
        Plot.rectY(data, Plot.binX({y: "count"}, {
            x: "DT_YEAR_COLLISION",
            fill: "TX_CLASS_ACCIDENTS_NL",
            insetLeft: -4,
            insetRight: -4
        })),
        Plot.ruleY([0])
    ],
    xAxis: {tickFormat: d3.format("d")}
})
````

## Binnen en buiten bebouwde kom

````js
Plot.plot({
    y: {grid: true},
    color: {legend: true},
    marks: [
        Plot.rectY(data, Plot.binX({y: "count"}, {
            x: "DT_YEAR_COLLISION",
            fill: "TX_BUILD_UP_AREA_NL",
            insetLeft: -4,
            insetRight: -4
        })),
        Plot.ruleY([0])
    ],
    xAxis: {tickFormat: d3.format("d")}
})
````

## ongevallen op kruispunt en niet op kruispunt

````js
Plot.plot({
    y: {grid: true},
    color: {legend: true},
    marks: [
        Plot.rectY(data, Plot.binX({y: "count"}, {
            x: "DT_YEAR_COLLISION",
            fill: "TX_CROSSWAY_NL",
            insetLeft: -4,
            insetRight: -4
        })),
        Plot.ruleY([0])
    ],
    xAxis: {tickFormat: d3.format("d")}
})
````
## Weersomstandigheden bij ongevallen

````js
Plot.plot({
    y: {grid: true},
    color: {legend: true},
    marks: [
        Plot.rectY(data, Plot.binX({y: "count"}, {
            x: "DT_YEAR_COLLISION",
            fill: "TX_WEATHER_NL",
            insetLeft: -4,
            insetRight: -4
        })),
        Plot.ruleY([0])
    ],
    xAxis: {tickFormat: d3.format("d")}
})
````

## Wegconditie bij ongevallen

````js
Plot.plot({
    y: {grid: true},
    color: {legend: true},
    marks: [
        Plot.rectY(data, Plot.binX({y: "count"}, {
            x: "DT_YEAR_COLLISION",
            fill: "TX_ROAD_CONDITION_NL",
            insetLeft: -4,
            insetRight: -4
        })),
        Plot.ruleY([0])
    ],
    xAxis: {tickFormat: d3.format("d")}
})
````

## Lichtgesteldheid bij ongevallen

````js
Plot.plot({
    y: {grid: true},
    color: {legend: true},
    marks: [
        Plot.rectY(data, Plot.binX({y: "count"}, {
            x: "DT_YEAR_COLLISION",
            fill: "TX_LIGHT_CONDITION_NL",
            insetLeft: -4,
            insetRight: -4
        })),
        Plot.ruleY([0])
    ],
    xAxis: {tickFormat: d3.format("d")}
})
````
## Type weg bij ongevallen

````js
Plot.plot({
    y: {grid: true},
    color: {legend: true},
    marks: [
        Plot.rectY(data, Plot.binX({y: "count"}, {
            x: "DT_YEAR_COLLISION",
            fill: "CD_ROAD_TYPE_NL",
            insetLeft: -4,
            insetRight: -4
        })),
        Plot.ruleY([0])
    ],
    xAxis: {tickFormat: d3.format("d")}
})
````

## Title 3

````js

const belgium = await FileAttachment("data/Gemeenten_Fusies.json").json()

const width = 600
const height = 600

// Create an SVG element
const svg = d3.create("svg").attr("viewBox", [0, 0, width, height]);

// Create a projection for Belgium
const projection = d3.geoMercator().fitSize([width, height], topojson.feature(belgium, belgium.objects.Gemeenten));

// Create a path generator
const path = d3.geoPath().projection(projection);

// Render the map
svg.append("path")
    .datum(topojson.feature(belgium, belgium.objects.Gemeenten))
    .attr("d", path)
    .attr("fill", "lightgray")
    .attr("stroke", "white");

// Display the map
svg.node()

````



