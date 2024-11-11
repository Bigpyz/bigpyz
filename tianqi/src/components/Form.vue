<template>
  <th>
    <table>
        <tr>
            <th>每日摘要</th>
            <th>最大值</th>
            <th>平均</th>
            <th>最小值</th>
        </tr>
        <tr v-if="Data" v-for="(item,index) in tableData" :key="index">
            <td>{{ item.name }}</td>
            <td>{{ item.max }}</td>
            <td>{{ item.avg }}</td>
            <td>{{ item.min }}</td>
        </tr>
    </table>
  </th>
</template>

<script lang="js" setup>
import http from '../api/http';
import { ref,onMounted } from 'vue';
const Data = ref(null)
const tableData = ref([]);
onMounted(async () => {
  try {
        const res = await http.get('/sum');
        if (res.data.code === 200) {
          Data.value = res.data.data;
          // 假设res.data.data具有正确的结构来填充tableData
          tableData.value =  [
              {
                name:"高温（°C）",
                max:Data.value.hei_tem.max,
                avg:Data.value.hei_tem.mean,
                min:Data.value.hei_tem.min
              },
              {
                name:"低温（°C）",
                max:Data.value.low_tem.max,
                avg:Data.value.low_tem.mean,
                min:Data.value.low_tem.min
              },
              {
                name:"降水（毫米）",
                max:Data.value.preci.max,
                avg:Data.value.preci.mean,
                min:Data.value.preci.min
              },
              {
                name:"风速（公里/小时）",
                max:Data.value.wind.max,
                avg:Data.value.wind.mean,
                min:Data.value.wind.min
              }
            
            ]
        } else {
          console.error('Failed to fetch data:', res.data.message || 'Unknown error');
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    });


</script>

<style scoped>

/* 可选的：为表格添加一些基本样式 */
        table {
            width: 100%; /* 设置表格宽度为容器宽度的50% */
            border-collapse: collapse; /* 合并表格边框 */
            margin: 20px 0; /* 添加顶部和底部外边距 */
            background-color: rgba(0,0,0,0.1);
            color:#ffffff;
            margin-left: 10px;
        }
        th, td {
            /* border: 1px solid #ddd; 添加边框 */
            padding: 8px; /* 添加内边距 */
           
        }
        td{
            text-align: center;
            font-size: 15px;
        }
       
</style>