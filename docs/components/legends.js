import * as d3 from "npm:d3";

export function legendeAccidentClasses(distinctAccidentClasses, classColors) {
    const padding = 10; // Padding between legend items
    const svg = d3.create("svg")
        .attr("viewBox", [0, 0, padding * (distinctAccidentClasses.length + 1) + distinctAccidentClasses.map(d => d.length * 7).reduce((a,b) => a + b, 0), 30])
        .style("font", "10px sans-serif")
        .style("user-select", "none");
  
    const legend = svg.append("g")
        .selectAll("g")
        .data(distinctAccidentClasses)
        .join("g")
        .attr("transform", (d, i) => `translate(${distinctAccidentClasses.slice(0, i).map(d => d.length * 7).reduce((a,b) => a + b, 0) + padding * i}, 0)`);
  
    legend.append("rect")
        .attr("x", 0)
        .attr("y", 5)
        .attr("width", 10)
        .attr("height", 10)
        .attr("fill", d => classColors[d]);
  
    legend.append("text")
        .attr("x", 15)
        .attr("y", 10)
        .attr("dy", "0.35em")
        .text(d => d);
  
    return svg.node();
  }