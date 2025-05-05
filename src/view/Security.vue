<template>
    <div class="analyze">
        <div class="result" v-if="securityResult">{{ securityResult }}</div>
        <div id="main"></div> <!-- 添加用于展示图表的 div -->
        <div id="rgb"></div>
    </div>
</template>

<script setup lang='ts'>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';
import axios from 'axios';

// import useEncipherStore from '../store/encipher';
// const encipherStore = useEncipherStore();
const securityResult = ref<string | null>(null);

onMounted(
    async () => {
    //     if(!encipherStore.rightImg){
    //     return
    // }
    try {
        // 从 JSON 文件读取数据
        const response = await axios.get('/output/npcr_uaci_baci_results.json');
        const data = response.data;

        // 提取数据
        const classNames = ['NPCR', 'UACI'];
        const probabilities = [data.NPCR, data.UACI];

        // 基于准备好的 DOM，初始化 echarts 实例
        const myChart = echarts.init(document.getElementById('main'));

        // 绘制柱状图
        myChart.setOption({
            title: {
                text: 'NPCR、UACI 分析结果',
                // left: 'center'
            },
            tooltip: {

            },
            xAxis: {
                // type: 'category',
                data: classNames,
                axisLabel: {
                    fontSize: 18 // 设置字体大小
                }
            },
            yAxis: {
                type: 'value',
                axisLabel: {
                    formatter: '{value} %' // 显示百分比
                }
            },
            series: [
                {
                    name: '值',
                    type: 'bar',
                    data: probabilities,
                    itemStyle: {
                        color: '#5470C6' // 设置柱状图颜色
                    }
                }
            ]
        });
    } catch (error) {
        console.error('读取数据失败:', error);
        securityResult.value = '读取数据失败，请检查文件路径或数据格式。';
    }

    try {
    console.log('开始读取数据...');
    const response = await axios.get('/output/entropy_results.json');
    const data = response.data;
    console.log('数据读取成功:', data);

    // 提取数据
    const classNames = ['Entropy_R', 'Entropy_G', 'Entropy_B'];
    const probabilities = [data.Entropy_R, data.Entropy_G, data.Entropy_B];

    // 检查 DOM 元素是否存在
    const element = document.getElementById('rgb');
    if (!element) {
        console.error('无法找到 #rgb 元素，请检查 DOM 是否正确渲染。');
        return;
    }

    // 初始化 ECharts 实例
    const myChart = echarts.init(element);

    // 绘制柱状图
    myChart.setOption({
        title: {
            text: '信息熵 分析结果',
        },
        tooltip: {
            // trigger: 'axis',
            // axisPointer: {
            //     type: 'shadow',
            // },
        },
        xAxis: {
            data: classNames,
            axisLabel: {
                fontSize: 18,
            },
        },
        yAxis: {
            type: 'value',
        },
        series: [
            {
                name: '值',
                type: 'bar',
                data: probabilities,
                itemStyle: {
                    color: (params:any) => {
                        // 根据柱状图的索引设置颜色
                        const colors = ['#FF0000', '#00FF00', '#0000FF']; // 红、绿、蓝
                        return colors[params.dataIndex];
                    },
                },
                label: {
                    show: true, // 显示数值
                    position: 'top', // 数值显示在柱状图顶部
                    fontSize: 14,
                    formatter: '{c}', // 显示数值本身
                },
            },
        ],
    });
} catch (error) {
    console.error('读取数据失败:', error);
    securityResult.value = '读取数据失败，请检查文件路径或数据格式。';
}
});
</script>

<style scoped>
.analyze {
    display: flex;
    /* flex-direction: column; */
    /* align-items: center; */
    height: 100%;
    /* 使容器占满视口高度 */
}

.result {
    font-size: 22px;
    font-weight: bold;
    /* margin: 20px 0; */
    text-align: center;
}

#main {
    margin-top: 5%;
    margin-left: 5%;
    width: 50%;
    height: 90%;
}

#rgb {
    margin-top: 5%;
    margin-left: 5%;
    width: 50%;
    height: 90%;
}
</style>