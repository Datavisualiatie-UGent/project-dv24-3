---
theme: dark
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



