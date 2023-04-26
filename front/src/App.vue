<template>
  <div id="app">
    <div id="user_panel" class="view">
      <h2>User Panel</h2>
      <UserPanel/>
    </div>
    <div id="views">
      <div id="left_col">
        <div id="left_up" class="view">
          <h2>Word Frequency</h2>
          <TreeMap />
        </div>
        <div id="TextList" class="view">
          <h2>Event Extraction</h2>
          <div id="left_middle">
            <!-- <que-card :key="refresh" :model_prop="model"></que-card> -->
            <TextList />
          </div>
          <div id="left_bottom">
            <TripleTree/>
          </div>
        </div>
      </div>
      <div id="right_col">
        <div id="right_up" class="view">
          <h2>Trend of Emotion</h2>
          <BarView :TimeSpan="TimeSpan"></BarView>
        </div>
        <div id="right_bottom" class="view">
          <h2>View 4</h2>
          <RumorTree/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import TreeMap from './components/TreeMap.vue'
import BarView from './components/BarView.vue'
import bus from "./components/bus.js"
import TextList from './components/TextList.vue'
import UserPanel from './components/UserPanel.vue'
import TripleTree from './components/TripleTree.vue'
import RumorTree from './components/RumorTree.vue'
export default {
  name: 'App',
  created () {
    bus.$on("TimeSpan", (val) => {
      this.TimeSpan = val
    })
  },
  data () {
    return {
      TimeSpan: undefined
    }
  },
  components: {
    TreeMap,
    BarView,
    TextList,
    UserPanel,
    TripleTree,
    RumorTree
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  color: #2c3e50;
  margin-top: 10px;
  background: rgb(255, 255, 255);
  display: flex;
  /* 设定布局 */
  height: 100%;
  width: 100%;
  overflow: auto;
  /* 如果块超出了空间怎么办 auto */
  flex-direction: column;
}
#user_panel {
  flex: 0 0 /* 35% */ 100px;
  flex-direction: column;
}
#views {
  flex: 0 0 auto;
  flex-direction: row;
  display: flex;
}
#left_col {
  flex: 0 0 /* 35% */ 720.6px;
  display: flex;
  flex-direction: column;
  overflow: hidden;

  /* margin-bottom: 10px; */
}

/* #rightCol {
    flex: 0 0
  } */

#left_up {
  flex: 0 0 /* 50% */ 440px;
  overflow: hidden;
  justify-content: space-between;
}
#TextList {
  display: flex;
  overflow: hidden;
  flex-direction: column;
  flex: 0 0 640px;
}
#left_middle {
  flex: 0 0 /* 50% */ 320px;
  margin: 0 5%;
  overflow: hidden;
  justify-content: space-between;
}
#left_bottom {
  flex: 0 0 /* 50% */ 320px;
  overflow: hidden;
  justify-content: space-between;
}
#right_col {
  display: flex;
  flex: 0 0 950px;
  flex-direction: column;
  overflow: hidden;
  /* justify-content: space-between; */
}
#right_up {
  flex: 0 0 /* 50% */ 440px;
  overflow: hidden;
  justify-content: space-between;
}
#right_bottom {
  flex: 0 0 /* 50% */ 640px;
  overflow: hidden;
  justify-content: space-between;
}
.view {
  margin: 5px;
  border: 1px solid #ccc !important;
  /* padding:5px 5px 5px 2px; */
  border-radius: 6px;
  /* box-shadow: 2.5px 2.5px 10px rgb(180, 180, 180); */
  overflow: hidden;
  height: 50%;
}
h2 {
  font-size: 15px;
  background: #f1f1f1;
  margin: 0;
}
</style>
