import * as d3 from "npm:d3";

export function color_mapping (distinct, colors) {
    return Object.fromEntries(distinct.map((x, index) => [x, colors[index % colors.length]]));
}

export function add_color_to_data(data, colors_mapped, key) {
    return data.map(d => ({ ...d, color: colors_mapped[d[key]] }));
}

export function legend(colors) {
    const distinct = Object.keys(colors);
    const padding = 10; // Padding between legend items
    const lineHeight = 20; // Height of each line in the legend
    const fontSize = 12; // Fixed font size
    const svgWidth = 200;
    const svgHeight = 600;

    const svg = d3.create("svg")
        .attr("viewBox", [0, 0, svgWidth, svgHeight])
        .style("font", `${fontSize}px sans-serif`)
        .style("user-select", "none");
  
    const legend = svg.append("g")
        .selectAll("g")
        .data(distinct)
        .join("g")
        .attr("transform", (d, i) => `translate(0, ${lineHeight * i})`);
  
    legend.append("rect")
        .attr("x", padding)
        .attr("y", 5)
        .attr("width", 10)
        .attr("height", 10)
        .attr("fill", d => colors[d]);
  
    legend.append("text")
        .attr("x", padding + 15)
        .attr("y", 10)
        .attr("dy", "0.35em")
        .text(d => d);
  
    return svg.node();
}

