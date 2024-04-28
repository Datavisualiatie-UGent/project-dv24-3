---
theme: light
toc: true
---
````js
import {legendeAccidentClasses} from "./components/legends.js"
````

# Verkeersongelukken
---

````js
const rawdata = await FileAttachment("data/OPENDATA_MAP_2017-2022.csv").csv()
const data = rawdata.map((d, i) => {
    d.DT_YEAR_COLLISION = d.DT_YEAR_COLLISION;
    d.DT_MONTH_COLLISION = parseInt(d.DT_MONTH_COLLISION);
    return d;
})
````

## Heatmap: Gekende ongevallen met gewonden per maand per jaar

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
            data,
            Plot.group(
                {fill: "count"}, {
                    x: (d) => d.DT_YEAR_COLLISION, 
                    y: (d) => d.DT_MONTH_COLLISION - 1, 
                    tip: true
                    }
            )
        )
    ]
})
````

## Waffle chart: Aantal ongevallen met gewonden per provincie 

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
units = units.flatMap(d => d3.range(Math.round(d.freq / 1000)).map(() => d))
units = units.sort( (d1, d2) => d2.freq - d1.freq)
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
            data,
            Plot.group(
                {fill: "count"},
                {x: "TX_ROAD_USR_TYPE1_NL", y: "TX_ROAD_USR_TYPE2_NL", tip: true}
            )
        )
    ]
})
````


## Stacked barchart: Type slachtoffer in ongevallen met gewonden

````js
const groupedAccidentClasses = Array.from(
  d3.rollup(
    rawdata,
    v => Array.from(
      d3.rollup(v, arr => arr.length, d => d.TX_CLASS_ACCIDENTS_NL),
      ([className, count]) => ({ class: className.toLowerCase(), count })
    ),
    d => d.DT_YEAR_COLLISION
  ),
  ([year, classCounts]) => classCounts.map(data => ({ year: parseInt(year), ...data }))
).flat();

const distinctAccidentClasses = [...new Set(groupedAccidentClasses.map(d => d.class.toLowerCase()))];
const colorScheme = d3.schemeCategory10;
const classColors = Object.fromEntries(distinctAccidentClasses.map((className, index) => [className, colorScheme[index % colorScheme.length]]));

const coloredData = groupedAccidentClasses.map(d => ({ ...d, color: classColors[d.class] }));

function line_plot(value) {

    let displayedClass;

    function update(value) {
        displayedClass = coloredData.filter(d => (d.class == value));
        console.log(displayedClass);
    }

    update(value);

    const p = Plot.plot({
    x: {label: "Jaar", tickFormat: d3.format("d"), ticks: 6},
    y: {
        label: "Aantal ongevallen",
        grid: true
    },
    marks: [
        Plot.ruleY([0]),
        Plot.lineY(displayedClass, {x: "year", y: "count", z: "class", stroke: "color"}),
        Plot.dot(displayedClass, { x: "year", y: "count", z: "class", fill: "color", size: 3, tip: true })
    ]
    });

    return p;
}

let accidentClass = line_plot(distinctAccidentClasses[0]);

````
${Inputs.bind(Inputs.select(distinctAccidentClasses, {value: distinctAccidentClasses, format: (x) => x}), accidentClass)}
${view(legendeAccidentClasses(distinctAccidentClasses, classColors))}
${view(accidentClass)}

## Stacked barchart: Binnen en buiten bebouwde kom

````js
Plot.plot({
    x: {label: "Jaar", tickFormat: d3.format("d"), ticks: 6},
    y: {grid: true},
    color: {legend: true},
    marks: [
        Plot.rectY(data, Plot.binX({y: "count"}, {
            x: "DT_YEAR_COLLISION",
            fill: "TX_BUILD_UP_AREA_NL",
            insetLeft: -10,
        })),
        Plot.ruleY([0])
    ],
    xAxis: {tickFormat: d3.format("d")}
})
````

## Stacked barchart: Ongevallen op kruispunt en niet op kruispunt

````js
Plot.plot({
    x: {label: "Jaar", tickFormat: d3.format("d"), ticks: 6},
    y: {grid: true},
    color: {legend: true},
    marks: [
        Plot.rectY(data, Plot.binX({y: "count"}, {
            x: "DT_YEAR_COLLISION",
            fill: "TX_CROSSWAY_NL",
            insetLeft: -10,
        })),
        Plot.ruleY([0])
    ],
    xAxis: {tickFormat: d3.format("d")}
})
````
## Stacked barchart: Weersomstandigheden bij ongevallen

````js
Plot.plot({
    x: {label: "Jaar", tickFormat: d3.format("d"), ticks: 6},
    y: {grid: true},
    color: {legend: true},
    marks: [
        Plot.rectY(data, Plot.binX({y: "count"}, {
            x: "DT_YEAR_COLLISION",
            fill: "TX_WEATHER_NL",
            insetLeft: -10,
        })),
        Plot.ruleY([0])
    ],
    xAxis: {tickFormat: d3.format("d")}
})
````

