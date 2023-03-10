<template>
  <a-table :columns="columns" :data-source="data" :pagination="{ pageSize: 10 }" :scroll="{ y: 200 }" :customRow="customRow">
    <span slot="tags" slot-scope="tags">
      <a-tag
        v-for="tag in tags"
        :key="tag"
        :color="tag === 'neg' ?  'geekblue' : 'green'"
      >
        {{ tag.toUpperCase() }}
      </a-tag>
    </span>
    
  </a-table>
</template>

<script>
import axios from "axios"
import bus from "./bus"
      const columns = [
        {
          title: 'mid',
          dataIndex: 'mid',
          width: 100,
        },
        {
          title: 'content',
          dataIndex: 'content',
          
        },
        {
          title: 'tags',
          dataIndex: 'tags', 
          width: 100,
          scopedSlots: { customRender: 'tags' }//记录
        },
      ];
  export default {
    name: "TextList",
    mounted () {
      
    },
    created () {
      bus.$on("SelectTime",(val) => {
      this.date=val["date"]
      this.event=val["event"]
      let param ={"date": this.date, "event": this.event} 
      console.log("拿到了date&event!!!!!!!",param)
      axios
        .post("http://10.192.9.11:9931/api/textlist", param)
        .then((response) => {
          this.data = response.data["res"]
          console.log("拿到了结果data!!!!!!!",this.data)
          // this.init()
        })
      
    });
    },
    data() {
      return {
        data:[],
        columns:columns,
        date:null,
        event:null
      }
    },
    methods: {
      customRow(record) {
        return{
        on:{
          click:(event)=>{
            console.log(record)
            bus.$emit('content2triple',record.content)
            // console.log(e.srcElement)
            // d3.selectAll('.ant-table-row-cell-break-word')
            // .style('background-color', '#ffffff')
            // d3.select(e.srcElement)
            // .style('background-color', '#e6f7ff')
          }
        }
      }
      }
    },
  }
</script>

<style scoped>

</style>