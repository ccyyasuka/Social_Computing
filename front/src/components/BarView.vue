<template>
  <div>
    <div id="panel">
      <h5 class='thre-title' id="salthre_title">Sampling Ratio</h5>
        <a-slider
              id="sample_proportion"
              :max="1"
              :min="0.05"
              :step="0.05"
              :default-value="0.5"
              style="width: 300px; margin-left: 22px"
              @afterChange="change_proportion"
            />
      <h5 class='thre-title' id="salthre_title">Time Span</h5>
      <a-select
        default-value="hour"
        style="width: 120px; margin-left: 22px"
        @change="ChangeDayYear">
        <a-select-option value="hour"> Hour </a-select-option>
      <a-select-option value="day">Day</a-select-option>
        
      </a-select>
      
    </div>
   <div v-if="loading" id="loading_spin">
      <a-spin :spinning="loading" />
    </div>
      
    <div id="Bar" >
      <svg id="BarSvg"></svg>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3"
import axios from "axios"
import bus from "./bus.js"
// import { DownOutlined } from '@ant-design/icons-vue';

export default {
  name: "BarView",
  props: {
    TimeSpan: {
      type: Array
    },
  },
  created () {
    //初始化时 created必然被调用 但是$on里面的东西只有传值进来才被调用
    bus.$on("SelectEvent", (val) => {
      console.log(val)
      console.log(this.TimeSpan)
      this.event = val
      
      this.loading = true
      let param = { "start": this.TimeSpan[0], "end": this.TimeSpan[1], "event": this.event, "day_or_year": this.day_or_year,"proportion":this.proportion }
      console.log("拿到了event!!!!!!!", param)
      axios
        .post("http://10.192.9.11:9931/api/sentiment", param)
        .then((response) => {
          this.data = response.data["res"]
          console.log("拿到了结果data!!!!!!!", this.data)
          this.loading = false
          
          this.init()
          
        })

    })



  },
  mounted () {
    // this.init()
  },
  data () {
    return {
      path: "http://127.0.0.1/15655/Bar",
      svg: null,
      event: null,
      // test_this.data2: [{ 'name': 'sydneysiege/', 'value': 12341 }, { 'name': 'sydneysiege/@user', 'value': 12141 }, { 'name': 'ottawashooting/', 'value': 10360 }, { 'name': 'charliehebdo/', 'value': 9817 }, { 'name': 'ottawashooting/@user', 'value': 9234 }, { 'name': 'charliehebdo/@user', 'value': 8929 }, { 'name': 'germanwings/', 'value': 3907 }, { 'name': 'germanwings/@user', 'value': 3682 }, { 'name': 'sydneysiege/the', 'value': 3185 }, { 'name': 'ottawashooting/the', 'value': 2106 }, { 'name': 'charliehebdo/the', 'value': 2079 }, { 'name': 'sydneysiege/httpurl', 'value': 1892 }, { 'name': 'sydneysiege/to', 'value': 1842 }, { 'name': 'charliehebdo/httpurl', 'value': 1747 }, { 'name': 'sydneysiege/in', 'value': 1636 }, { 'name': 'charliehebdo/in', 'value': 1632 }, { 'name': 'sydneysiege/is', 'value': 1535 }, { 'name': 'sydneysiege/a', 'value': 1523 }, { 'name': 'ottawashooting/in', 'value': 1495 }, { 'name': 'sydneysiege/not', 'value': 1387 }, { 'name': 'sydneysiege/!', 'value': 1384 }, { 'name': 'charliehebdo/to', 'value': 1352 }, { 'name': 'ottawashooting/to', 'value': 1336 }, { 'name': 'ottawashooting/httpurl', 'value': 1283 }, { 'name': 'sydneysiege/of', 'value': 1257 }, { 'name': 'charliehebdo/of', 'value': 1229 }, { 'name': 'ottawashooting/a', 'value': 1170 }, { 'name': 'sydneysiege/sydney', 'value': 1148 }, { 'name': 'ottawashooting/!', 'value': 1144 }, { 'name': 'ottawashooting/is', 'value': 1118 }, { 'name': 'charliehebdo/a', 'value': 1041 }, { 'name': 'charliehebdo/!', 'value': 1035 }, { 'name': 'ottawashooting/of', 'value': 1023 }, { 'name': 'sydneysiege/you', 'value': 1006 }, { 'name': 'sydneysiege/and', 'value': 1003 }],
      // test_this.data1: [{ 'name': 'sydneysiege/', 'value': 12341 }, { 'name': 'sydneysiege/@user', 'value': 12141 }, { 'name': 'charliehebdo/', 'value': 9817 }, { 'name': 'charliehebdo/@user', 'value': 8929 }, { 'name': 'sydneysiege/the', 'value': 3185 }, { 'name': 'charliehebdo/the', 'value': 2079 }, { 'name': 'sydneysiege/httpurl', 'value': 1892 }, { 'name': 'sydneysiege/to', 'value': 1842 }, { 'name': 'charliehebdo/httpurl', 'value': 1747 }, { 'name': 'sydneysiege/in', 'value': 1636 }, { 'name': 'charliehebdo/in', 'value': 1632 }, { 'name': 'sydneysiege/is', 'value': 1535 }, { 'name': 'sydneysiege/a', 'value': 1523 }, { 'name': 'sydneysiege/not', 'value': 1387 }, { 'name': 'sydneysiege/!', 'value': 1384 }, { 'name': 'charliehebdo/to', 'value': 1352 }, { 'name': 'sydneysiege/of', 'value': 1257 }, { 'name': 'charliehebdo/of', 'value': 1229 }, { 'name': 'sydneysiege/sydney', 'value': 1148 }, { 'name': 'charliehebdo/a', 'value': 1041 }, { 'name': 'charliehebdo/!', 'value': 1035 }, { 'name': 'sydneysiege/you', 'value': 1006 }, { 'name': 'sydneysiege/and', 'value': 1003 }, { 'name': 'charliehebdo/paris', 'value': 967 }, { 'name': 'sydneysiege/i', 'value': 939 }, { 'name': 'charliehebdo/is', 'value': 923 }, { 'name': 'sydneysiege/sydneysiege', 'value': 874 }, { 'name': 'charliehebdo/not', 'value': 869 }, { 'name': 'sydneysiege/are', 'value': 844 }, { 'name': 'charliehebdo/and', 'value': 819 }, { 'name': 'sydneysiege/it', 'value': 793 }, { 'name': 'sydneysiege/this', 'value': 786 }, { 'name': 'sydneysiege/that', 'value': 776 }, { 'name': 'sydneysiege/hostages', 'value': 747 }, { 'name': 'sydneysiege/cafe', 'value': 676 }],
      data: null,
      day_or_year: "hour",
      proportion:0.5,
      loading :false,
      
    }
  },
  methods: {
    ChangeDayYear (value) {
      this.day_or_year = value
      // let param = { "start": this.TimeSpan[0], "end": this.TimeSpan[1], "event": this.event, "day_or_year": this.day_or_year,"sample_mode":this.sample_mode }
      // console.log("拿到了event!!!!!!!", param)
      // axios
      //   .post("http://10.192.9.11:9931/api/sentiment", param)
      //   .then((response) => {
      //     this.data = response.data["res"]
      //     console.log("拿到了结果data!!!!!!!", this.data)
      //     this.init()
      //   })
      if (this.event!=null)
      {
        let param = { "start": this.TimeSpan[0], "end": this.TimeSpan[1], "event": this.event, "day_or_year": this.day_or_year,"proportion":this.proportion }
        console.log("拿到了event!!!!!!!", param)
        axios
          .post("http://10.192.9.11:9931/api/sentiment", param)
          .then((response) => {
            this.data = response.data["res"]
            console.log("拿到了结果data!!!!!!!", this.data)
            this.loading = false
            
            this.init()
            
          })
      }
      
    },
    change_proportion(value){
      this.proportion = value
      if (this.event!=null)
      {
        let param = { "start": this.TimeSpan[0], "end": this.TimeSpan[1], "event": this.event, "day_or_year": this.day_or_year,"proportion":this.proportion }
        console.log("拿到了event!!!!!!!", param)
        axios
          .post("http://10.192.9.11:9931/api/sentiment", param)
          .then((response) => {
            this.data = response.data["res"]
            console.log("拿到了结果data!!!!!!!", this.data)
            this.loading = false
            
            this.init()
            
          })
      }
      
    },
    init () {
      // this.data = [
      //   { "date": '1988-01-01', "pos": 0.9, "neg": 0.9 },
      //   { "date": '1988-01-02', "pos": 0.8, "neg": 0.5 },
      //   { "date": '1988-01-03', "pos": 0.7, "neg": 0.2 },
      //   { "date": '1988-01-04', "pos": 0.6, "neg": 0.1 },
      //   { "date": '1988-01-05', "pos": 0.5, "neg": 0.15 },
      //   { "date": '1988-01-06', "pos": 0.6, "neg": 0.4 },
      //   { "date": '1988-01-07', "pos": 0.7, "neg": 0.3 },
      //   { "date": '1988-01-08', "pos": 0.9, "neg": 0.9 },
      //   { "date": '1988-01-09', "pos": 0.8, "neg": 0.5 },
      //   { "date": '1988-01-10', "pos": 0.7, "neg": 0.2 },
      //   { "date": '1988-01-11', "pos": 0.6, "neg": 0.1 },
      //   { "date": '1988-01-12', "pos": 0.5, "neg": 0.15 },
      //   { "date": '1988-01-13', "pos": 0.6, "neg": 0.4 },
      //   { "date": '1988-01-14', "pos": 0.7, "neg": 0.3 },
      // ]
      this.draw()
      console.log(this.event)

    },
    draw () {
      let that=this//记录
      // console.log("0000000000000000000000000000000000000")
      d3.select("#BarSvg").selectAll("*").remove()//删除BarSvg下面所有已有的dom 但是BarSvg不删除
      const height = 360
      const width = 900
      let margin = ({ top: 20, right: 0, bottom: 30, left: 40 })


      console.log(this.data.map(d => d.date))
      // all_time = d3.extent(this.data, d => d.date)
      let x = d3.scaleBand()
        .domain(this.data.map(d => d.date))
        .range([margin.left, width - margin.right])
        .padding(0.1)
      console.log("111111111111111111111111111111111111111111111111")
      let y = d3.scaleLinear()//￥记录 y轴的生成原理
        .domain([0, 1]).nice()
        // .range([(height - margin.bottom)/2, margin.top])
        .range([(height - margin.bottom), margin.top])//280 30
      let y1 = d3.scaleLinear()
        .domain([0, 1]).nice()
        // .range([(height - margin.bottom)/2, margin.top])
        .range([height / 2, margin.top])//150 30

      let y2 = d3.scaleLinear()
        .domain([0, 1]).nice()
        // .range([(height - margin.bottom)/2, margin.top])
        .range([height / 2, height - margin.top])//270 150

      let xAxis = g => g
        .attr("transform", `translate(0,${height / 2})`)
        .call(d3.axisBottom(x).tickSizeOuter(0))
      let yAxis1 = g => g
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y1))
        .call(g => g.select(".domain").remove())
      let yAxis2 = g => g
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y2))
        .call(g => g.select(".domain").remove())

      //添加提示框
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

      const svg = d3.selectAll("#Bar").select("#BarSvg")
        // .attr("viewBox", [0, 0, width*2, 2*height])
        // .attr("id","BarSvg")
        .attr("width", width)
        .attr("height", height)
        .call(zoom)
      console.log("222222222222222222222222222222222222")
      svg.append("g")
        .attr("class", "bars")
        .attr("fill", "#226DDD")
        .style("opacity", 0.5)
        .selectAll("rect")
        .data(this.data)
        .join("rect")
        .attr("x", d => x(d.date))
        .attr("y", d => y1(d.pos))
        .attr("height", d => y1(0) - y1(d.pos))
        .attr("width", x.bandwidth())
        .on("mouseover", function (e, d) {
          console.log(d)
          tooltip.html(d.date + "<br />" + d.pos)
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
        .on("click", function (e, d) {
          // console.log("event", this.event)
          bus.$emit("SelectTime", { "date": d.date, "event": that.event })
          console.log("SelectTime",d.date)
        })


      svg.append("g")
        .attr("class", "bars")
        .attr("fill", "#C43CC4")
        .style("opacity", 0.5)
        .selectAll("rect")
        .data(this.data)
        .join("rect")
        .attr("x", d => x(d.date))
        .attr("y", d => y1(0))
        .attr("height", d => y1(0) - y1(d.neg))
        .attr("width", x.bandwidth())
        .on("mouseover", function (e, d) {
          console.log(d)
          tooltip.html(d.date + "<br />" + d.neg)
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
        .on("click", function (e, d) {
          // console.log("event", this.event)
          bus.$emit("SelectTime", { "date": d.date, "event": that.event })
        })

      svg.append("g")
        .attr("class", "x-axis")
        .call(xAxis)
        .call(g => g.selectAll(".tick").remove())

      svg.append("g")
        .attr("class", "y-axis")
        .call(yAxis1)
      svg.append("g")
        .attr("class", "y-axis")
        .call(yAxis2)


      //￥记录
      function zoom (svg) {
        const extent = [[margin.left, margin.top], [width - margin.right, height - margin.top]]
        console.log(extent)
        svg.call(d3.zoom()
          .scaleExtent([1, 8])
          .translateExtent(extent)
          .extent(extent)
          .on("zoom", zoomed))

        function zoomed (event) {
          x.range([margin.left, width - margin.right].map(d => event.transform.applyX(d)))
          svg.selectAll(".bars rect").attr("x", d => x(d.date)).attr("width", x.bandwidth())
          svg.selectAll(".x-axis").call(xAxis)
            .call(g => g.selectAll(".tick").remove())//￥记录
        }
      }


    }
  },




}
</script>

<style >
#panel {
  display:flex;
  justify-content: flex-start;
  padding: 0 10% 0 0;
  flex:0 0 70%;
}
#loading_spin
{
  text-align: center
}
.thre-title{
  font-size:120%
}
</style>