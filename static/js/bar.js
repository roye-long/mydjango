/**
 * Created by Administrator on 2016/12/9.
 */
function  barplots(lists,mains){

        var  xdata =new Array();
var ydata=[];
for (vars in lists){
    xdata.push(lists[vars].question__question_text);
    ydata.push(lists[vars].svotes)
}
 require([
                'echarts',
                'echarts/chart/bar',
                'echarts/chart/line',
                'echarts/component/legend',
                'echarts/component/toolbox',
                'echarts/component/title',
                'echarts/component/tooltip',
                 'zrender/vml/vml'
            ], function (echarts) {

                var chart = echarts.init(document.getElementById(mains), null, {
                    renderer: 'canvas'
                });
                chart.setOption( {
                    //标题
                    title :{
                    text: "各问题各选项投票人数对比",
                        subtext: "数据来自问卷调查",
                        x: 'center'
                    },

                    //图例
                    legend: {
                        //data: ['line', 'line2', 'line3'],
                        data: ['人数'],
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
                        name:'问题',
                        data: xdata,
                    },
                    yAxis: {

                        name : '人数(人)',
                        type : 'value'

                    },
                    series: [{
                        name: '人数',
                        type: 'bar',
                        barWidth:50,
                        //stack: 'all',
                        //symbolSize: 10,
                        data: ydata,
                        //itemStyle: itemStyle,
                        //smooth: true,
                        //connectNulls: true
                    }, ]
                });
              });
        }


