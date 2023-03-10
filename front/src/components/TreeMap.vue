<template>
  <div>
    <!-- <button type="button" @click="timedraw">test</button> -->
    <a-space direction="vertical">
      <a-range-picker
        :show-time="{ format: 'HH:mm' }"
        format="YYYY-MM-DD HH:mm"
        :placeholder="['Start Time', 'End Time']"
        @ok="onOk"
      />
      <div id="topk_thre">
        <h5 style="font-size: 120%">top-k words</h5>
        <a-slider
          id="tree_thre"
          :max="80"
          :min="50"
          :step="1"
          :default-value="55"
          style="width: 300px; margin-left: 22px"
          @afterChange="treemap_thre"
        />
      </div>
    </a-space>
    <div id="TreeMap"></div>
  </div>
</template>

<script>
import * as d3 from "d3"
import axios from "axios"
import bus from "./bus"

export default {
  name: "TreeMap",
  mounted () {

    // this.init()
  },
  data () {
    return {
      path: "http://127.0.0.1/15655/words_count",
      svg: null,
      count: 0,
      // test_data2: [{ 'name': 'sydneysiege/', 'value': 12341 }, { 'name': 'sydneysiege/@user', 'value': 12141 }, { 'name': 'ottawashooting/', 'value': 10360 }, { 'name': 'charliehebdo/', 'value': 9817 }, { 'name': 'ottawashooting/@user', 'value': 9234 }, { 'name': 'charliehebdo/@user', 'value': 8929 }, { 'name': 'germanwings/', 'value': 3907 }, { 'name': 'germanwings/@user', 'value': 3682 }, { 'name': 'sydneysiege/the', 'value': 3185 }, { 'name': 'ottawashooting/the', 'value': 2106 }, { 'name': 'charliehebdo/the', 'value': 2079 }, { 'name': 'sydneysiege/httpurl', 'value': 1892 }, { 'name': 'sydneysiege/to', 'value': 1842 }, { 'name': 'charliehebdo/httpurl', 'value': 1747 }, { 'name': 'sydneysiege/in', 'value': 1636 }, { 'name': 'charliehebdo/in', 'value': 1632 }, { 'name': 'sydneysiege/is', 'value': 1535 }, { 'name': 'sydneysiege/a', 'value': 1523 }, { 'name': 'ottawashooting/in', 'value': 1495 }, { 'name': 'sydneysiege/not', 'value': 1387 }, { 'name': 'sydneysiege/!', 'value': 1384 }, { 'name': 'charliehebdo/to', 'value': 1352 }, { 'name': 'ottawashooting/to', 'value': 1336 }, { 'name': 'ottawashooting/httpurl', 'value': 1283 }, { 'name': 'sydneysiege/of', 'value': 1257 }, { 'name': 'charliehebdo/of', 'value': 1229 }, { 'name': 'ottawashooting/a', 'value': 1170 }, { 'name': 'sydneysiege/sydney', 'value': 1148 }, { 'name': 'ottawashooting/!', 'value': 1144 }, { 'name': 'ottawashooting/is', 'value': 1118 }, { 'name': 'charliehebdo/a', 'value': 1041 }, { 'name': 'charliehebdo/!', 'value': 1035 }, { 'name': 'ottawashooting/of', 'value': 1023 }, { 'name': 'sydneysiege/you', 'value': 1006 }, { 'name': 'sydneysiege/and', 'value': 1003 }],
      // test_data1: [{ 'name': 'sydneysiege/', 'value': 12341 }, { 'name': 'sydneysiege/@user', 'value': 12141 }, { 'name': 'charliehebdo/', 'value': 9817 }, { 'name': 'charliehebdo/@user', 'value': 8929 }, { 'name': 'sydneysiege/the', 'value': 3185 }, { 'name': 'charliehebdo/the', 'value': 2079 }, { 'name': 'sydneysiege/httpurl', 'value': 1892 }, { 'name': 'sydneysiege/to', 'value': 1842 }, { 'name': 'charliehebdo/httpurl', 'value': 1747 }, { 'name': 'sydneysiege/in', 'value': 1636 }, { 'name': 'charliehebdo/in', 'value': 1632 }, { 'name': 'sydneysiege/is', 'value': 1535 }, { 'name': 'sydneysiege/a', 'value': 1523 }, { 'name': 'sydneysiege/not', 'value': 1387 }, { 'name': 'sydneysiege/!', 'value': 1384 }, { 'name': 'charliehebdo/to', 'value': 1352 }, { 'name': 'sydneysiege/of', 'value': 1257 }, { 'name': 'charliehebdo/of', 'value': 1229 }, { 'name': 'sydneysiege/sydney', 'value': 1148 }, { 'name': 'charliehebdo/a', 'value': 1041 }, { 'name': 'charliehebdo/!', 'value': 1035 }, { 'name': 'sydneysiege/you', 'value': 1006 }, { 'name': 'sydneysiege/and', 'value': 1003 }, { 'name': 'charliehebdo/paris', 'value': 967 }, { 'name': 'sydneysiege/i', 'value': 939 }, { 'name': 'charliehebdo/is', 'value': 923 }, { 'name': 'sydneysiege/sydneysiege', 'value': 874 }, { 'name': 'charliehebdo/not', 'value': 869 }, { 'name': 'sydneysiege/are', 'value': 844 }, { 'name': 'charliehebdo/and', 'value': 819 }, { 'name': 'sydneysiege/it', 'value': 793 }, { 'name': 'sydneysiege/this', 'value': 786 }, { 'name': 'sydneysiege/that', 'value': 776 }, { 'name': 'sydneysiege/hostages', 'value': 747 }, { 'name': 'sydneysiege/cafe', 'value': 676 }],
      thresh: 55,
      tooltip:null,
      cur_data:null,
      start:null,
      end:null
    }
  },
  methods:
  {
    onOk (value) {
      var that = this//记录 这里的that和提示框的关系
      var moment = require('moment')
      var start = moment(value[0]._d).valueOf() / 1000
      var end = moment(value[1]._d).valueOf() / 1000
      this.start = start
      this.end = end
      console.log(start)
      console.log(end)
      bus.$emit("TimeSpan", [start, end])
      var param = { "start": start, "end": end, "thresh": this.thresh }
      axios
        .post("http://10.192.9.11:9931/api/words", param)
        .then((response) => {
          if (this.count === 0) 
          {

            console.log("draw")
            console.log(response.data["res"])
            if (response.data["res"].length < 1)
              that.$message.error('There is no data for this period.')
            else {
              this.count++
              this.cur_data = response.data["res"]
              this.init(this.cur_data)
            }

            // console.log(this.test_data1)
            // this.init(this.test_data1)
          }
          else {
            // console.log("update")
            // this.cur_data = response.data["res"]
            // this.update(this.cur_data)
            if (response.data["res"].length < 1)
              that.$message.error('There is no data for this period.')
            else {
              this.count++
              this.cur_data = response.data["res"]
              this.update(this.cur_data)
            }
            // this.update(this.test_data2)
          }//数据估计有问题
        })
    },
    treemap_thre (value) { 
      this.thresh = value
      let that = this
      var param = { "start": this.start, "end": this.end, "thresh": this.thresh }
      axios
        .post("http://10.192.9.11:9931/api/words", param)
        .then((response) => {
          if (this.count === 0) 
          {

            console.log("draw")
            console.log(response.data["res"])
            if (response.data["res"].length < 1)
              that.$message.error('There is no data for this period.')
            else {
              this.count++
              this.cur_data = response.data["res"]
              this.init(this.cur_data)
            }

            // console.log(this.test_data1)
            // this.init(this.test_data1)
          }
          else {
            // console.log("update")
            // this.cur_data = response.data["res"]
            // this.update(this.cur_data)
            if (response.data["res"].length < 1)
              that.$message.error('There is no data for this period.')
            else {
              this.count++
              this.cur_data = response.data["res"]
              this.update(this.cur_data)
            }
            // this.update(this.test_data2)
          }//数据估计有问题
        })
      
       },


    preprocess (data1) {
      var width = 700
      var height = 320
      var margin = 0 // shorthand for margins
      var marginTop = margin // top margin, in pixels
      var marginRight = margin // right margin, in pixels
      var marginBottom = margin // bottom margin, in pixels
      var marginLeft = margin // left margin, in pixels
      var padding = 1 // shorthand for inner and outer padding
      var paddingInner = padding // to separate a node from its adjacent siblings
      var paddingOuter = padding // shorthand for top, right, bottom, and left padding
      var paddingTop = paddingOuter // to separate a node’s top edge from its children
      var paddingRight = paddingOuter // to separate a node’s right edge from its children
      var paddingBottom = paddingOuter // to separate a node’s bottom edge from its children
      var paddingLeft = paddingOuter // to separate a node’s left edge from its children
      var round = true
      var tile = d3.treemapSquarify
      var label = (d, n) => [...d.name.split(".").pop().split(/(?=[A-Z][a-z])/g), n.value.toLocaleString("en")].join("\n")
      var title = (d, n) => `${d.name}\n${n.value.toLocaleString("en")}` // text to show on hover
      console.log(data1)
      data1.sort(this.shuffle)
      const root1 = d3.stratify().path(d => d.name.replace(/\./g, "/"))(data1)
      root1.sum(function (d) {
        if (d != null)
          return Math.max(0, d?.value)
        else
          return 0
      })
      // Prior to sorting, if a group channel is specified, construct an ordinal color scale.
      const leaves = root1.leaves()
      console.log("leaves", leaves)
      // const G = group == null ? null : leaves.map(d => group(d.data["name"]));
      const G = leaves.map(d => d.data["name"].split("/")[0])
      var zDomain = G
      zDomain = new d3.InternSet(zDomain)//去重
      const color = d3.scaleOrdinal(zDomain, d3.schemeTableau10)

      // Compute labels and titles.
      const L = label == null ? null : leaves.map(d => label(d.data, d))
      const T = title === undefined ? L : title == null ? null : leaves.map(d => title(d.data, d))
      console.log("LLLLLLLLLLLLLLLLL",L)
      console.log(T)
      // Sort the leaves (typically by descending value for a pleasing layout).
      // if (sort != null) root.sort(sort);

      // Compute the treemap layout.
      const treemap1 = d3.treemap()
        .tile(tile)
        .size([width - marginLeft - marginRight, height - marginTop - marginBottom])
        .paddingInner(paddingInner)
        .paddingTop(paddingTop)
        .paddingRight(paddingRight)
        .paddingBottom(paddingBottom)
        .paddingLeft(paddingLeft)
        .round(round)
      treemap1(root1)
      var temp = Math.max.apply(null, data1.map(d => d.value))
      console.log(temp)
      var text_opacity = d3.scaleLinear().domain([0, temp]).range([0, 1])
      console.log(text_opacity(20))
      return [leaves, L, T, G, color, text_opacity]

    },




    init (data) {

      this.Treemap(data, {
        path: d => d.name.replace(/\./g, "/"), // e.g., "flare/animate/Easing"
        value: d => d?.value, // size of each node (file); null for internal nodes (folders)
        group: d => d.name.split(".")[1], // e.g., "animate" in "flare.animate.Easing"; for color
        label: (d, n) => [...d.name.split(".").pop().split(/(?=[A-Z][a-z])/g), n.value.toLocaleString("en")].join("\n"),
        title: (d, n) => `${d.name}\n${n.value.toLocaleString("en")}`, // text to show on hover
        link: (d, n) => `https://github.com/prefuse/Flare/blob/master/flare/src${n.id}.as`,
        width: 700,
        height: 320
      })
    },
    sleep (n) {
      var start = new Date().getTime()
      //  console.log('休眠前：' + start);
      while (true) {
        if (new Date().getTime() - start > n) {
          break
        }
      }
      // console.log('休眠后：' + new Date().getTime());
    },
    timedraw () {
      var d1 = new Date(2001)
      var d2 = new Date(2001)
      var d3 = new Date(2001)
      const data1 = {
        "d1": [{ "name": "a/aa", "value": 54 }
          , { "name": "a/b", "value": 51 }
          , { "name": "a/c", "value": 79 }
          , { "name": "a/d", "value": 97 }
          , { "name": "a/e", "value": 6 }
          , { "name": "a/ff", "value": 48 }
          , { "name": "b/a", "value": 0 }
          , { "name": "b/b", "value": 49 }
          , { "name": "b/c", "value": 0 }
          , { "name": "b/d", "value": 27 }
          , { "name": "c/aa", "value": 21 }
          , { "name": "c/b", "value": 18 }
          , { "name": "c/c", "value": 62 }
          , { "name": "c/d", "value": 24 }
          , { "name": "c/e", "value": 29 }
        ],
        "d2": [{ "name": "a/aa", "value": 54 }
          , { "name": "a/b", "value": 51 }
          , { "name": "a/c", "value": 19 }
          , { "name": "a/d", "value": 17 }
          , { "name": "a/e", "value": 76 }
          , { "name": "a/ff", "value": 48 }
          , { "name": "b/a", "value": 46 }
          , { "name": "b/b", "value": 49 }
          , { "name": "b/c", "value": 90 }
          , { "name": "b/d", "value": 27 }
          , { "name": "c/aa", "value": 21 }
          , { "name": "c/b", "value": 18 }
          , { "name": "c/c", "value": 62 }
          , { "name": "c/d", "value": 24 }
          , { "name": "c/e", "value": 29 }
        ],
        "d3": [{ "name": "a/aa", "value": 14 }
          , { "name": "a/b", "value": 21 }
          , { "name": "a/c", "value": 39 }
          , { "name": "a/d", "value": 47 }
          , { "name": "a/e", "value": 56 }
          , { "name": "a/ff", "value": 68 }
          , { "name": "b/a", "value": 76 }
          , { "name": "b/b", "value": 0 }
          , { "name": "b/bbb", "value": 54 }
          , { "name": "b/c", "value": 80 }
          , { "name": "b/d", "value": 97 }
          , { "name": "c/aa", "value": 11 }
          , { "name": "c/b", "value": 28 }
          , { "name": "c/c", "value": 32 }
          , { "name": "c/d", "value": 44 }
          , { "name": "c/e", "value": 59 }
          , { "name": "d/f", "value": 59 }
        ]
      }
      // for (var key in data1)
      // {
      //   // this.sleep(2000)
      //   console.log("aaa")
      //   this.update(data1[key])
      // }
      // this.update(data1["d1"])
      // this.update(data1["d2"])
      this.update(data1["d3"])

    },
    shuffle (a, b) {
      return Math.random() > .5 ? -1 : 1
      //用Math.random()函数生成0~1之间的随机数与0.5比较，返回-1或1
    },


    Treemap (data,
      { // data is either tabular (array of objects) or hierarchy (nested objects)
        path, // as an alternative to id and parentId, returns an array identifier, imputing internal nodes
        id = Array.isArray(data) ? d => d.id : null, // if tabular data, given a d in data, returns a unique identifier (string)
        parentId = Array.isArray(data) ? d => d.parentId : null, // if tabular data, given a node d, returns its parent’s identifier
        children, // if hierarchical data, given a d in data, returns its children
        value, // given a node d, returns a quantitative value (for area encoding; null for count)
        sort = (a, b) => d3.descending(a.value, b.value), // how to sort nodes prior to layout
        label, // given a leaf node d, returns the name to display on the rectangle
        group, // given a leaf node d, returns a categorical value (for color encoding)
        title, // given a leaf node d, returns its hover text
        link, // given a leaf node d, its link (if any)
        linkTarget = "_blank", // the target attribute for links (if any)
        // tile = d3.treemapResquarify, // treemap strategy
        width = 640, // outer width, in pixels
        height = 400, // outer height, in pixels
        margin = 0, // shorthand for margins
        marginTop = margin, // top margin, in pixels
        marginRight = margin, // right margin, in pixels
        marginBottom = margin, // bottom margin, in pixels
        marginLeft = margin, // left margin, in pixels
        padding = 1, // shorthand for inner and outer padding
        paddingInner = padding, // to separate a node from its adjacent siblings
        paddingOuter = padding, // shorthand for top, right, bottom, and left padding
        paddingTop = paddingOuter, // to separate a node’s top edge from its children
        paddingRight = paddingOuter, // to separate a node’s right edge from its children
        paddingBottom = paddingOuter, // to separate a node’s bottom edge from its children
        paddingLeft = paddingOuter, // to separate a node’s left edge from its children
        round = true, // whether to round to exact pixels
        colors = d3.schemeTableau10, // array of colors
        zDomain, // array of values for the color scale
        fill = "#ccc", // fill for node rects (if no group color encoding)
        fillOpacity = group == null ? null : 0.6, // fill opacity for node rects
        stroke, // stroke for node rects
        strokeWidth, // stroke width for node rects
        strokeOpacity, // stroke opacity for node rects
        strokeLinejoin, // stroke line join for node rects
      } = {}) {
      // If id and parentId options are specified, or the path option, use d3.stratify
      // to convert tabular data to a hierarchy; otherwise we assume that the data is
      // specified as an object {children} with nested objects (a.k.a. the “flare.json”
      // format), and use d3.hierarchy.

      //path d => d.name.replace(/\./g, "/")
      //只走d3.stratify().path(path)(data)这条路 把data.name中 换成flare/a/b格式
      // const root = (path != null) ? (d3.stratify().path(path)(data))
      //     : (
      //       (id != null || parentId != null) 
      //       ? (d3.stratify().id(id).parentId(parentId)(data))
      //       : d3.hierarchy(data, children)
      //     );
      // console.log(root)
      // // debugger
      // // Compute the values of internal nodes by aggregating from the leaves.
      // // root.sum(d => Math.max(0, value(d)));
      // root.sum(function(d)
      // {
      //   if (d!=null)
      //   return Math.max(0, value(d))
      //   else
      //   return 0
      // })
      // // Prior to sorting, if a group channel is specified, construct an ordinal color scale.
      // const leaves = root.leaves();
      // console.log("leaves",leaves)
      // // const G = group == null ? null : leaves.map(d => group(d.data["name"]));
      // const G = leaves.map(d=>d.data["name"].split("/")[0])
      // if (zDomain === undefined) zDomain = G;
      // zDomain = new d3.InternSet(zDomain);//去重
      // const color = d3.scaleOrdinal(zDomain, colors);

      // // Compute labels and titles.
      // const L = label == null ? null : leaves.map(d => label(d.data, d));
      // const T = title === undefined ? L : title == null ? null : leaves.map(d => title(d.data, d));
      // console.log(L)
      // console.log(T)
      // // Sort the leaves (typically by descending value for a pleasing layout).
      // if (sort != null) root.sort(sort);

      // // Compute the treemap layout.
      // const treemap1 =  d3.treemap()
      //     .tile(tile)
      //     .size([width - marginLeft - marginRight, height - marginTop - marginBottom])
      //     .paddingInner(paddingInner)
      //     .paddingTop(paddingTop)
      //     .paddingRight(paddingRight)
      //     .paddingBottom(paddingBottom)
      //     .paddingLeft(paddingLeft)
      //     .round(round);
      // treemap1(root);
      // console.log(treemap1)
      // console.log(leaves)
      var res = this.preprocess(data)
      var leaves = res[0]
      var L = res[1]
      var T = res[2]
      var G = res[3]
      var color = res[4]
      var text_opacity = res[5]
      var max_data = Math.max.apply(null, data.map(d => d.value))
      var tooltip = d3.select("body")
        .append("div")
        .attr("class", "tooltip")
        .style("position", "absolute")
        .style("width", 150)
        .style("height", "auto")
        .style("font-size", "14px")
        .style("text-align", "center")
        .style("border-style", "solid")
        .style("border-width", "1px")
        .style("border-radius", "5px")
        .style("background-color", "white")


      const svg = d3.selectAll("#TreeMap").append("svg")
        .attr("viewBox", [-marginLeft, -marginTop, width, height])
        .attr("width", width)
        .attr("height", height)
        .attr("style", "max-width: 100%; height: auto; height: intrinsic;")
        .attr("font-family", "sans-serif")
        .attr("font-size", 10)
      console.log("leaves", leaves)
      const node = svg.selectAll("rect")
        .data(leaves)
        .join("rect")
      const text_node = svg.selectAll("text")
        .data(leaves)
        .join("text")
        .text(d => { return d.data["name"].split("/")[1] + "\t" + d.data["value"] })
        .attr("transform", d => `translate(${d.x0},${(d.y0 + d.y1) / 2})`)
        .attr("fill-opacity", d => {
          if (d.data["value"] < max_data / 3)
            return 0
          return 1
        })

      // .attr("xlink:href", link == null ? null : (d) => link(d.data, d))
      // .attr("target", link == null ? null : linkTarget)
      node
        .attr("fill", color ? (d, i) => color(G[i]) : fill)
        .attr("fill-opacity", 0.6)
        .attr("stroke", stroke)
        .attr("transform", d => `translate(${d.x0},${d.y0})`)
        .attr("stroke-width", strokeWidth)
        .attr("stroke-opacity", strokeOpacity)
        .attr("stroke-linejoin", strokeLinejoin)
        .attr("width", d => { return d.x1 - d.x0 })
        .attr("height", d => d.y1 - d.y0)
        .on("click", function (e, d) {//e是鼠标事件 d是每个方块挂载的数据 可以通过此处传递信息出去
          // console.log()
          console.log("splited", d.id.split("/")[1])
          bus.$emit("SelectEvent", d.id.split("/")[1])
        })
        .on("mouseover", function (e, d) {
          console.log(d)
          tooltip.html(d.data["name"]+"<br />"+d.data["value"])
            .style("left", (e.pageX) + "px")
            .style("top", (e.pageY + 20) + "px")
            .style("opacity", 1.0)
        })
        .on("mousemove", function (e, d) {
          tooltip.style("left", (e.pageX) + "px")
            .style("top", (e.pageY + 20) + "px")

        })
        .on("mouseout", function (d) {
          tooltip.style("opacity", 0)
        })

      // if (T) {
      //   node.append("title").text((d, i) => T[i])
      // }

      // if (L) {
      //   // A unique identifier for clip paths (to avoid conflicts).
      //   // const uid = `O-${Math.random().toString(16).slice(2)}`;

      //   // node.append("clipPath")
      //   //    .attr("id", (d, i) => `${uid}-clip-${i}`)
      //   //  .append("rect")
      //   //    .attr("width", d => d.x1 - d.x0)
      //   //    .attr("height", d => d.y1 - d.y0);

      //   // node.append("text")
      //   //     .attr("clip-path", (d, i) => `url(${new URL(`#${uid}-clip-${i}`, location)})`)
      //   //   .selectAll("tspan")
      //   //   .data((d, i) => `${L[i]}`.split(/\n/g))
      //   //   .join("tspan")
      //   //     .attr("x", 3)
      //   //     .attr("y", (d, i, D) => `${(i === D.length - 1) * 0.3 + 1.1 + i * 0.9}em`)
      //   //     .attr("fill-opacity", (d, i, D) => i === D.length - 1 ? 0.7 : null)
      //   //     .text(d => d);   
      //   node.append("text")
      //     //   .attr("clip-path", (d, i) => `url(${new URL(`#${uid}-clip-${i}`, location)})`)
      //     // .selectAll("tspan")
      //     // .data((d, i) => `${L[i]}`.split(/\n/g))
      //     // .join("tspan")
      //     //   .attr("x", 3)
      //     //   .attr("y", (d, i, D) => `${(i === D.length - 1) * 0.3 + 1.1 + i * 0.9}em`)
      //     //   .attr("fill-opacity", (d, i, D) => i === D.length - 1 ? 0.7 : null)
      //     .text(d => { return d.data["name"].split("/")[1] + "\t" + d.data["value"] })
      //     .attr("transform", d => `translate(${d.x0},${(d.y0 + d.y1) / 2})`)
      //     .attr("fill-opacity", d => {
      //       if (d.data["value"] < max_data / 3)
      //         return 0
      //       return 1
      //     })

      // }
      this.svg = svg
      this.node = node
      this.tooltip = tooltip

      // Object.assign(svg.node(), {scales: {color}});
    },

    update (data1) {
      //    console.log("啊啊啊啊啊啊啊啊啊啊啊啊")
      //    var linkTarget = "_blank";
      //    var path= d => d.name.replace(/\./g, "/"); // e.g., "flare/animate/Easing"
      // var value= d => d?.value; // size of each node (file); null for internal nodes (folders)
      // var group= d => d.name.split(".")[1]; // e.g., "animate" in "flare.animate.Easing"; for color
      // var label= (d, n) => [...d.name.split(".").pop().split(/(?=[A-Z][a-z])/g), n.value.toLocaleString("en")].join("\n");
      // var title= (d, n) => `${d.name}\n${n.value.toLocaleString("en")}`; // text to show on hover
      // var link=(d, n) => `https://github.com/prefuse/Flare/blob/master/flare/src${n.id}.as`;
      // var width= 550;
      // var height= 250;
      // var tile = d3.treemapBinary ;
      // var colors = d3.schemeTableau10;
      // var margin = 0 // shorthand for margins
      // var marginTop = margin // top margin, in pixels
      // var marginRight = margin // right margin, in pixels
      // var marginBottom = margin // bottom margin, in pixels
      // var marginLeft = margin // left margin, in pixels
      // var padding = 1 // shorthand for inner and outer padding
      // var paddingInner = padding // to separate a node from its adjacent siblings
      // var paddingOuter = padding // shorthand for top, right, bottom, and left padding
      // var paddingTop = paddingOuter // to separate a node’s top edge from its children
      // var paddingRight = paddingOuter // to separate a node’s right edge from its children
      // var paddingBottom = paddingOuter // to separate a node’s bottom edge from its children
      // var paddingLeft = paddingOuter // to separate a node’s left edge from its children
      // var round = true

      //  const data1 = [{ "name": "a/aa", "value": 54 }
      //   , { "name": "a/b", "value": 51 }
      //   , { "name": "a/c", "value": 79 }
      //   , { "name": "a/d", "value": 97 }
      //   , { "name": "a/e", "value": 6 }
      //   , { "name": "a/ff", "value": 48 }
      //   , { "name": "b/a", "value": 46 }
      //   , { "name": "b/b", "value": 49 }
      //   , { "name": "b/c", "value": 90 }
      //   , { "name": "b/d", "value": 27 }
      //   , { "name": "c/aa", "value": 21 }
      //   , { "name": "c/b", "value": 18 }
      //   , { "name": "c/c", "value": 62 }
      //   , { "name": "c/d", "value": 24 }
      //   , { "name": "c/e", "value": 29 }
      // ]
      //  var id = Array.isArray(data1) ? d => d.id : null; // if tabular data, given a d in data, returns a unique identifier (string)
      //   var parentId = Array.isArray(data1) ? d => d.parentId : null; // if tabular data, given a node d, returns its parent’s identifier
      //   var children= undefined;
      // const root1 = d3.stratify().path(d => d.name.replace(/\./g, "/"))(data1)

      //   console.log(root1)
      //   // debugger
      //   // Compute the values of internal nodes by aggregating from the leaves.
      //   // root.sum(d => Math.max(0, value(d)));
      //   root1.sum(function(d)
      //   {
      //     if (d!=null)
      //     return Math.max(0, value(d))
      //     else
      //     return 0
      //   })
      //   // Prior to sorting, if a group channel is specified, construct an ordinal color scale.
      //   const leaves = root1.leaves();
      //   console.log("leaves",leaves)
      //   // const G = group == null ? null : leaves.map(d => group(d.data["name"]));
      //   const G = leaves.map(d=>d.data["name"].split("/")[0])
      //   var zDomain = G;
      //   zDomain = new d3.InternSet(zDomain);//去重
      //   const color = group == null ? null : d3.scaleOrdinal(zDomain, colors);

      //   // Compute labels and titles.
      //   const L = label == null ? null : leaves.map(d => label(d.data, d));
      //   const T = title === undefined ? L : title == null ? null : leaves.map(d => title(d.data, d));
      //   console.log(L)
      //   console.log(T)
      //   // Sort the leaves (typically by descending value for a pleasing layout).
      //   // if (sort != null) root.sort(sort);

      //   // Compute the treemap layout.
      //   const treemap1 =  d3.treemap()
      //       .tile(tile)
      //       .size([width - marginLeft - marginRight, height - marginTop - marginBottom])
      //       .paddingInner(paddingInner)
      //       .paddingTop(paddingTop)
      //       .paddingRight(paddingRight)
      //       .paddingBottom(paddingBottom)
      //       .paddingLeft(paddingLeft)
      //       .round(round);
      //   treemap1(root1);
      //   console.log(treemap1)
      var res = this.preprocess(data1)
      var leaves = res[0]
      var L = res[1]
      var T = res[2]
      var G = res[3]
      var color = res[4]
      var text_opacity = res[5]
      var max_data = Math.max.apply(null, data1.map(d => d.value))
      var tooltip = this.tooltip
      console.log("leavessssssssssssssssssssssssssssssssssssssssssss")
      console.log(leaves)
      console.log(this.svg.selectAll("rect"))

      //  this.svg.selectAll("a").data(leaves).transition()
      //       .duration(500)
      //       .ease(d3.easeLinear)

      //   console.log(this.svg.selectAll("rect"))
      
      //3-10代码
      let nodes = this.svg.selectAll("rect").data(leaves).join("rect")
        .transition()
        .duration(500)
        .ease(d3.easeLinear)
        .attr("transform", d => { console.log(d); return `translate(${d.x0},${d.y0})` })
        .attr("width", d => { console.log(d); return d.x1 - d.x0 })
        .attr("height", d => d.y1 - d.y0)
        .attr("fill", (d, i) => color(G[i]))
        .attr("fill-opacity", 0.6)
        this.svg.selectAll("rect")
        .on("click", function (e, d) {//e是鼠标事件 d是每个方块挂载的数据 可以通过此处传递信息出去
          // console.log()
          console.log("splited", d.id.split("/")[1])
          bus.$emit("SelectEvent", d.id.split("/")[1])})
        .on("mouseover", function (e, d) {
          console.log(d)
          tooltip.html(d.data["name"]+"<br />"+d.data["value"])
            .style("left", (e.pageX) + "px")
            .style("top", (e.pageY + 20) + "px")
            .style("opacity", 1.0)
        })
        .on("mousemove", function (e, d) {
          tooltip.style("left", (e.pageX) + "px")
            .style("top", (e.pageY + 20) + "px")

        })
        .on("mouseout", function (d) {
          tooltip.style("opacity", 0)
        })


        this.svg.selectAll("text")
        .data(leaves)
        .join("text")
        .transition()
        .duration(500)
        .ease(d3.easeLinear)
        .text(d => { return d.data["name"].split("/")[1] + "\t" + d.data["value"] })
        .attr("transform", d => `translate(${d.x0},${(d.y0 + d.y1) / 2})`)
        .attr("fill-opacity", d => {
          if (d.data["value"] < max_data / 3)
            return 0
          return 1
        })
      // console.log("老节点选择",nodes)
      // nodes.selectAll("rect").remove()
      // nodes.selectAll("title").remove()
      // nodes.selectAll("text").remove()
      // console.log("节点选择",nodes)
      // console.log("数树叶",leaves)

      // let nodes = this.svg.selectAll("a")
      // nodes.data(leaves).enter().append("a")
      //   // .join("a")
      // // let nodes = this.svg.selectAll("a")
      // console.log("新节点选择",nodes)
      
      // nodes.append("rect")
      //   .attr("fill", (d, i) => color(G[i]))
      //   .attr("fill-opacity", 0.6)
      //   .attr("stroke", 1)
      //   .attr("transform", d => `translate(${d.x0},${d.y0})`)
      //   // .attr("stroke-width", strokeWidth)
      //   // .attr("stroke-opacity", strokeOpacity)
      //   // .attr("stroke-linejoin", strokeLinejoin)
      //   .attr("width", d => { return d.x1 - d.x0 })
      //   .attr("height", d => d.y1 - d.y0)
      //   .on("click", function (e, d) {//e是鼠标事件 d是每个方块挂载的数据 可以通过此处传递信息出去
      //     // console.log()
      //     console.log("splited", d.id.split("/")[1])
      //     bus.$emit("SelectEvent", d.id.split("/")[1])
      //   })

      // nodes.append("title").text((d, i) => T[i])
      // nodes.append("text")
      //   .text(d => { return d.data["name"].split("/")[1] + "\t" + d.data["value"] })
      //   .attr("transform", d => `translate(${d.x0},${(d.y0 + d.y1) / 2})`)
      //   .attr("fill-opacity", d => {
      //     if (d.data["value"] < max_data / 3)
      //       return 0
      //     return 1
      //   })
      // nodes.transition()
      //   .duration(500)
      //   .ease(d3.easeLinear)


      //1月能用
      // let nodes = this.svg.selectAll("rect").data(leaves)
      //  console.log("只有rect",nodes) 
      //   nodes.join("rect").transition()
      //   .duration(500)
      //   .ease(d3.easeLinear)
      //   .attr("transform", d => {  return `translate(${d.x0},${d.y0})` })
      //   .attr("width", d => {  return d.x1 - d.x0 })
      //   .attr("height", d => d.y1 - d.y0)
      //   .attr("fill", (d, i) => color(G[i]))
      //   .attr("fill-opacity", 0.6)
      //   .on("click", function (e, d) {//e是鼠标事件 d是每个方块挂载的数据 可以通过此处传递信息出去
      //     // console.log()
      //     // console.log("splited", d.id.split("/")[1])
      //     bus.$emit("SelectEvent", d.id.split("/")[1])
      //   })



      // .attr("stroke", stroke)
      // .attr("transform", d => `translate(${d.x0},${d.y0})`)
      // .attr("stroke-width", strokeWidth)
      // .attr("stroke-opacity", strokeOpacity)
      // .attr("stroke-linejoin", strokeLinejoin); 
      // node.append("title").text((d, i) => T[i])

      //能用
      // this.svg.selectAll("title").data(leaves).join("title").transition()
      //   .duration(500).text((d, i) => T[i])
      // this.svg.selectAll("text").data(leaves).join("text").transition()
      //   .duration(500)
      //   .text(d => { return d.data["name"].split("/")[1] + "\t" + d.data["value"] })
      //   .attr("transform", d => `translate(${d.x0},${(d.y0 + d.y1) / 2})`)
      //   .attr("fill-opacity", d => {
      //     if (d.data["value"] < max_data / 3)
      //       return 0
      //     return 1
      //   })
      // this.sleep(2000)
    }

  },
}
</script>

<style >
#topk_thre {
  display: flex;
  /* align-items: start; */
  justify-content: flex-start;
  /* flex-direction: row; */
}
</style>