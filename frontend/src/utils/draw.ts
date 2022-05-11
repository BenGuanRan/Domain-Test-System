import * as echarts from "echarts";

export function drawRadar(id: string, data: Array<number>, aveData: Array<number>) {
    data = data.map(i => i + 9)
    aveData = aveData.map(i => i + 9)
    const myChart = echarts.init(document.getElementById(id));
    const option = {

        legend: {
            data: ['该域名各项得分', '平均得分']
        },
        radar: {
            // shape: 'circle',
            indicator: [
                { name: 'IP', max: 18 },
                { name: 'CNAME', max: 18 },
                { name: '注册商', max: 18 },
                { name: 'NS服务商', max: 18 },
                { name: '顶级域名', max: 18 },
                { name: 'DNS服务商', max: 18 }
            ]
        },
        series: [
            {
                name: 'Budget vs spending',
                type: 'radar',
                data: [
                    {
                        value: data,
                        name: '该域名各项得分'
                    },
                    {
                        value: aveData,
                        name: '平均得分'
                    }
                ]
            }
        ]
    };
    myChart.setOption(option);
}