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
    const svg = d3.create("svg")
        .attr("viewBox", [0, 0, padding * (distinct.length + 1) + distinct.map(d => d.length * 7).reduce((a,b) => a + b, 0), 30])
        .style("font", "10px sans-serif")
        .style("user-select", "none");
  
    const legend = svg.append("g")
        .selectAll("g")
        .data(distinct)
        .join("g")
        .attr("transform", (d, i) => `translate(${distinct.slice(0, i).map(d => d.length * 7).reduce((a,b) => a + b, 0) + padding * i}, 0)`);
  
    legend.append("rect")
        .attr("x", 0)
        .attr("y", 5)
        .attr("width", 10)
        .attr("height", 10)
        .attr("fill", d => colors[d]);
  
    legend.append("text")
        .attr("x", 15)
        .attr("y", 10)
        .attr("dy", "0.35em")
        .text(d => d);
  
    return svg.node();
  }