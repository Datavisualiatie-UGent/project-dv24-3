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
    d.DT_YEAR_COLLISION = parseInt(d.DT_YEAR_COLLISION);
    d.DT_MONTH_COLLISION = parseInt(d.DT_MONTH_COLLISION);
    return d;
})
````

````js
Plot.plot({
    color: { legend: true, scheme: "Oranges" },
    y: { grid: true, reverse: true },
    title: "Ongevallen per maand per jaar",
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

## Title 2



