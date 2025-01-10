

// 在独立js脚本中定义比较长的回调函数
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        // home页面
        func_home_chart_PVline: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('home_chart_PVline'));

            const option = {
                title: {
                    text: '7日活跃用户'
                },
                grid: {
                    left: '4%',
                    right: '4%',
                    bottom: '4%',
                    containLabel: true
                },
                tooltip: {
                    trigger: 'axis',
                },
                label: {
                    show: true,
                    position: 'top',
                    itemStyle: {
                        color: '#333',
                    },
                },
                color: ['#1f63fb'],
                xAxis: {
                    data: data['x'],
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        data: data['y'],
                        type: 'bar',
                        smooth: true
                    }
                ]
            };

            // 渲染
            myChart.setOption(option);
        },
        func_home_chart_UVline: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('home_chart_UVline'));

            const option = {
                title: {
                    text: '7日注册用户'
                },
                tooltip: {
                    trigger: 'axis',
                },
                grid: {
                    left: '4%',
                    right: '4%',
                    bottom: '4%',
                    containLabel: true
                },
                legend: {
                },
                label: {
                    show: true,
                    position: 'top',
                    itemStyle: {
                        color: '#333',
                    },
                },
                color: ['#1f63fb'],
                xAxis: {
                    data: data['x'],
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        data: data['y'],
                        type: 'line',
                        smooth: true
                    }
                ]
            };
            // 渲染
            myChart.setOption(option);
        },
        func_home_chart_UserGraph: function (data, chinajson) {

            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('home_chart_UserGraph'));
            echarts.registerMap("CHINA", chinajson, {});

            const option = {
                title: {
                    text: "用户数据地图分布",
                },
                tooltip: {
                    show: true,
                    textStyle: {
                        color: "#2f333c",
                        fontSize: 12,
                        fontWeight: "bold",
                    },
                    trigger: 'item',
                    showDelay: 0,
                    transitionDuration: 0.2,
                    formatter: (v) => {
                        const result = data.find((item) => item.name === v.name);
                        if (result.value) {
                            return `${result.name}数据<br>
                          用户数：${result.value}<br>`;
                        } else {
                            return `${result.name}<br>
                          暂无数据`;
                        }
                    }
                },
                // label:{
                //     show: true,
                //     color: "#2f333c",
                //     fontSize: 12,
                //     fontWeight: "bold",
                // },
                label: {
                    show: true,
                    position: 'top',
                    itemStyle: {
                        fontSize: 12,
                        color: '#2f333c',
                        fontWeight: "bold",
                    },
                },
                // visualMap: {
                //     min: 0,
                //     max: 9,
                //     left: 'left',
                //     top: 'bottom',
                //     text: ['高','低'],
                //     calculable: true,
                //     inRange: {
                //         color: ['#e0ffff', '#006edd']
                //     }
                // },
                toolbox: {
                    show: true,
                    //orient: 'vertical',
                    left: 'right',
                    top: 'top',
                    feature: {
                        dataView: { readOnly: false },
                        restore: {},
                        saveAsImage: {}
                    }
                },
                series: [
                    {
                        name: "省份数据",
                        id: "numbers",
                        type: "map",
                        roam: false,
                        map: "CHINA",
                        animationDurationUpdate: 1000,
                        universalTransition: true,
                        zoom: 1.6,
                        top: 150,
                        itemStyle: {
                            borderColor: "rgba(0, 124, 225, 0.4)",
                            areaColor: "rgba(0, 124, 210, 0.2)",
                            borderWidth: 1,
                        },
                        emphasis: { // 设置鼠标 hover 时的样式
                            itemStyle: {
                                borderColor: "rgba(0, 124, 225, 0.8)", // 边框颜色
                                areaColor: "rgba(0, 124, 210, 0.6)", // 区域颜色
                                borderWidth: 1, // 边框宽度
                            },
                        },
                        data: data
                    }
                ]
            };
            myChart.setOption(option);
        },
        func_home_chart_Genderpie: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('home_chart_Genderpie'));

            const option = {
                title: {
                    text: "用户性别分布",
                },
                color: ['#1565ff', '#fd8a25'],
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    top: '5%',
                    left: 'center'
                },
                label: {
                    show: false,
                    position: 'center',
                    formatter: '{b}: {d}%'
                },
                series: [
                    {
                        name: '用户性别分布',
                        type: 'pie',
                        radius: ['30%', '50%'],
                        data: data
                    }
                ]
            };
            // 渲染
            myChart.setOption(option);
        },
        func_home_chart_Sourcepie: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('home_chart_Sourcepie'));

            const option = {
                title: {
                    text: "用户来源分布",
                },
                color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                    '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    top: '10%',
                    left: 'center'
                },
                grid: {
                    top: '32%',
                    left: '32%',
                    right: '32%',
                    bottom: '32%',
                },
                label: {
                    show: false,
                    position: 'center',
                    formatter: '{b}: {d}%'
                },
                series: [
                    {
                        name: '来源',
                        type: 'pie',
                        radius: ['30%', '50%'],
                        center: ['50%', '60%'],
                        // adjust the start and end angle
                        data: data
                    }
                ]
            };
            // 渲染
            myChart.setOption(option);
        },



        // userData 页面
        func_userData_chart_Genderpie: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('userData_chart_Genderpie'));

            const option = {
                title: {
                    text: "用户性别分布",
                },
                color: ['#1565ff', '#fd8a25'],
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    top: '5%',
                    left: 'center'
                },
                label: {
                    show: false,
                    position: 'center',
                    formatter: '{b}: {d}%'
                },
                series: [
                    {
                        name: '用户性别分布',
                        type: 'pie',
                        radius: ['30%', '50%'],
                        data: data
                    }
                ]
            };
            // 渲染
            myChart.setOption(option);
        },
        func_userData_chart_Sourcepie: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('userData_chart_Sourcepie'));

            const option = {
                title: {
                    text: "用户来源分布",
                },
                color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                    '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    top: '10%',
                    left: 'center'
                },
                grid: {
                    top: '32%',
                    left: '32%',
                    right: '32%',
                    bottom: '32%',
                },
                label: {
                    show: false,
                    position: 'center',
                    formatter: '{b}: {d}%'
                },
                series: [
                    {
                        name: '来源',
                        type: 'pie',
                        radius: ['30%', '50%'],
                        center: ['50%', '60%'],
                        // adjust the start and end angle
                        data: data
                    }
                ]
            };
            // 渲染
            myChart.setOption(option);
        },
        func_userData_chart_Agecutline: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('userData_chart_Agecutline'));

            const option = {
                title: {
                    text: '各年龄段用户'
                },
                grid: {
                    left: '4%',
                    right: '4%',
                    bottom: '4%',
                    containLabel: true
                },
                tooltip: {
                    trigger: 'axis',
                },
                label: {
                    show: true,
                    position: 'top',
                    itemStyle: {
                        color: '#333',
                    },
                },
                color: ['#1f63fb'],
                xAxis: {
                    data: data['x'],
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        data: data['y'],
                        type: 'bar',
                        smooth: true
                    }
                ]
            };

            // 渲染
            myChart.setOption(option);
        },
        func_userData_chart_Vipline: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('userData_chart_Vipline'));

            const option = {
                title: {
                    text: 'VIP等级用户'
                },
                tooltip: {
                    trigger: 'axis',
                },
                grid: {
                    left: '4%',
                    right: '4%',
                    bottom: '4%',
                    containLabel: true
                },
                legend: {
                },
                label: {
                    show: true,
                    position: 'top',
                    itemStyle: {
                        color: '#333',
                    },
                },
                color: ['#1f63fb'],
                xAxis: {
                    data: data['x'],
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        data: data['y'],
                        type: 'bar',
                        smooth: true
                    }
                ]
            };
            // 渲染
            myChart.setOption(option);
        },
        func_userData_chart_Careerpie: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('userData_chart_Careerpie'));

            const option = {
                title: {
                    text: "用户职业分布",
                },
                color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                    '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    top: '10%',
                    left: 'center'
                },
                grid: {
                    top: '32%',
                    left: '32%',
                    right: '32%',
                    bottom: '32%',
                },
                label: {
                    show: false,
                    position: 'center',
                    formatter: '{b}: {d}%'
                },
                series: [
                    {
                        name: '职业',
                        type: 'pie',
                        radius: ['30%', '50%'],
                        center: ['50%', '60%'],
                        // adjust the start and end angle
                        data: data
                    }
                ]
            };
            // 渲染
            myChart.setOption(option);
        },
        func_userData_chart_OSpie: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('userData_chart_OSpie'));

            const option = {
                title: {
                    text: "登陆系统分布",
                },
                color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                    '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    top: '10%',
                    left: 'center'
                },
                grid: {
                    top: '32%',
                    left: '32%',
                    right: '32%',
                    bottom: '32%',
                },
                label: {
                    show: false,
                    position: 'center',
                    formatter: '{b}: {d}%'
                },
                series: [
                    {
                        name: '登陆系统',
                        type: 'pie',
                        radius: ['30%', '50%'],
                        center: ['50%', '60%'],
                        // adjust the start and end angle
                        data: data
                    }
                ]
            };
            // 渲染
            myChart.setOption(option);
        },
        func_userData_chart_Activityline: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('userData_chart_Activityline'));

            const option = {
                title: {
                    text: '活跃度走势(万)'
                },
                grid: {
                    left: '4%',
                    right: '4%',
                    bottom: '4%',
                    containLabel: true
                },
                tooltip: {
                    trigger: 'axis',
                },
                color: ['#fd8a25', '#2fccba',],
                xAxis: {
                    data: data['x'],
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        data: data['y'],
                        type: 'line',
                        smooth: true,
                    },
                    {
                        data: data['y'],
                        type: 'bar',
                        label: {
                            show: true,
                            position: 'top',
                            formatter: '{c}万'
                        }
                    }
                ]
            };

            // 渲染
            myChart.setOption(option);
        },
        func_userData_chart_UserGraph: function (data, chinajson) {

            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('userData_chart_UserGraph'));
            echarts.registerMap("CHINA", chinajson, {});

            const option = {
                title: {
                    text: "用户数据地图分布",
                },
                tooltip: {
                    show: true,
                    textStyle: {
                        color: "#2f333c",
                        fontSize: 12,
                        fontWeight: "bold",
                    },
                    trigger: 'item',
                    showDelay: 0,
                    transitionDuration: 0.2,
                    formatter: (v) => {
                        const result = data.find((item) => item.name === v.name);
                        if (result.value) {
                            return `${result.name}数据<br>
                          用户数：${result.value}<br>`;
                        } else {
                            return `${result.name}<br>
                          暂无数据`;
                        }
                    }
                },
                // label:{
                //     show: true,
                //     color: "#2f333c",
                //     fontSize: 12,
                //     fontWeight: "bold",
                // },
                // label: {
                //     show: true,
                //     position: 'top',
                //     // itemStyle: {
                //     //     fontSize: 12,
                //     //     color: '#2f333c',
                //     //     fontWeight: "bold",
                //     // },
                // },
                // visualMap: {
                //     min: 0,
                //     max: 9,
                //     left: 'left',
                //     top: 'bottom',
                //     text: ['高','低'],
                //     calculable: true,
                //     inRange: {
                //         color: ['#e0ffff', '#006edd']
                //     }
                // },
                toolbox: {
                    show: true,
                    //orient: 'vertical',
                    left: 'right',
                    top: 'top',
                    feature: {
                        dataView: { readOnly: false },
                        restore: {},
                        saveAsImage: {}
                    }
                },
                series: [
                    {
                        name: "省份数据",
                        id: "numbers",
                        type: "map",
                        roam: false,
                        map: "CHINA",
                        animationDurationUpdate: 1000,
                        universalTransition: true,
                        zoom: 1.6,
                        top: 150,
                        label: {
                            show: true,
                            fontSize: 10,
                            color: "#000",
                            formatter: function (params) {
                                return params.name;
                            },
                        },
                        itemStyle: {
                            borderColor: "rgba(0, 124, 225, 0.4)",
                            areaColor: "rgba(0, 124, 210, 0.2)",
                            borderWidth: 1,
                        },
                        emphasis: { // 设置鼠标 hover 时的样式
                            itemStyle: {
                                borderColor: "rgba(0, 124, 225, 0.8)", // 边框颜色
                                areaColor: "rgba(0, 124, 210, 0.6)", // 区域颜色
                                borderWidth: 1, // 边框宽度
                            },
                        },
                        select: {
                            itemStyle: {
                                areaColor: 'rgba(0, 124, 210, 0.6)',
                            },
                        },
                        data: data
                    }
                ]
            };
            myChart.setOption(option);
        },




        // tagAnalysis 页面
        func_tagAnalysis_chart_Taggrouppie: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('tagAnalysis_chart_Taggrouppie'));

            const option = {
                title: {
                    text: "标签群组分布",
                },
                color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                    '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    top: '10%',
                    left: 'center'
                },
                grid: {
                    top: '32%',
                    left: '32%',
                    right: '32%',
                    bottom: '32%',
                },
                label: {
                    show: false,
                    position: 'center',
                    formatter: '{b}: {d}%'
                },
                series: [
                    {
                        name: '标签群组分布',
                        type: 'pie',
                        radius: ['30%', '50%'],
                        data: data
                    }
                ]
            };
            // 渲染
            myChart.setOption(option);
        },
        func_tagAnalysis_chart_Importanttagcoverbar: function (data, years, datatypenum) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('tagAnalysis_chart_Importanttagcoverbar'));


            function torun(years, data) {
                let option={};

                const updateFrequency = 2000;
                const dimension = 0;
                // const tagColors = {
                //     day_active: '#00008b',
                //     last24hour_active: '#f00'
                // };
                let startIndex = 1;
                let startYear = years[startIndex];
                option = {
                    color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                        '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                    title: {
                        text: "重点标签覆盖用户迁移",
                    },
                    grid: {
                        top: '16%',
                        bottom: '16%',
                        left: '26%',
                        right: '10%'
                    },
                    // toolbox: {
                    //     show: true,
                    //     feature: {
                    //         restore: {}
                    //     }
                    // },
                    xAxis: {
                        max: 'dataMax',
                        axisLabel: {
                            formatter: function (n) {
                                return Math.round(n) + '';
                            }
                        }
                    },
                    dataset: {
                        source: data.slice(1).filter(function (d) {
                            return d[2] === startYear;
                        })
                    },
                    yAxis: {
                        type: 'category',
                        inverse: true,
                        max: datatypenum,
                        axisLabel: {
                            show: true,
                            fontSize: 14,
                            formatter: function (value) {
                                return value;
                            },
                            rich: {
                                flag: {
                                    fontSize: 25,
                                    padding: 5
                                }
                            }
                        },
                        animationDuration: 300,
                        animationDurationUpdate: 300
                    },
                    series: [
                        {
                            realtimeSort: true,
                            seriesLayoutBy: 'column',
                            type: 'bar',
                            encode: {
                                x: dimension,
                                y: 3
                            },
                            label: {
                                show: true,
                                precision: 1,
                                position: 'right',
                                valueAnimation: true,
                                fontFamily: 'monospace'
                            }
                        }
                    ],
                    // Disable init animation.
                    animationDuration: 0,
                    animationDurationUpdate: updateFrequency,
                    animationEasing: 'linear',
                    animationEasingUpdate: 'linear',
                    graphic: {
                        elements: [
                            {
                                type: 'text',
                                right: 160,
                                bottom: 60,
                                style: {
                                    text: startYear,
                                    font: 'bolder 40px monospace',
                                    fill: 'rgba(100, 100, 100, 0.25)'
                                },
                                z: 100
                            }
                        ]
                    }
                };

                myChart.setOption(option);
                for (let i = startIndex; i < years.length - 1; ++i) {
                    (function (i) {
                        setTimeout(function () {
                            updateYear(years[i + 1]);
                        }, (i - startIndex) * updateFrequency);
                    })(i);
                }
                function updateYear(year) {
                    let source = data.slice(1).filter(function (d) {
                        return d[2] === year;
                    });
                    option.series[0].data = source;
                    option.graphic.elements[0].style.text = year;
                    myChart.setOption(option);
                }
            }

            torun(years, data);

        },


        // eventAnalysis 页面
        func_eventAnalysis_chart_eventbarline: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('eventAnalysis_chart_eventbarline'));

            const option = {
                title: {
                    text: '图表展示'
                },
                toolbox: {
                    right: 20,
                    show: true,
                    feature: {
                        magicType: { type: ['line', 'bar'] },
                    }
                },
                grid: {
                    left: '4%',
                    right: '4%',
                    bottom: '4%',
                    containLabel: true
                },
                tooltip: {
                    trigger: 'axis',
                },
                label: {
                    show: true,
                    position: 'top',
                    itemStyle: {
                        color: '#333',
                    },
                },
                color: ['#1f63fb'],
                xAxis: {
                    data: data?data['x']:[],
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        data: data?data['y']:[],
                        type: 'bar',
                        smooth: true
                    }
                ]
            };

            // 渲染
            myChart.setOption(option);
        },
        func_eventAnalysis_chart_eventGrouppie: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('eventAnalysis_chart_eventGrouppie'));

            const option = {
                title: {
                    text: "标签群组分布",
                },
                color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                    '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    top: '10%',
                    left: 'center'
                },
                grid: {
                    top: '32%',
                    left: '32%',
                    right: '32%',
                    bottom: '32%',
                },
                label: {
                    show: false,
                    position: 'center',
                    formatter: '{b}: {d}%'
                },
                series: [
                    {
                        name: '标签群组分布',
                        type: 'pie',
                        radius: ['30%', '50%'],
                        data: data
                    }
                ]
            };
            // 渲染
            myChart.setOption(option);
        },
        func_eventAnalysis_chart_Importanteventcoverbar: function (data, years, datatypenum) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('eventAnalysis_chart_Importanteventcoverbar'));


            function torun(years, data) {
                let option={};

                const updateFrequency = 2000;
                const dimension = 0;
                // const tagColors = {
                //     day_active: '#00008b',
                //     last24hour_active: '#f00'
                // };
                let startIndex = 1;
                let startYear = years[startIndex];
                option = {
                    color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                        '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                    title: {
                        text: "重点标签覆盖用户迁移",
                    },
                    grid: {
                        top: '16%',
                        bottom: '16%',
                        left: '26%',
                        right: '10%'
                    },
                    // toolbox: {
                    //     show: true,
                    //     feature: {
                    //         restore: {}
                    //     }
                    // },
                    xAxis: {
                        max: 'dataMax',
                        axisLabel: {
                            formatter: function (n) {
                                return Math.round(n) + '';
                            }
                        }
                    },
                    dataset: {
                        source: data.slice(1).filter(function (d) {
                            return d[2] === startYear;
                        })
                    },
                    yAxis: {
                        type: 'category',
                        inverse: true,
                        max: datatypenum,
                        axisLabel: {
                            show: true,
                            fontSize: 14,
                            formatter: function (value) {
                                return value;
                            },
                            rich: {
                                flag: {
                                    fontSize: 25,
                                    padding: 5
                                }
                            }
                        },
                        animationDuration: 300,
                        animationDurationUpdate: 300
                    },
                    series: [
                        {
                            realtimeSort: true,
                            seriesLayoutBy: 'column',
                            type: 'bar',
                            encode: {
                                x: dimension,
                                y: 3
                            },
                            label: {
                                show: true,
                                precision: 1,
                                position: 'right',
                                valueAnimation: true,
                                fontFamily: 'monospace'
                            }
                        }
                    ],
                    // Disable init animation.
                    animationDuration: 0,
                    animationDurationUpdate: updateFrequency,
                    animationEasing: 'linear',
                    animationEasingUpdate: 'linear',
                    graphic: {
                        elements: [
                            {
                                type: 'text',
                                right: 160,
                                bottom: 60,
                                style: {
                                    text: startYear,
                                    font: 'bolder 40px monospace',
                                    fill: 'rgba(100, 100, 100, 0.25)'
                                },
                                z: 100
                            }
                        ]
                    }
                };

                myChart.setOption(option);
                for (let i = startIndex; i < years.length - 1; ++i) {
                    (function (i) {
                        setTimeout(function () {
                            updateYear(years[i + 1]);
                        }, (i - startIndex) * updateFrequency);
                    })(i);
                }
                function updateYear(year) {
                    let source = data.slice(1).filter(function (d) {
                        return d[2] === year;
                    });
                    option.series[0].data = source;
                    option.graphic.elements[0].style.text = year;
                    myChart.setOption(option);
                }
            }

            torun(years, data);

        },

        // funnelAnalysis 页面
        func_funnelAnalysis_chart_funnel: function (columns, data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('funnelAnalysis_chart_funnel'));

            const option = {
                title: {
                  text: '漏斗展示'
                },
                color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                    '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'], // 颜色 
                grid: {
                    top: '10%',
                    left: '40%',
                    right: '40%',
                    bottom: '10%'
                },
                tooltip: {
                  trigger: 'item',
                  formatter: '{a} <br/>{b} : {c}%'
                },
                legend: {
                  data: columns?columns:[]
                },
                series: [
                  {
                    name: 'Expected',
                    type: 'funnel',
                    left: '10%',
                    width: '80%',
                    label: {
                      formatter: '{b}'
                    },
                    labelLine: {
                      show: false
                    },
                    itemStyle: {
                      opacity: 0.7
                    },
                    emphasis: {
                      label: {
                        position: 'inside',
                        formatter: '{c}'
                      }
                    },
                    data: data
                },
                  {
                    name: 'Actual',
                    type: 'funnel',
                    left: '10%',
                    width: '80%',
                    maxSize: '80%',
                    label: {
                      position: 'inside',
                      formatter: '{c}',
                      color: '#fff'
                    },
                    itemStyle: {
                      opacity: 0.5,
                      borderColor: '#fff',
                      borderWidth: 2
                    },
                    emphasis: {
                      label: {
                        position: 'inside',
                        formatter: '{c}'
                      }
                    },
                    data: data,
                    // Ensure outer shape will not be over inner shape when hover.
                    z: 100
                  }
                ]
              };

            // 渲染
            myChart.setOption(option);
        },


        // retentionAnalysis 页面
        func_retentionAnalysis_chart_funnel: function (columns, data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('retentionAnalysis_chart_funnel'));

            const option = {
                title: {
                  text: '漏斗展示'
                },
                color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                    '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'], // 颜色 
                grid: {
                    top: '10%',
                    left: '40%',
                    right: '40%',
                    bottom: '10%'
                },
                tooltip: {
                  trigger: 'item',
                  formatter: '{a} <br/>{b} : {c}%'
                },
                legend: {
                  data: columns?columns:[]
                },
                series: [
                  {
                    name: 'Expected',
                    type: 'funnel',
                    left: '10%',
                    width: '80%',
                    label: {
                      formatter: '{b}'
                    },
                    labelLine: {
                      show: false
                    },
                    itemStyle: {
                      opacity: 0.7
                    },
                    emphasis: {
                      label: {
                        position: 'inside',
                        formatter: '{c}'
                      }
                    },
                    data: data
                },
                  {
                    name: 'Actual',
                    type: 'funnel',
                    left: '10%',
                    width: '80%',
                    maxSize: '80%',
                    label: {
                      position: 'inside',
                      formatter: '{c}',
                      color: '#fff'
                    },
                    itemStyle: {
                      opacity: 0.5,
                      borderColor: '#fff',
                      borderWidth: 2
                    },
                    emphasis: {
                      label: {
                        position: 'inside',
                        formatter: '{c}'
                      }
                    },
                    data: data,
                    // Ensure outer shape will not be over inner shape when hover.
                    z: 100
                  }
                ]
              };

            // 渲染
            myChart.setOption(option);
        },

        // sessionAnalysis_chart_barline
        func_sessionAnalysis_chart_barline: function (res) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('sessionAnalysis_chart_barline'));

            const option = {
                title: {
                    text: '图表展示'
                },
                color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                    '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                toolbox: {
                    right: 20,
                    show: true,
                    feature: {
                        magicType: { type: ['line', 'bar'] },
                    }
                },
                grid: {
                    left: '4%',
                    right: '4%',
                    bottom: '4%',
                    containLabel: true
                },
                tooltip: {
                    trigger: 'axis',
                },
                label: {
                    show: true,
                    position: 'top',
                    itemStyle: {
                        color: '#333',
                    },
                },
                xAxis: {
                    data: res && res["xData"] ? res["xData"] : []
                },
                yAxis: {
                    type: 'value'
                },
                series: res && res["seriesData"] ? res["seriesData"] : []
            };

            // 渲染
            myChart.setOption(option);
        },


        // userpathAnalysis_chart_sankey
        func_userpathAnalysis_chart_sankey: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('userpathAnalysis_chart_sankey'));

            const option = {
                title: {
                  text: '图表展示'
                },
                tooltip: {
                  trigger: 'item',
                  triggerOn: 'mousemove'
                },
                series: [
                  {
                    type: 'sankey',
                    data: data && data.nodes?data.nodes:[],
                    links: data && data.links?data.links:[],
                    lineStyle: {
                      curveness: 0.5
                    }
                  }
                ]
              }

            // 渲染
            myChart.setOption(option);
        },


        // customAnalysis_chart_chart
        func_customAnalysis_chart_chart: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('customAnalysis_chart_chart'));

            const option = {
                title: {
                    text: '图表展示'
                },
                color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                    '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                toolbox: {
                    right: 20,
                    show: true,
                    feature: {
                        magicType: { type: ['line', 'bar'] },
                    }
                },
                grid: {
                    left: '4%',
                    right: '4%',
                    bottom: '4%',
                    containLabel: true
                },
                tooltip: {
                    trigger: 'axis',
                },
                label: {
                    show: true,
                    position: 'top',
                    itemStyle: {
                        color: '#333',
                    },
                },
                xAxis: {
                    data: data && data.x ? data.x : []
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        data: data && data.y ? data.y : [],
                        type: 'line',
                        smooth: true,
                    },
                ]
            };

            // 渲染
            myChart.setOption(option);
        },


        // userPortraitAnalysis_chart_age
        func_userPortraitAnalysis_chart_age: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('userPortraitAnalysis_chart_age'));
        
            // 检查数据是否存在
            if (data && data.x && data.y) {

            const option = {
                title: {
                    text: '用户年龄分布'
                },
                color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                    '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                grid: {
                    left: '4%',
                    right: '4%',
                    bottom: '4%',
                    containLabel: true
                },
                tooltip: {
                    trigger: 'axis',
                },
                label: {
                    show: true,
                    position: 'top',
                    itemStyle: {
                        color: '#333',
                    },
                },
                xAxis: {
                    data: data && data.x ? data.x : []
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        data: data && data.y ? data.y : [],
                        type: 'bar',
                        smooth: true,
                    },
                ]
            };
            myChart.setOption(option);
        } 
            else {
                // 如果没有数据，可以设置一个空的配置或者不显示图表
                myChart.setOption({}); 
            }
        },

        // userPortraitAnalysis_chart_sex
        func_userPortraitAnalysis_chart_sex: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('userPortraitAnalysis_chart_sex'));

            const option = {
                title: {
                    text: "用户性别分布",
                },
                color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                    '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    top: '5%',
                    left: 'center'
                },
                grid: {
                    top: '32%',
                    left: '32%',
                    right: '32%',
                    bottom: '32%',
                },
                label: {
                    show: false,
                    position: 'center',
                    formatter: '{b}: {d}%'
                },
                series: [
                    {
                        name: '用户性别分布',
                        type: 'pie',
                        radius: ['30%', '50%'],
                        data: data?data:[]
                    }
                ]
            };

            if (data) {
                myChart.setOption(option);
              } else {
                myChart.setOption({});
              }
        },

        // userPortraitAnalysis_chart_os
        func_userPortraitAnalysis_chart_os: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('userPortraitAnalysis_chart_os'));

            const option = {
                title: {
                    text: "用户系统分布",
                },
                color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                    '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    top: '14%',
                    left: 'center'
                },
                label: {
                    show: false,
                    position: 'center',
                    formatter: '{b}: {d}%'
                },
                series: [
                    {
                        name: '用户性别分布',
                        type: 'pie',
                        radius: ['30%', '50%'],
                        center:["50%", "56%"],
                        data: data?data:[]
                    }
                ]
            };

            if (data) {
                myChart.setOption(option);
              } else {
                myChart.setOption({});
              }
        },

        // userPortraitAnalysis_chart_loc
        func_userPortraitAnalysis_chart_loc(data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('userPortraitAnalysis_chart_loc'));
        
            // 检查数据是否存在
            if (data && data.x && data.y) {
                const option = {
                    title: {
                        text: '用户地域分布'
                    },
                    color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                        '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                    grid: {
                        left: '4%',
                        right: '4%',
                        bottom: '4%',
                        containLabel: true
                    },
                    tooltip: {
                        trigger: 'axis',
                    },
                    label: {
                        show: true,
                        position: 'top',
                        itemStyle: {
                            color: '#333',
                        },
                    },
                    xAxis: {
                        data: data.x
                    },
                    yAxis: {
                        type: 'value'
                    },
                    series: [
                        {
                            data: data.y,
                            type: 'bar',
                            smooth: true,
                        },
                    ]
                };
        
                myChart.setOption(option);
            } else {
                // 如果没有数据，可以设置一个空的配置或者不显示图表
                myChart.setOption({}); // 这将清空图表
                // 或者可以显示一个提示信息
                // myChart.showLoading({
                //     text: '没有数据',
                //     color: '#000',
                //     textColor: '#fff',
                //     maskColor: 'rgba(255, 255, 255, 0.5)',
                //     textStyle: {
                //         fontSize: 20,
                //         fontWeight: 'bold'
                //     }
                // });
            }
        },

        // userPortraitAnalysis_chart_apprun
        func_userPortraitAnalysis_chart_apprun(data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('userPortraitAnalysis_chart_apprun'));
        
            // 检查数据是否存在
            if (data && data.x && data.y) {
                const option = {
                    title: {
                        text: '用户启动app'
                    },
                    color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                        '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                    grid: {
                        left: '4%',
                        right: '4%',
                        bottom: '4%',
                        containLabel: true
                    },
                    tooltip: {
                        trigger: 'axis',
                    },
                    label: {
                        show: true,
                        position: 'top',
                        itemStyle: {
                            color: '#333',
                        },
                    },
                    xAxis: {
                        data: data.x
                    },
                    yAxis: {
                        type: 'value'
                    },
                    series: [
                        {
                            data: data.y,
                            type: 'bar',
                            smooth: true,
                        },
                    ]
                };
        
                myChart.setOption(option);
            } else {
                myChart.setOption({});
            }
        },

        // userPortraitAnalysis_chart_pay
        func_userPortraitAnalysis_chart_pay(data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('userPortraitAnalysis_chart_pay'));
        
            // 检查数据是否存在
            if (data && data.x && data.y) {
                const option = {
                    title: {
                        text: '用户支付订单'
                    },
                    color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                        '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                    grid: {
                        left: '4%',
                        right: '4%',
                        bottom: '4%',
                        containLabel: true
                    },
                    tooltip: {
                        trigger: 'axis',
                    },
                    label: {
                        show: true,
                        position: 'top',
                        itemStyle: {
                            color: '#333',
                        },
                    },
                    xAxis: {
                        data: data.x
                    },
                    yAxis: {
                        type: 'value'
                    },
                    series: [
                        {
                            data: data.y,
                            type: 'bar',
                            smooth: true,
                        },
                    ]
                };
        
                myChart.setOption(option);
            } else {
                myChart.setOption({});
            }
        },






        // dynamicsalesAnalysis_chart_cancelorder
        func_dynamicsalesAnalysis_chart_cancelorder(data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('dynamicsalesAnalysis_chart_cancelorder'));
        
            // 检查数据是否存在
            if (data && data.x && data.y) {
                const option = {
                    title: {
                        text: '订单取消'
                    },
                    color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                        '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                    grid: {
                        left: '8%',
                        right: '8%',
                        bottom: '4%',
                        containLabel: true
                    },
                    tooltip: {
                        trigger: 'axis',
                    },
                    label: {
                        show: true,
                        position: 'top',
                        itemStyle: {
                            color: '#333',
                        },
                    },
                    xAxis: {
                        data: data.x
                    },
                    yAxis: {
                        type: 'value'
                    },
                    series: [
                        {
                            data: data.y,
                            type: 'bar',
                            smooth: true,
                        },
                    ]
                };
        
                myChart.setOption(option);
            } else {
                myChart.setOption({});
            }
        },

        // dynamicsalesAnalysis_chart_gmv30
        func_dynamicsalesAnalysis_chart_gmv30(data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('dynamicsalesAnalysis_chart_gmv30'));
        
            // 检查数据是否存在
            if (data && data.x && data.y) {
                const option = {
                    title: {
                        text: '订单取消'
                    },
                    color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                        '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                    grid: {
                        left: '8%',
                        right: '8%',
                        bottom: '4%',
                        containLabel: true
                    },
                    tooltip: {
                        trigger: 'axis',
                    },
                    xAxis: {
                        data: data.x
                    },
                    yAxis: {
                        type: 'value'
                    },
                    series: [
                        {
                            data: data.y,
                            type: 'bar',
                            smooth: true,
                        },
                    ]
                };
        
                myChart.setOption(option);
            } else {
                myChart.setOption({});
            }
        },

        // dynamicsalesAnalysis_chart_gmvcontribute
        func_dynamicsalesAnalysis_chart_gmvcontribute: function (data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('dynamicsalesAnalysis_chart_gmvcontribute'));

            const option = {
                title: {
                    text: "GMV各端贡献",
                },
                color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                    '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    top: '10%',
                    left: 'center'
                },
                grid: {
                    top: '32%',
                    left: '32%',
                    right: '32%',
                    bottom: '32%',
                },
                label: {
                    show: false,
                    position: 'center',
                    formatter: '{b}: {d}%'
                },
                series: [
                    {
                        name: '用户性别分布',
                        type: 'pie',
                        radius: ['30%', '50%'],
                        center:["50%", "56%"],
                        data: data?data:[]
                    }
                ]
            };

            if (data) {
                myChart.setOption(option);
              } else {
                myChart.setOption({});
              }
        },

        // dynamicsalesAnalysis_chart_salestrend
        func_dynamicsalesAnalysis_chart_salestrend(data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('dynamicsalesAnalysis_chart_salestrend'));
        
            // 检查数据是否存在
            if (data && data.x && data.y) {
                const option = {
                    title: {
                        text: '各类商品销售趋势'
                    },
                    color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                        '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                    grid: {
                        left: '8%',
                        right: '8%',
                        bottom: '4%',
                        containLabel: true
                    },
                    tooltip: {
                        trigger: 'axis',
                    },
                    xAxis: {
                        data: data.x
                    },
                    yAxis: {
                        type: 'value'
                    },
                    series: data.y
                };
        
                myChart.setOption(option);
            } else {
                myChart.setOption({});
            }
        },


        // dynamicsalesAnalysis_chart_shoprate
        func_dynamicsalesAnalysis_chart_shoprate(data) {
            // 根据id初始化绑定图表
            const myChart = echarts.init(document.getElementById('dynamicsalesAnalysis_chart_shoprate'));

            const option = {
                title: {
                    text: "商铺占比",
                },
                color: ['#1565ff', '#1ac6ff', '#ff8a01', '#3cc780',
                    '#7443d4', '#ffc400', '#304d77', '#b58deb', '#52d068'],
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    top: '10%',
                    left: 'center'
                },
                grid: {
                    top: '32%',
                    left: '32%',
                    right: '32%',
                    bottom: '32%',
                },
                label: {
                    show: false,
                    position: 'center',
                    formatter: '{b}: {d}%'
                },
                series: [
                    {
                        name: '用户性别分布',
                        type: 'pie',
                        radius: ['30%', '50%'],
                        center:["50%", "56%"],
                        data: data?data:[]
                    }
                ]
            };

            if (data) {
                myChart.setOption(option);
              } else {
                myChart.setOption({});
              }
        },


    }
})