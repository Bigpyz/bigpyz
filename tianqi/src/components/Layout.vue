<script setup>
import {ref,onMounted,watch} from 'vue'
import {getTem} from '../option/temperature.js';
import { getWater } from '../option/water.js';
import { getPre } from '../option/precipitation.js';
import { getWind } from '../option/wind.js';
import {getHum} from '../option/wei.js';
import http from '../api/http';

import Echarts from './Echarts.vue'
import Form from './Form.vue'
import { ElLoading } from 'element-plus'
const tem =ref(null)
const option = ref(null)
const TemWidth = ref('70.25rem');
const TemHeight = ref('32.0000rem');
const PreWidth = ref('25.25rem');
const PreHeight = ref('19.3000rem');
const date = ref(2024);
const fullscreenLoading = ref(false)

function onSomeValueChanged(newValue, oldValue) {
      console.log(`someValue changed from ${oldValue} to ${newValue}`);
      // 在这里执行其他操作
      wendu()
    }
 
    // 使用 watch 来观察 someValue 的变化
    watch(date, onSomeValueChanged);
const options = [
  {
    value: 2020,
    label: '2020',
  },
  {
    value: 2021,
    label: '2021',
  },
  {
    value: 2022,
    label: '2022',
  },
  {
    value: 2023,
    label: '2023',
  },
  {
    value: 2024,
    label: '2024',
  },
]
// 函数来更新 tem 的值
const pach = async()=>{
  fullscreenLoading.value = true
  const loading = ElLoading.service({
    lock: true,
    text: 'Loading',
    background: 'rgba(0, 0, 0, 0.7)',
  })
  await http.post(`/scrapy`)
  loading.close()
  fullscreenLoading.value = false
  window.location.reload();
  
}
const wendu = async() => {
  tem.value = null;
   await getTem(date.value).then(data=>{
    tem.value = data
  })
  console.log(tem.value);
};
 
const shidu = async() => {
  tem.value = null;
  await getPre(date.value).then(data=>{
    tem.value = data
  })
  console.log(tem.value);
};
 
const jiangshui = async() => {
  tem.value = null;
  await getWater(date.value).then(data=>{
    tem.value = data
  })
  console.log(tem.value);
};
 
const feng = async() => {
  tem.value = null;
  await getWind(date.value).then(data=>{
    tem.value = data
  })
  console.log(tem.value);
};
function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // 月份从0开始，所以需要+1，并补0
    const day = String(date.getDate()).padStart(2, '0'); // 补0
 
    return `${year}年${month}月${day}日`;
}

wendu()

// 在组件挂载之前获取数据
onMounted(async () => {
  const date = new Date().getFullYear();
  const d = formatDate(new Date()); 
  await http.get(`/wind/${date}`).then(res=>{
   console.log(res.data);
  if(res.data.code === 200){
    const {dates,winds} = res.data.data;
    console.log(dates);
    console.log(d);
    const index = dates.indexOf(d);
    console.log(index);
    console.log(winds[index]);
    option.value = getHum(winds[index]);

  }
})
});
</script>

