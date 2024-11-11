import http from '../api/http';
import * as echarts from 'echarts';
export const getOption = async()=>{
  let time = [],
      hei = [],
      low = [],
      hu=[],
      pr=[];
      
        const res = await http.post('/predict');
        console.log(res.data, "ops");
        
          const { dates, hei_tem, low_tem, hum, preci } = res.data;
          time = dates;
          hei = hei_tem;
          low = low_tem;
          hu = hum;
          pr = preci;
       
      console.log(time, hei, low, hu, pr);
return [{
  title: {
  //   text: 'Stacked Area Chart'
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      label: {
        backgroundColor: '#6a7985'
      }
    }
  },
  legend: {
    data: ['每日最高气温', '每日最低气温'],
    textStyle: {
      color: ['#0d4523', '#ff0000']
}
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
     data:time,
    }
  ],
  yAxis: [
    {
      type: 'value',
      name: '温度/℃',
      
      axisLabel: {
        formatter: '{value} °C'
      }
    }
  ],
  series: [
    {
      name: '每日最高气温',
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
       data: hei,
       tooltip: {
        valueFormatter: function (value) {
          return value + ' °C';
        }
      },
    },
    
    {
      name: '每日最低气温',
      type: 'line',
      smooth: true, //平滑曲线
            symbol: "circle", //数据点形状
            symbolSize: 5, //数据点大小
            showSymbol: false, //不显示数据点
            selected: false,
            lineStyle: {
                
                    color: "#0184d5", //线条颜色
                    width: 2 //线条宽度
                
            },
            areaStyle: {
                
                    color: new echarts.graphic.LinearGradient(
                        0, 0, 0, 1, [{
                                offset: 0,
                                color: "rgba(68, 29, 22, 0.4)" //渐变色
                            },
                            {
                                offset: 0.8,
                                color: "rgba(68, 29, 22, 0.1)" //渐变色
                            }
                        ],
                        false
                    ),
                    shadowColor: "rgba(68, 29, 22, 0.1)" //阴影颜色
                
            },
            itemStyle: {
               
                    color: "#0184d5", //数据点颜色
                    borderColor: "rgba(221, 220, 107, .1)", //边框颜色
                    borderWidth: 12 //边框宽度
                
            },
      emphasis: {
        focus: 'series'
      },
      data: low,
      tooltip: {
        valueFormatter: function (value) {
          return value + ' °C';
        }
      },
    }
    
  ]
},
{
  title: {
    text: '湿度'
  },
  tooltip: {
    trigger: 'axis',
   
  },
  legend: {
    data: ['当日湿度']
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
      data:hu,
      tooltip: {
        valueFormatter: function (value) {
          return value + ' %';
        }
      },
    },
   
  ]
},
{
  tooltip: {
    trigger: 'axis',
    
  },
 
  legend: {
    data: ['当日降水量']
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
      data: time,
      axisPointer: {
        type: 'shadow'
      }
    }
  ],
  yAxis: [
    {
      type: 'value',
      name: '降水量',
     
      // interval: 50,
      axisLabel: {
        formatter: '{value} ml'
      }
    },
    
  ],
  series: [
    {
      name: '当日降水量',
      type: 'bar',
      tooltip: {
        valueFormatter: function (value) {
          return value + ' ml';
        }
      },
      data:pr
    },
   
  ]
}
]
}