## Stacked barchart: Wegconditie bij ongevallen

````js
Plot.plot({
    x: {label: "Jaar", tickFormat: d3.format("d"), ticks: 6},
    y: {grid: true},
    color: {legend: true},
    marks: [
        Plot.rectY(data, Plot.binX({y: "count"}, {
            x: "DT_YEAR_COLLISION",
            fill: "TX_ROAD_CONDITION_NL",
            insetLeft: -10,
        })),
        Plot.ruleY([0])
    ],
    xAxis: {tickFormat: d3.format("d")}
})
````

## Stacked barchart: Lichtgesteldheid bij ongevallen

````js
Plot.plot({
    x: {label: "Jaar", tickFormat: d3.format("d"), ticks: 6},
    y: {grid: true},
    color: {legend: true},
    marks: [
        Plot.rectY(data, Plot.binX({y: "count"}, {
            x: "DT_YEAR_COLLISION",
            fill: "TX_LIGHT_CONDITION_NL",
            insetLeft: -10,
        })),
        Plot.ruleY([0])
    ],
    xAxis: {tickFormat: d3.format("d")}
})
````
## Stacked barchart: Type weg bij ongevallen

````js
Plot.plot({
    x: {label: "Jaar", tickFormat: d3.format("d"), ticks: 6},
    y: {grid: true},
    color: {legend: true},
    marks: [
        Plot.rectY(data, Plot.binX({y: "count"}, {
            x: "DT_YEAR_COLLISION",
            fill: "CD_ROAD_TYPE_NL",
            insetLeft: -10,
        })),
        Plot.ruleY([0])
    ],
    xAxis: {tickFormat: d3.format("d")}
})
````

## Kaart: Type slachtoffer met locatie

````js

import proj4 from "npm:proj4";

const belgium = await FileAttachment("data/Gemeenten_Fusies.json").json()

const geolocations = rawdata.map(d => ({
    x: parseFloat(d.MS_X_COORD),
    y: parseFloat(d.MS_Y_COORD),
    type: d.TX_CLASS_ACCIDENTS_NL.toLowerCase()
})).filter(d => isFinite(d.x) && isFinite(d.y));

proj4.defs("EPSG:31370", "+proj=lcc +lat_0=90 +lon_0=4.36748666666667 +lat_1=51.1666672333333 +lat_2=49.8333339 +x_0=150000.013 +y_0=5400088.438 +ellps=intl +towgs84=-106.8686,52.2978,-103.7239,-0.3366,0.457,-1.8422,-1.2747 +units=m +no_defs +type=crs");

// Convert all geolocations to geographic coordinates (Lambert 1972 projection)
const geographic_coordinates = geolocations.map(d => {
    const transformedCoordinates = proj4('EPSG:31370', 'EPSG:4326', [d.x, d.y]);
    return { coordinates: transformedCoordinates, type: d.type };
    });

const distinct_types = [...new Set(geolocations.map(d => d.type))];

const coordinates_by_type = new Object();

distinct_types.forEach(type => {
    const coordinates = geographic_coordinates.filter(d => d.type === type).map(d => ({ coordinates: d.coordinates, type:d.type }));
    coordinates_by_type[type] = coordinates;
});


function chart(value) {
    const width = 800;
    const height = 600;

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
        .domain(geographic_coordinates.map(d => d.type))
        .range(d3.schemeCategory10);

    // Define the legend item width and height
    const legendItemWidth = 30;
    const legendItemHeight = 30;
      
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
        .style("font-size", "16px")
        .style("font-family", "Arial");

    // Update function
    function update(value) {
        const displayed = value.reduce((result, key) => {
            if (coordinates_by_type[key]) {
                result = result.concat(coordinates_by_type[key]);
            }
            return result;
        }, []);

        svg.selectAll("circle") // Select all circles
        .data(displayed, d => d.type) // Bind data filtered by checkbox values
        .join(
            enter => enter.append("circle") // Append new circles for entered data
            .attr("cx", d => projection(d.coordinates)[0])
            .attr("cy", d => projection(d.coordinates)[1])
            .attr("r", 1)
            .attr("fill", d => colorScale(d.type))
            .attr("class", d => "type-" + d.type),
            exit => exit.remove() // Remove circles for exited data
        );
  }

  // Initialize with all types displayed
  update(value);

  // Bind update function to value change
  Object.defineProperty(svg.node(), "value", {
    get() {
      return value;
    },
    set(v) {
      value = v;
      update(value); // Call update function
    }
  });
  
  
    // Display the SVG
    return svg.node();
}

let type_victim = chart(distinct_types);

````
${Inputs.bind(Inputs.checkbox(distinct_types, {value: distinct_types, format: (x) => x}), type_victim)}
${view(type_victim)}

## TODO: Correlatiematrix?

