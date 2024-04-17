---
theme: light
toc: true
---

# Verkeersongelukken

Introstukje

## Title 1

````js
const rawdata = await FileAttachment("data/OPENDATA_MAP_2017-2022.csv").csv()
const data = rawdata.filter((d, i) => d.CD_ROAD_USR_TYPE1 < 99 && d.CD_ROAD_USR_TYPE2 < 99).map((d, i) => {
    d.DT_YEAR_COLLISION = d.DT_YEAR_COLLISION;
    d.DT_MONTH_COLLISION = parseInt(d.DT_MONTH_COLLISION);
    return d;
})
````

````js
Plot.plot({
    color: { legend: true, scheme: "Oranges" },
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
                { fill: "count" },
                { x: "DT_YEAR_COLLISION", y: "DT_MONTH_COLLISION", tip: true }
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


## Title 2

````js
Plot.plot({
  y: {grid: true},
  color: {legend: true},
  marks: [
    Plot.rectY(data, Plot.binX({y: "count"}, {x: "DT_YEAR_COLLISION", fill: "TX_CLASS_ACCIDENTS_NL", insetLeft: -4, insetRight: -4 })),
    Plot.ruleY([0])
  ],
  xAxis: {tickFormat: d3.format("d")}
})
````

## Title 3

````js

import proj4 from "npm:proj4";

const belgium = await FileAttachment("data/Gemeenten_Fusies.json").json()

const geolocations = rawdata.map(d => ({
    x: parseFloat(d.MS_X_COORD),
    y: parseFloat(d.MS_Y_COORD),
    type: d.TX_CLASS_ACCIDENTS_NL.toLowerCase()
}));

const width = 1200;
const height = 1000;

proj4.defs("EPSG:31370", "+proj=lcc +lat_0=90 +lon_0=4.36748666666667 +lat_1=51.1666672333333 +lat_2=49.8333339 +x_0=150000.013 +y_0=5400088.438 +ellps=intl +towgs84=-106.8686,52.2978,-103.7239,-0.3366,0.457,-1.8422,-1.2747 +units=m +no_defs +type=crs");

// Convert all geolocations to geographic coordinates (Lambert 1972 projection)
const geographicCoordinates = geolocations.map(d => {
    // Check if coordinates are finite numbers
    if (!isFinite(d.x) || !isFinite(d.y)) {
      return { coordinates: [NaN, NaN], type: d.type }; // Return NaN for invalid coordinates
    }
    const transformedCoordinates = proj4('EPSG:31370', 'EPSG:4326', [d.x, d.y]);
    return { coordinates: transformedCoordinates, type: d.type };
}).filter(d => !isNaN(d.coordinates[0]) && !isNaN(d.coordinates[1]));

// Create a new SVG element
const svg = d3.create("svg")
    .attr("viewBox", [0, 0, width, height]);

// Define the Mercator projection
const projection = d3.geoMercator().fitSize([width, height], topojson.feature(belgium, belgium.objects.Gemeenten));

// Create a path generator
const path = d3.geoPath().projection(projection);

svg.append("path")
    .datum(topojson.feature(belgium, belgium.objects.Gemeenten))
    .attr("d", path)
    .attr("fill", "lightgray")
    .attr("stroke", "white");

// Define a scale for colors
const colorScale = d3.scaleOrdinal()
  .domain(geographicCoordinates.map(d => d.type))
  .range(d3.schemeCategory10);

  // Define the legend item width and height
const legendItemWidth = 20;
const legendItemHeight = 20;
  
  // Create a legend for the colors
const legend = svg.append("g")
    .attr("class", "legend")
    .attr("transform", "translate(20," + (height - (colorScale.domain().length * legendItemHeight)) + ")");

// Add rectangles and labels for each year in the legend
legend.selectAll("rect")
    .data(colorScale.domain())
    .enter().append("rect")
    .attr("x", 0)
    .attr("y", (d, i) => i * legendItemHeight)
    .attr("width", legendItemWidth)
    .attr("height", legendItemHeight)
    .attr("fill", colorScale);

legend.selectAll("text")
    .data(colorScale.domain())
    .enter().append("text")
    .attr("x", legendItemWidth + 5)
    .attr("y", (d, i) => i * legendItemHeight + legendItemHeight / 2)
    .attr("dy", "0.35em")
    .text(d => d)
    .attr("fill", "black")
    .style("font-size", "14px")
    .style("font-family", "Arial");

// Append circle elements for each geographic coordinate
svg.selectAll("circle")
  .data(geographicCoordinates)
  .enter().append("circle")
    .attr("cx", d => projection(d.coordinates)[0])
    .attr("cy", d => projection(d.coordinates)[1])
    .attr("r", 1)
    .attr("fill", d => colorScale(d.type));

````
${svg.node()}



