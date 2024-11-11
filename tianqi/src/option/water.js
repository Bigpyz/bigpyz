import http from '../api/http';


export const getWater = async(date)=>{
 
  if(!date){
    date = new Date().getFullYear();
   }
let time = [],
    water = [];
  await http.get(`/preci/${date}`).then(res=>{
   console.log(res.data);
  if(res.data.code === 200){
    const {dates,preci} = res.data.data;
    time = dates;
    water = preci;
   
  }
})


return {
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
      data:water
    },
   
  ]
};
}