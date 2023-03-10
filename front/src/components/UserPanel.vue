<template>
  <div id="panel_view">
    <div id="csv_input">
      <input type="file" id="files" ref="refFile" v-on:change="importCsv" />
    </div>
    <div v-if="loading" id="loading">
      <a-spin :spinning="loading" />
    </div>
    <div id="static" v-if="loaded">
      <!-- 记录 vif等vue命令 -->
      <a-statistic
        title="data_count"
        :value="data_count"
      />
      <a-statistic title="top event" :value="top_event" />
      <a-statistic title="top event frequency" :value="freq" />
      <a-statistic title="earlist time" :value="earlist" />
      <a-statistic title="latest time" :value="latest" />
    </div>
  </div>
</template>

<script>
import axios from "axios"
import Papa from 'papaparse'
export default {
  name: "UserPanel",
  data () {
    return {
      data_count: null,
      top_event: null,
      freq: null,
      loading: false,
      loaded: false,
      not_enough_keys_error:false,
      headers: {
        authorization: 'authorization-text',
      },
      latest:null,
      earlist:null
    }
  },
  methods: {
    importCsv () 
    {
      let selectedFile = null
      try
      {
        this.loaded=false
        this.loading=true
        selectedFile = this.$refs.refFile.files[0]
        if (selectedFile === undefined) {
          return
        }
        
        var reader = new FileReader()
        reader.readAsDataURL(selectedFile)
        reader.onload = evt => {
          // 检查编码
          let encoding = this.checkEncoding(evt.target.result)
          // 将csv转换成二维数组
          Papa.parse(selectedFile, {
            encoding: encoding,
            complete: res => {
              // UTF8 \r\n与\n混用时有可能会出问题
              let data = res.data
              if (data[data.length - 1] == "") {
                //去除最后的空行
                data.pop()
              }
              console.log(data)  // data就是文件里面的数据

              var param = { "list": data }
              axios
                .post("http://10.192.9.11:9931/api/convert2df", param)
                .then((response) => {
                  res = response.data["res"][0]
                  console.log(res)
                  if (res["data_count"]=="don't enough keys")
                  {
                      this.HasError=true
                  }
                  else
                  {
                    this.data_count = res["data_count"]
                    this.top_event = res["top_event"]
                    this.freq = res["freq"]
                    this.earlist = res["earlist"]
                    this.latest = res["latest"]
                    this.loading=false
                    this.loaded = true 
                  }
                  
                })


            }
          })
        }
      }
      catch
      {
        alert("Error: The selected file should be a csv file")
      }
      
    },
    checkEncoding (base64Str) {
      // 这种方式得到的是一种二进制串
      var str = atob(base64Str.split(';base64,')[1])
      // console.log(str);
      // 要用二进制格式
      const jschardet = require("jschardet")
      var encoding = jschardet.detect(str)
      encoding = encoding.encoding
      // console.log( encoding );
      if (encoding === 'windows-1252') {	// 有时会识别错误（如UTF8的中文二字）
        encoding = 'ANSI'
      }
      return encoding
    }
  },
}
</script>

<style>
#panel_view {
  display: flex;
  flex-direction: row;
  height: 80%;
  width: 100%;
  float:left
}
#static {
  display: flex;
  gap: 30px;
  flex-direction: row;
  height: 80%;
  width: 70%;
  justify-content: center/* 针对flex的居中 */
  /* text-align: center 传统居中布局 */
  /* 设为 Flex 布局以后，子元素的float、clear和vertical-align属性将失效。 */
}
#csv_input
{
  text-align:center
}
#loading {
  display: flex;
  flex-direction: row;
  height: 80%;
  width: 70%;
  justify-content: center/* 针对flex的居中 */
  /* text-align: center 传统居中布局 */
  /* 设为 Flex 布局以后，子元素的float、clear和vertical-align属性将失效。 */
}
</style>