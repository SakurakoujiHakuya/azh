<template>
    <div class="analyze">
        <div class="result" v-if="diagnosisResult">{{ diagnosisResult }}</div>
        <div id="main"></div> <!-- 添加用于展示图表的 div -->
    </div>
</template>

<script setup lang='ts'>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';
import axios from 'axios';

const diagnosisResult = ref<string | null>(null);

onMounted(async () => {
    // 读取文件内容
    const response = await axios.get('/output/prediction_result.txt');
    const fileContent = response.data;

    // 解析文件内容
    const probabilities = parseProbabilities(fileContent);
    const classNames = ['Mild_Demented', 'Moderate_Demented', 'Non_Demented', 'Very_Mild_Demented'];

    // 找到概率最高的类
    const maxProbabilityIndex = probabilities.indexOf(Math.max(...probabilities));
    const maxProbabilityClass = classNames[maxProbabilityIndex];

    // 设置诊断结果
    diagnosisResult.value = '诊断结果为: ' + maxProbabilityClass;

    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('main'));
    // 绘制图表
    myChart.setOption({
        title: {
            text: '阿兹海默病诊断'
        },
        tooltip: {},
        xAxis: {
            data: classNames,
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
    flex-direction: column;
    align-items: center;
    height: 100%;
    /* 使容器占满视口高度 */
}

.result {
    font-size: 22px;
    font-weight: bold;
    margin: 20px 0;
    text-align: center;

}

#main {
    width: 90%;
    height: 90%;
}
</style>