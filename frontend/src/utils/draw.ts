import * as echarts from "echarts";

export function drawRadar(node: any, data: Array<number>, aveData: Array<number>) {
    data = data.map(i => i + 9)
    aveData = aveData.map(i => i + 9)
    const myChart = echarts.init(node);
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
        toolbox: {
            feature: {
                saveAsImage: {
                    name: '域名饼状图',
                    show: true,
                    excludeComponents: ['toolbox'],
                    pixelRatio: 2
                }

            }
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
    window.onresize = () => {
        myChart.resize();
    };
    myChart.setOption(option);
}

export function drawBar(node: any, data: number[], IPData: number[], CNAMEData: number[], serverData: number[], NSData: number[], rootData: number[], DNSData: number[]): void {
    data = [1, 2, 4, 5, 6, 4, 5, 8, 7, 6, 2, 1, 4, 5, 8, 7, 9, 6]
    IPData = [1, 5, 4, 8, 7, 5, 2, 1, 5, 6, 5, 4, 8, 9, 7, 5, 6, 2]
    CNAMEData = [5, 4, 8, 6, 2, 1, 5, 6, 9, 8, 7, 5, 6, 3, 2, 1, 5, 9]
    serverData = [4, 5, 8, 5, 9, 1, 2, 5, 8, 6, 3, 2, 1, 8, 5, 0, 2, 5]
    NSData = [4, 5, 6, 9, 8, 7, 5, 2, 4, 5, 6, 9, 8, 4, 5, 6, 2, 1]
    rootData = [4, 5, 2, 8, 6, 5, 2, 1, 2, 0, 1, 5, 6, 9, 0, 2, 5, 6]
    DNSData = [4, 5, 8, 9, 7, 8, 6, 5, 8, 9, 8, 9, 8, 2, 6, 8, 9, 8]

    const myChart = echarts.init(node)
    const emphasisStyle = {
        itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0,0,0,0.3)'
        }
    };
    const option = {
        legend: {
            data: ['综合得分', 'IP得分', 'CNAME得分', '服务商得分', 'NS服务商得分', '顶级域得分', 'DNS服务商得分'],
            left: '10%',
            selectedMode: 'single' // 设置单选多选模式
        },
        brush: {
            toolbox: ['rect', 'polygon', 'lineX', 'lineY', 'keep', 'clear'],
            xAxisIndex: 0
        },
        toolbox: {
            feature: {
                magicType: {
                    type: ['stack']
                },
                dataView: {},
                saveAsImage: {
                    name: '域名条形图',
                    show: true,
                    excludeComponents: ['toolbox'],
                    pixelRatio: 2
                }

            }
        },
        tooltip: {},
        xAxis: {
            data: ['[-9,-8)', '[-8,-7)', '[-7,-6)', '[-6,-5)', '[-5,-4)', '[-4,-3)', '[-3,-2)', '[-2,-1)',
                '[-1,0)', '[0,1)', '[1,2)', '[2,3)', '[3,4)', '[4,5)', '[5,6)', '[6,7)', '[7,8)', '[8,9]'],
            name: '得分区间',
            axisLine: { onZero: true },
            splitLine: { show: false },
            splitArea: { show: false }
        },
        yAxis: {
            name: '数量',
        },
        grid: {
            bottom: 100
        },
        series: [
            {
                name: '综合得分',
                type: 'bar',
                emphasis: emphasisStyle,
                data: data
            },
            {
                name: 'IP得分',
                type: 'bar',
                emphasis: emphasisStyle,
                data: IPData
            },
            {
                name: 'CNAME得分',
                type: 'bar',
                emphasis: emphasisStyle,
                data: CNAMEData
            },
            {
                name: '服务商得分',
                type: 'bar',
                emphasis: emphasisStyle,
                data: serverData
            },
            {
                name: 'NS服务商得分',
                type: 'bar',
                emphasis: emphasisStyle,
                data: NSData
            },
            {
                name: '顶级域得分',
                type: 'bar',
                emphasis: emphasisStyle,
                data: rootData
            },
            {
                name: 'DNS服务商得分',
                type: 'bar',
                emphasis: emphasisStyle,
                data: DNSData
            },

        ]
    };
    window.onresize = () => {
        myChart.resize();
    };
    myChart.setOption(option);
}