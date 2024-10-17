<template>
    <div class="analyze">
        <div id="main"></div> <!-- 添加用于展示图表的 div -->
    </div>
</template>

<script setup lang='ts'>
import { onMounted } from 'vue';
import * as echarts from 'echarts';
import axios from 'axios';

onMounted(async () => {
    // 读取文件内容
    const response = await axios.get('/output/prediction_result.txt');
    const fileContent = response.data;

    // 解析文件内容
    const probabilities = parseProbabilities(fileContent);

    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('main'));
    // 绘制图表
    myChart.setOption({
        title: {
            // text: '阿兹海默病诊断'
        },
        tooltip: {},
        xAxis: {
            data: ['Mild_Demented', 'Moderate_Demented', 'Non_Demented', 'Very_Mild_Demented'],
            axisLabel: {
                fontSize: 18 // 设置字体大小
            }
        },
        yAxis: {},
        series: [
            {
                name: '概率',
                type: 'bar',
                data: probabilities
            }
        ]
    });
});

// 解析文件内容的函数
function parseProbabilities(fileContent: string) {
    const lines = fileContent.split('\n');
    const probabilities: number[] = [];
    lines.forEach(line => {
        const match = line.match(/: (\d+\.\d+)/);
        if (match) {
            probabilities.push(parseFloat(match[1]));
        }
    });
    return probabilities;
}
</script>

<style scoped>
.analyze {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    /* 使容器占满视口高度 */
}

#main {
    width: 100%;
    height: 100%;
}
</style>