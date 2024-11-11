import * as echarts from 'echarts';
import http from '../api/http';



export const getTem= async(date)=>{
  
     if(!date){
      date = new Date().getFullYear();
     }
     let time = [],
     hei= [],
     low= [],
     hei_his= [],
     low_his= [],
     pre_hei= [],
     pre_low= [];
    await http.get(`/tem/${date}`).then(res=>{
   
      if(res.data.code === 200){
        const {dates,hei_his_temps,hei_temps,low_his_temps,low_temps,pre_hei_temps,pre_low_temps } = res.data.data;
        time = dates;
        hei = hei_temps;
        low = low_temps;
        pre_hei = pre_hei_temps;
        pre_low = pre_low_temps;
        hei_his = hei_his_temps;
        low_his = low_his_temps;
      
      }

    })
    return {
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
        data: ['每日最高气温', '每日最低气温','历史每日最高气温', '历史每日最低气温'],
        textStyle: {
          color: ['#0d4523', '#ff0000', '#0000ff', '#ffff00']
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
        },
         {
        name: '历史每日最高气温',
        type: 'line',
        data: hei_his,
         lineStyle: {
               type: 'dashed', // 设置为虚线
                color: '#ffffff', // 线条颜色
                width: 2 // 线条宽度
         },
         tooltip: {
          valueFormatter: function (value) {
            return value + ' °C';
          }
        },
      },
      {
        name: '历史每日最低气温',
        type: 'line',
        data:low_his,
       lineStyle: {
            type: 'dashed', // 设置为虚线
            color: '#ffffff', // 线条颜色
            width: 2 // 线条宽度
          },
         tooltip: {
            valueFormatter: function (value) {
             return value + ' °C';
            }
          },
      }
        
      ]
    };
}
 