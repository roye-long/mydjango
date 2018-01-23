function  plots(lists){

        var  xdata =new Array();
var ydata=[];
for (vars in lists){
    xdata.push(lists[vars].color);
    ydata.push(lists[vars].ct)
}
 require([
                'echarts',
                'echarts/chart/bar',
                'echarts/chart/line',
                'echarts/component/legend',
                'echarts/component/toolbox',
                'echarts/component/title',
                'echarts/component/tooltip'
                //'zrender/vml/vml'
            ], function (echarts) {

                var chart = echarts.init(document.getElementById('main1'), null, {
                    renderer: 'canvas'
                });
                chart.setOption( {
                    //标题
                    title :{
                    text: "颜色对比",
                        subtext: "来自京东女装数据",
                        x: 'center'
                    },

                    //图例
                    legend: {
                        //data: ['line', 'line2', 'line3'],
                        data: ['数量','数量2'],
                        x: 'left'
                    },


                    //提示框
                    tooltip: {
                        trigger: 'axis',
                        show:true
                    },
                    //工具箱
                    toolbox: {
                        show: true,
                        feature: {
                            mark: {show: true},
                            dataView: {show: true, readOnly: false},
                            magicType: {show: true, type: ['line', 'bar']},
                            restore: {show: true},
                            saveAsImage: {show: true}
                        }
                    },
                    calculable : true,
                    //坐标轴
                    xAxis: {
                        name:'颜色样式',
                        data: xdata,
                    },
                    yAxis: {

                        name : '数据(件)',
                        type : 'value'

                    },
                    series: [{
                        name: '数量',
                        type: 'bar',
                        //barWidth:10,
                        //stack: 'all',
                        //symbolSize: 10,
                        data: ydata,
                        //itemStyle: itemStyle,
                        //smooth: true,
                        //connectNulls: true
                    }, {
                        name: '数量2',
                        type: 'line',
                        //stack: 'all',
                        //symbolSize: 10,
                        data: ydata,
                        //itemStyle: itemStyle,
                        //connectNulls: true,
                        //smooth: true
                    }/* {
                        name: 'line3',
                        type: 'line',
                        stack: 'all',
                        symbolSize: 10,
                        data: data3,
                        itemStyle: itemStyle,
                        label: {
                            normal: {
                                show: true
                            }
                        },
                        connectNulls: true,
                        smooth: true
                    }*/]
                });
              });
        }