<template>
 <div class="con">
  <div class="header">桂林市天气数据统计   

    <el-button 
      v-loading.fullscreen.lock="fullscreenLoading"
      id="pc" 
      type="primary" 
      @click="pach()"> 开始爬取 </el-button>
  </div>
   
 
 <div id="box">
  <div class="main-left" style="margin-left: 1%;">
        <!--条形图-->
        <div class="border-container" >        
         <Form/>

        <span class="top-left border-span"></span>
            <span class="top-right border-span"></span>
            <span class="bottom-left border-span"></span>
            <span class="bottom-right border-span"></span>
        </div>
        <!--折线图-->
        <div class="border-container">    
            <Echarts v-if="option" :dataSource="option" :canvasWidth="PreWidth" :canvasHeight="PreHeight"></Echarts> 
            <span class="top-left border-span"></span>
            <span class="top-right border-span"></span>
            <span class="bottom-left border-span"></span>
            <span class="bottom-right border-span"></span>
        </div>
   

    </div>

    <div class="main-middle">
       

        <div class="border-container">
 
            <div id="main" style="width:60.4583rem;padding: 1.0417rem;">
              <div id="select">
              <div> <el-button @click="wendu()" type="warning" round>温度</el-button>
               <el-button @click="shidu()" type="warning" round>湿度</el-button>
               <el-button @click="jiangshui()" type="warning" round>降水量</el-button>
               <el-button @click="feng()" type="warning" round>风速</el-button>
              </div>
               <div style="color: azure;">
                年份：
                <el-select
                    v-model="date"
                    placeholder="Select"
                    size="large"
                    style="width: 240px"
                  >
                    <el-option
                      v-for="item in options"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    />
                  </el-select>
               </div>
              </div>
              <Echarts v-if="tem" :dataSource="tem" :canvasWidth="TemWidth" :canvasHeight="TemHeight"></Echarts>
            </div>
           
            <span class="top-left border-span"></span>
            <span class="top-right border-span"></span>
            <span class="bottom-left border-span"></span>
            <span class="bottom-right border-span"></span>
        </div>
    </div>
 </div>
 </div>
  
</template>

<style scoped>

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

li {
    list-style: none;
}
.con{
  display: flex;
  flex-direction: column;
}
.header{
 height: 6.25rem;
 position: relative;
 padding-top: 13px;
 font-size: 36px;
 color: #ffffff;
 text-align: center;
 background: url(../assets/bg.png) top center no-repeat;
}
#pc{
  position: absolute;
  right: 50px;
  bottom: 0px;
  padding: 10px;
}
#box{
  flex: 1;
  display: flex;
  flex-direction: row
}
.border-container {
 position: relative;
 margin-top: 15px;
 padding: 10px;

 border: 1px solid rgba(255,255,255,.15);
box-shadow: inset 0 0 50px rgba(255,255,255,.1),0 0 5px rgba(0,0,0,.3)
}
.border-container span.top-left {
 top: -2px;
 left:-2px;
 border-top: 2px solid #54dcf2;
 border-left: 2px solid #54dcf2;
}

.border-container span.top-right {
 top:-2px;
 right:-2px;
 border-top: 2px solid #54dcf2;
 border-right:2px solid #54dcf2;
}

.border-container span.bottom-left {
 bottom: -2px;
 left: -2px;
 border-bottom: 2px solid #54dcf2;
 border-left: 2px solid #54dcf2;
}

.border-container span.bottom-right {
 bottom: -2px;
 right: -2px;
 border-bottom: 2px solid #54dcf2;
 border-right: 2px solid #54dcf2;
}
.main-left,
.main-right{
 float: left;
 width: 26%;
 height: 700px;
 padding: 0 10px;
}
.main-middle{
  padding: 0 10px;
  flex: 1;
  margin-right: 39px;
}
.boxsize{
  width: 15.625rem;
  height:18.8167rem;
}
.border-container span.border-span {
 display: block;
 position: absolute;
 width:20px;
 height: 20px; opacity: .5
}

.border-container span.top-left {
 top: -2px;
 left:-2px;
 border-top: 2px solid #54dcf2;
 border-left: 2px solid #54dcf2;
}

.border-container span.top-right {
 top:-2px;
 right:-2px;
 border-top: 2px solid #54dcf2;
 border-right:2px solid #54dcf2;
}

.border-container span.bottom-left {
 bottom: -2px;
 left: -2px;
 border-bottom: 2px solid #54dcf2;
 border-left: 2px solid #54dcf2;
}

.border-container span.bottom-right {
 bottom: -2px;
 right: -2px;
 border-bottom: 2px solid #54dcf2;
 border-right: 2px solid #54dcf2;
}
.name-title{
 font-size:16px; font-weight: bolder;
 color: #00ffff;
}

#select{
  width: 119%;
    height: 3.1rem;
    padding: 0px 35px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

</style>
