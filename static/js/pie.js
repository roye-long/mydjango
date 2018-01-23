/**
 * Created by Administrator on 2016/12/9.
 */
/**
 * Created by Administrator on 2016/12/9.
 */
function  pieplots(lists,mains){

        var  xdata =new Array();
var ydata=[];
var data=[]
for (vars in lists){
    xdata.push(lists[vars].choice_text);
    ydata.push(lists[vars].svotes)
    data.push({value:lists[vars].svotes,name:lists[vars].choice_text})
}

 require([
                'echarts',
                'echarts/chart/pie',
                'echarts/chart/funnel',
                'echarts/component/legend',
                'echarts/component/toolbox',
                'echarts/component/title',
                'echarts/component/tooltip'
                //'zrender/vml/vml'
            ], function (echarts) {

                var chart = echarts.init(document.getElementById(mains), null, {
                    renderer: 'canvas'
                });
                chart.setOption( {
    title : {
        text: '各问题投票人数分布',
        subtext: '数据来源投票结果',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        orient : 'vertical',
        x : 'left',
        data:xdata
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {
                show: true,
                type: ['pie', 'funnel'],
                option: {
                    funnel: {
                        x: '25%',
                        width: '50%',
                        funnelAlign: 'left',
                        max: 1548
                    }
                }
            },
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    series : [
        {
            name:'问题',
            type:'pie',
            radius : '55%',
            center: ['50%', '60%'],
            data:data,
        }
    ]
});
              });
        }


