/**
 * Created by Administrator on 2016/12/6.
 */
function  plots(lists){

        var  xdata =new Array();
var yxdata=[];
var yidata=[]
for (vars in lists){
    xdata.push(lists[vars].xinqi);
    yxdata.push(lists[vars].maxs)
    yidata.push(lists[vars].minx)
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
                chart.setOption({
    title : {
        text: '未来一周气温变化',
        subtext: '纯属虚构'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['最高气温','最低气温']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            boundaryGap : false,
            data :xdata
        }
    ],
    yAxis : [
        {
            type : 'value',
            axisLabel : {
                formatter: '{value} °C'
            }
        }
    ],
    series : [
        {
            name:'最高气温',
            type:'line',
            data:yxdata,
            markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                ]
            },
            markLine : {
                data : [
                    {type : 'average', name: '平均值'}
                ]
            }
        },
        {
            name:'最低气温',
            type:'line',
            data:yidata,
            markPoint : {
                data : [
                    {name : '周最低', value : -2, xAxis: 1, yAxis: -1.5}
                ]
            },
            markLine : {
                data : [
                    {type : 'average', name : '平均值'}
                ]
            }
        }
    ]
})});}