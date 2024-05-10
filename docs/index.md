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


```js
const ongevallen_per_jaar = await FileAttachment("data/ongevallen_gewonden_jaar.json").json();
```

Jammer genoeg zijn er elk jaar nog veel ongevallen. Het statistiekbureau van België StatBel biedt een [dataset](https://statbel.fgov.be/nl/open-data/geolocalisatie-van-de-verkeersongevallen-2017-2022)
aan waarin verkeersongevallen opgelijst staan van 2017 tot 2022. De dataset is gebaseerd op ongevallen geregistreerd door federale politie, dus het is mogelijk dat sommige ongevallen niet in deze dataset vervat zitten.
Het doel van deze visualisatie is meer inzicht creëren in de data, en aantonen waar eventueel veiligere situaties moeten voorzien worden.


Een eerste duidelijke trend is al zichtbaar op de eerste grafiek: beduidend minder ongevallen in 2020. Hier is een eenvoudige verklaring voor: Corona.
Iedereen werd verzocht om zoveel mogelijk thuis te blijven en van thuis te werken. Het gevolg was dat er veel minder mensen op de baan waren, en er dus veel minder ongevallen zijn.


```js
Plot.plot({
    y: {grid: true, domain: [0, 43000], label: "accidents"},
    title: "Gekende ongevallen per jaar",
    marginTop: 0,
    insetRight: 0,
    x: {tickFormat: ""},
    marks: [
        Plot.barY(
            ongevallen_per_jaar,
            {x: "year", y:"value", tip:true}
        ),
        Plot.ruleY([0])
    ]
})
```



```js
const rawdata = await FileAttachment("data/OPENDATA_MAP_2017-2022.csv").csv()
```




## Heatmap: Gekende ongevallen met gewonden per maand per jaar

```js
const ongevallen_per_maand_jaar = await FileAttachment("data/ongevallen_gewonden_maand_jaar.json").json();
```

Onderstaande visualisatie toont het aantal ongevallen per maand doorheen de jaren.
Hierbij hebben we gekozen voor een heatmap om de relatieve frequenties van
ongevallen in verschillende periodes in één oogopslag te kunnen vergelijken.

Interessant hier is dat 2020 beduidend minder ongevallen heeft dan andere
jaren, met april 2020 veruit het minste aantal ongevallen. Dit is natuurlijk het begin van de Covid-19 pandemie, 
wanneer iedereen de regels strikt volgde en enkel buiten ging wanneer dit echt noodzakelijk was.

````js
Plot.plot({
    title: "Gekende ongevallen per jaar per maand",
    width: 350,
    height: 600,
    color: {legend: true, scheme: "Oranges"},
    marginTop: 0,
    aspectRatio: 1,
    xscale: "band",
    x: {type: "band", label: "Jaar", tickFormat: ""},
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

## Bar chart: Aantal ongevallen per provincie 

Hier visualiseren we hoe het totaal aantal ongevallen verdeeld is onder de
verschillende provincies relatief ten opzichte van het aantal inwoners.
Oost-Vlaanderen is de provincie met gemiddeld het meeste ongevallen per inwoner.

Over het algemeen lijkt het ook dat de Waalse provincies het beter doen dan de Vlaamse. Dit kan natuurlijk komen 
doordat in Vlaanderen meer grote steden zijn, en dat hierrond meer accidenten gebeuren.

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

De dataset bevat voor elk ongeval ook informatie over de twee betrokken
partijen. Met onderstaande heatmap visualiseren we welke combinaties van
partijen er het vaakst voorkomen in de dataset. Op de X as staat de primaire bestuurder.
Dit is de bestuurder die een ongeval heeft gehad. Op de Y as staan andere betrokken bestuurders of obstakels.
Het kleur geeft aan hoeveel zo een type ongeval is geregistreerd. Opgelet: het is een logaritmische kleurschaal.

Hier zien we dat de personenwagen veruit de grootste partij is, gecombineerd
met een andere personenwagen, een fietser, of een hindernis. Dit laatste
betekent dat de personenwagen niet tegen een ander voertuig is gereden, maar
tegen een object of gebouw.

Daarnaast is het ook zichtbaar dat fietser een grote groep van primaire bestuurders zijn.
Deze hebben dan hoofdzakelijk ongevallen met personenwagens en andere fietsers


```js
const ongevallen_per_weggebruiker = await FileAttachment("data/ongevallen_per_betrokken_weggebruiker.json").json();
```

````js
Plot.plot({
    title: "betrokken weggebruikers",
    color: {legend: true, scheme: "Oranges", type: "log"},
    aspectRatio: 1.4,
    marginTop: 0,
    marginLeft: 200,
    marginBottom: 120,
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
````


## Explore it yourself

De volgende visualisatie is interactief: je kan een onderwerp kiezen, zoals gewonden of kruispunten, en dan bekijken welke data hierover bestaat.
Zo is voor ongevallen bijvoorbeeld te zien dat het merendeel gebeurt niet in de buurt van een kruispunt

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

Hier tonen we op een kaart alle locaties waar er ongevallen zijn gebeurd met
gewonden. Aangezien personenwagens de meeste ongevallen veroorzaken is het niet
onverwacht dat de datapunten een vrij gedetailleerde kaart vormen van het
Belgisch wegennet.

````js
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

