<template>
    <div class="analyze">
        <div id="main"></div> <!-- 添加用于展示图表的 div -->
    </div>
</template>

<script setup lang='ts'>
import { onMounted } from 'vue';
import * as echarts from 'echarts';

onMounted(() => {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('main'));
    // 绘制图表
    myChart.setOption({
        title: {
            // text: '阿兹海默病诊断'
        },
        tooltip: {},
        xAxis: {
            data: ['Mild_Demented', 'Moderate_Demented', 'Non_Demented', 'Very_Mild_Demented']
        },
        yAxis: {},
        series: [
            {
                name: '概率',
                type: 'bar',
                data: [0.1004, 0.1100, 0.1203, 0.6999]
            }
        ]
    });
});
</script>

<style scoped>
.analyze {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    /* height: 80vh; */
    /* 使容器占满视口高度 */
}

#main {
    width: 100%;
    height: 100%;
    /* width: 900px;
    height: 700px; */

}
</style>