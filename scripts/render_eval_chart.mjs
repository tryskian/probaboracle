import fs from "node:fs";
import { JSDOM } from "jsdom";
import * as d3 from "d3";

const [, , inputPath, outputPath] = process.argv;

if (!inputPath || !outputPath) {
  console.error("Usage: node scripts/render_eval_chart.mjs <input.json> <output.svg>");
  process.exit(1);
}

const payload = JSON.parse(fs.readFileSync(inputPath, "utf8"));
const dom = new JSDOM("<!DOCTYPE html><body></body>");

const width = 960;
const height = 640;
const margin = { top: 146, right: 52, bottom: 84, left: 72 };
const innerWidth = width - margin.left - margin.right;
const innerHeight = height - margin.top - margin.bottom;

const colors = {
  fail: "#F24A3D",
  pass: "#FDB24A",
  pending: "#3B347E",
  text: "#1F1F1F",
  inverseText: "#FFFFFF",
  muted: "#5C6670",
  axis: "#AEB6BF",
  grid: "#E7EBEF",
  surface: "#FFFFFF",
};

function segmentLabelColor(key) {
  if (key === "pending" || key === "fail") return colors.inverseText;
  return colors.text;
}

const body = d3.select(dom.window.document).select("body");
const svg = body
  .append("svg")
  .attr("xmlns", "http://www.w3.org/2000/svg")
  .attr("width", width)
  .attr("height", height)
  .attr("viewBox", `0 0 ${width} ${height}`)
  .attr("role", "img")
  .attr("aria-label", "Probaboracle pass fail pending stacked bar chart");

svg.append("rect").attr("width", width).attr("height", height).attr("fill", colors.surface);

svg
  .append("text")
  .attr("x", 40)
  .attr("y", 40)
  .attr("fill", colors.text)
  .attr("font-family", "Helvetica, Arial, sans-serif")
  .attr("font-size", 28)
  .attr("font-weight", 700)
  .text(payload.title);

svg
  .append("text")
  .attr("x", 40)
  .attr("y", 68)
  .attr("fill", colors.muted)
  .attr("font-family", "Helvetica, Arial, sans-serif")
  .attr("font-size", 15)
  .text(payload.subtitle);

const summary = payload.summary;
const summaryText = `total ${summary.total} • fail ${summary.fail} • pass ${summary.pass} • pending ${summary.pending}`;
svg
  .append("text")
  .attr("x", 40)
  .attr("y", 96)
  .attr("fill", colors.text)
  .attr("font-family", "Helvetica, Arial, sans-serif")
  .attr("font-size", 15)
  .attr("font-weight", 600)
  .text(summaryText);

const legend = svg.append("g").attr("transform", `translate(${width - 250}, 32)`);
const legendItems = [
  { key: "pending", label: "PENDING" },
  { key: "fail", label: "FAIL" },
  { key: "pass", label: "PASS" },
];

legendItems.forEach((item, index) => {
  const row = legend.append("g").attr("transform", `translate(0, ${index * 24})`);
  row
    .append("rect")
    .attr("width", 16)
    .attr("height", 16)
    .attr("rx", 3)
    .attr("fill", colors[item.key]);
  row
    .append("text")
    .attr("x", 24)
    .attr("y", 12)
    .attr("fill", colors.text)
    .attr("font-family", "Helvetica, Arial, sans-serif")
    .attr("font-size", 13)
    .attr("font-weight", 600)
    .text(item.label);
});

const chartRoot = svg.append("g").attr("transform", `translate(${margin.left}, ${margin.top})`);

const x = d3
  .scaleBand()
  .domain(payload.lanes.map((lane) => lane.prompt_type))
  .range([0, innerWidth])
  .padding(0.28);

const y = d3
  .scaleLinear()
  .domain([0, Math.max(1, summary.max_lane_total)])
  .nice()
  .range([innerHeight, 0]);

const stackedRows = payload.lanes.map((lane) => ({
  prompt_type: lane.prompt_type,
  fail: lane.counts.fail,
  pass: lane.counts.pass,
  pending: lane.counts.pending,
  total: lane.total,
}));

const stack = d3.stack().keys(payload.series_order);
const series = stack(stackedRows);

chartRoot
  .append("g")
  .selectAll("line")
  .data(y.ticks(5))
  .join("line")
  .attr("x1", 0)
  .attr("x2", innerWidth)
  .attr("y1", (d) => y(d))
  .attr("y2", (d) => y(d))
  .attr("stroke", colors.grid)
  .attr("stroke-width", 1);

chartRoot
  .append("g")
  .attr("transform", `translate(0, ${innerHeight})`)
  .call(d3.axisBottom(x))
  .call((axis) => axis.select(".domain").attr("stroke", colors.axis))
  .call((axis) =>
    axis
      .selectAll("text")
      .attr("fill", colors.text)
      .attr("font-family", "Helvetica, Arial, sans-serif")
      .attr("font-size", 13)
      .attr("font-weight", 600)
  )
  .call((axis) => axis.selectAll(".tick line").attr("stroke", colors.axis));

chartRoot
  .append("g")
  .call(d3.axisLeft(y).ticks(5).tickFormat(d3.format("d")))
  .call((axis) => axis.select(".domain").attr("stroke", colors.axis))
  .call((axis) =>
    axis
      .selectAll("text")
      .attr("fill", colors.muted)
      .attr("font-family", "Helvetica, Arial, sans-serif")
      .attr("font-size", 12)
  )
  .call((axis) => axis.selectAll(".tick line").attr("stroke", colors.axis));

const layer = chartRoot
  .append("g")
  .selectAll("g")
  .data(series)
  .join("g")
  .attr("fill", (d) => colors[d.key]);

layer
  .selectAll("rect")
  .data((d) => d)
  .join("rect")
  .attr("x", (d) => x(d.data.prompt_type))
  .attr("y", (d) => y(d[1]))
  .attr("width", x.bandwidth())
  .attr("height", (d) => Math.max(0, y(d[0]) - y(d[1])));

series.forEach((seriesEntry) => {
  chartRoot
    .append("g")
    .selectAll("text")
    .data(seriesEntry)
    .join("text")
    .filter((d) => d.data[seriesEntry.key] > 0 && y(d[0]) - y(d[1]) > 22)
    .attr("x", (d) => x(d.data.prompt_type) + x.bandwidth() / 2)
    .attr("y", (d) => y(d[1]) + (y(d[0]) - y(d[1])) / 2 + 4)
    .attr("text-anchor", "middle")
    .attr("fill", segmentLabelColor(seriesEntry.key))
    .attr("font-family", "Helvetica, Arial, sans-serif")
    .attr("font-size", 12)
    .attr("font-weight", 700)
    .text((d) => d.data[seriesEntry.key]);
});

chartRoot
  .append("g")
  .selectAll("text")
  .data(stackedRows)
  .join("text")
  .attr("x", (d) => x(d.prompt_type) + x.bandwidth() / 2)
  .attr("y", (d) => y(d.total) - 10)
  .attr("text-anchor", "middle")
  .attr("fill", colors.text)
  .attr("font-family", "Helvetica, Arial, sans-serif")
  .attr("font-size", 13)
  .attr("font-weight", 700)
  .text((d) => d.total);

svg
  .append("text")
  .attr("x", margin.left)
  .attr("y", height - 26)
  .attr("fill", colors.muted)
  .attr("font-family", "Helvetica, Arial, sans-serif")
  .attr("font-size", 12)
  .text(`Generated ${payload.generated_at}`);

fs.writeFileSync(outputPath, body.html());
