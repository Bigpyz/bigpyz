import http from '../api/http';


export const getWind = async(date)=>{

  if(!date){
    date = new Date().getFullYear();
   }
  let time = [],
      wind = [];
  await http.get(`/wind/${date}`).then(res=>{
   console.log(res.data);
  if(res.data.code === 200){
    const {dates,winds} = res.data.data;
    time = dates;
    wind = winds;

  }
})


return  {
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      label: {
        backgroundColor: '#6a7985'
      }
    }
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data:time,
  },
  yAxis: {
    type: 'value',
    name: '公里/小时',
  },
  series: [
    {
      data:wind,
      type: 'line',
      smooth: true,
      symbol: "circle", //数据点形状
      symbolSize: 5, //数据点大小
      showSymbol: false, //不显示数据点
      areaStyle: {},
      tooltip: {
        valueFormatter: function (value) {
          console.log(value);
         
            return value + ' 公里/小时';
          
        }
      },
    }
  ]
};  
}