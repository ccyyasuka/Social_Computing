<template>
  <div>
    <div id="RumorTree">
      <svg id="RumorTreeSvg"></svg>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3"
import axios from "axios"
import bus from "./bus.js"
export default {
  data () {
    return {

    }
  },
  created () {
    let param = { "date": 0, "event": 0 }
    // bus.$on("SelectTime",(val) => {
    //   this.date=val["date"]
    //   this.event=val["event"]
    //   let param ={"date": this.date, "event": this.event} 
    //   axios
    //     .post("http://10.192.9.11:9931/api/RumorTree", param)
    //     .then((response) => {
    //       console.log(response)
    //       let temp = JSON.stringify(response.data)
    //       console.log(temp)
    //       let res = JSON.parse(temp)
    //       console.log(res)
    //       this.ini_links = res
    //       console.log(this.ini_links)
    //       this.draw()
    //     })

    // });
    axios
      .post("http://10.192.9.11:9931/api/RumorTree", param)
      .then((response) => {
        console.log(response)
        let temp = JSON.stringify(response.data)
        console.log(temp)
        let res = JSON.parse(temp)
        console.log(res)
        this.ini_links = res
        console.log(this.ini_links)
        this.draw()

      })
  },
  methods: {
    draw () {
      function linkArc (d) {
        const r = Math.hypot(d.target.x - d.source.x, d.target.y - d.source.y)
        return `
          M${d.source.x},${d.source.y}
          A${r},${r} 0 0,1 ${d.target.x},${d.target.y}
        `
      }
      let drag = simulation => {

        function dragstarted (event, d) {
          if (!event.active) simulation.alphaTarget(0.3).restart()
          d.fx = d.x
          d.fy = d.y
        }

        function dragged (event, d) {
          d.fx = event.x
          d.fy = event.y
        }

        function dragended (event, d) {
          if (!event.active) simulation.alphaTarget(0)
          d.fx = null
          d.fy = null
        }

        return d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended)
      }


      let links = this.ini_links
      // console.log(links)
      let types = Array.from(new Set(links.map(d => d.type)))

      let data = ({ nodes: Array.from(new Set(links.flatMap(l => [l.source, l.target])), id => ({ id })), links })

      let height = 600
      let width = 940
      let color = d3.scaleOrdinal(types, d3.schemeCategory10)

      links = data.links.map(d => Object.create(d))
      const nodes = data.nodes.map(d => Object.create(d))

      const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id))
        .force("charge", d3.forceManyBody().strength(-200))
        .force("x", d3.forceX())
        .force("y", d3.forceY())
      d3.select("#RumorTreeSvg").selectAll("*").remove()
      // const svg = d3.selectAll("#CommentNetwork").append("svg")
      //     .attr("viewBox", [-width / 2, -height / 2, width*2, height*2])
      //     .style("font", "12px sans-serif");
      const svg = d3.select("#RumorTreeSvg").attr("viewBox", [-width / 2, -height / 2, width, height])
      let g = svg.append("g")

      const zoom = d3.zoom()
        .scaleExtent([1, 8])
        .on("zoom", zoomed)
      function zoomed (event) {
        const { transform } = event
        g.attr("transform", transform)
        g.attr("stroke-width", 1 / transform.k)
      }
      svg.call(zoom)
      // .attr("viewBox", [0, 0, width*2, 2*height])
      // .attr("id","BarSvg")
      // .attr("width", width)
      // .attr("height", height)

      // Per-type markers, as they don't inherit styles.
      g.append("defs").selectAll("marker")
        .data(types)
        .join("marker")
        .attr("id", d => `arrow-${d}`)
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 15)
        .attr("refY", -0.5)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("path")
        .attr("fill", color)
        .attr("d", "M0,-5L10,0L0,5")

      const link = g.append("g")
        .attr("fill", "none")
        .attr("stroke-width", 1.5)
        .selectAll("path")
        .data(links)
        .join("path")
        .attr("stroke", d => color(d.type))
        .attr("marker-end", d => `url(${new URL(`#arrow-${d.type}`, location)})`)

      const node = g.append("g")
        .attr("fill", "currentColor")
        .attr("stroke-linecap", "round")
        .attr("stroke-linejoin", "round")
        .selectAll("g")
        .data(nodes)
        .join("g")
        .call(drag(simulation))

      node.append("circle")
        .attr("stroke", "white")
        .attr("stroke-width", 1.5)
        .attr("r", 4)

      node.append("text")
        .attr("x", 8)
        .attr("y", "0.31em")
        .text(d => d.id)
        .clone(true).lower()
        .attr("fill", "none")
        .attr("stroke", "white")
        .attr("stroke-width", 3)

      simulation.on("tick", () => {
        link.attr("d", linkArc)
        node.attr("transform", d => `translate(${d.x},${d.y})`)
      })
    }
  },
}
</script>

<style lang="scss" scoped>
</style>