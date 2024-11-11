import * as echarts from 'echarts';
import http from '../api/http';


export const getPre = async(date)=>{
  if(!date){
    date = new Date().getFullYear();
   }
  let time = [],
      hums_f = [],
      hums_his_f = [];

  await http.get(`/hum/${date}`).then(res=>{
   console.log(res.data);
  if(res.data.code === 200){
    const {dates,hums_his,hums } = res.data.data;
    time = dates;
    hums_f = hums;
    hums_his_f = hums_his;
   
  }
})
return  {
  title: {
    text: '湿度'
  },
  tooltip: {
    trigger: 'axis',
   
  },
  legend: {
    data: ['当日湿度','历史每日湿度']
  },
  toolbox: {
    feature: {
      saveAsImage: {}
    }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: [
    {
      type: 'category',
      boundaryGap: false,
      axisTick: {
        show: false //不显示刻度线
      },
      data: time,
       
    }
  ],
  yAxis: [
    {
      type: 'value',
      max:'100',
      min:'0',
       axisLabel: {
        formatter: '{value} %'
      }
    }
  ],
  series: [
    {
      name: '当日湿度',
      type: 'line',
      smooth: true, //平滑曲线
              symbol: "circle", //数据点形状
              symbolSize: 5, //数据点大小
              showSymbol: false, //不显示数据点
              lineStyle: {
                  
                      color: "#00d887", //线条颜色
                      width: 2 //线条宽度
                  
              },
              areaStyle: {
                 
                      color: new echarts.graphic.LinearGradient(
                          0, 0, 0, 1, [{
                                  offset: 0,
                                  color: "rgba(0, 216, 135, 0.4)" //渐变色
                              },
                              {
                                  offset: 0.8,
                                  color: "rgba(0, 216, 135, 0.1)" //渐变色
                              }
                          ],
                          false
                      ),
                      shadowColor: "rgba(0, 0, 0, 0.1)" //阴影颜色
                  
              },
              itemStyle: {
                  
                      color: "#00d887", //数据点颜色
                      borderColor: "rgba(68, 29, 22, .1)", //边框颜色
                      borderWidth: 12 //边框宽度
                  
              },
        emphasis: {
          focus: 'series'
        },
      data:hums_f,
      tooltip: {
        valueFormatter: function (value) {
          return value + ' %';
        }
      },
    },
    {
      name: '历史每日湿度',
      type: 'line',
      data:hums_his_f,
     lineStyle: {
                        type: 'dashed', // 设置为虚线
                        color: '#00000', // 线条颜色
                        width: 2 // 线条宽度
                    },
    }
   
  ]
};
}