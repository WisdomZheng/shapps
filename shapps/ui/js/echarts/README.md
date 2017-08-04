sample:
=============================
HTML:
-----------------------------
```
<!-- prepare a DOM with height and width set for ECharts -->
<div id="main" style="width:600px; height:400px;"></div>
<!-- or use percentage -->
<div id="main" style="width:80%; height:20%;"></div>
```

JS:
-----------------------------
```
// init echarts instance
var myChart = echarts.init(document.getElementById('main'));

// set options for echarts
var option = {
            title: {
                text: 'ECharts Example'
            },
            tooltip: {},
            legend: {
                data:['Sales']
            },
            xAxis: {
                data: ["Shirt","Sweater","Coat","Pants","Shoes","Socks"]
            },
            yAxis: {},
            series: [{
                name: 'Sales',
                type: 'bar',
                data: [5, 20, 36, 10, 10, 20]
            }]
        };

// link option to echarts
myChart.setOption(option);
```


DOCS:
-----------------------------
```
Official Page: http://echarts.baidu.com/
Tutorial: http://echarts.baidu.com/tutorial.html
API: http://echarts.baidu.com/api.html
Options Setting: http://echarts.baidu.com/option.html
Examples: http://echarts.baidu.com/examples.html
```