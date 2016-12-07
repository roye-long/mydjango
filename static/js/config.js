require.config({
    packages: [
        {
            main: 'echarts',
            location: '/static/echarts/src',
            name: 'echarts'
        },
        {
            main: 'zrender',
            location: '/static/echarts/zrender-master/src',
            name: 'zrender'
        }
    ]
    // urlArgs: '_v_=' + +new Date()
});
