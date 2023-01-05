'''
文件：Taxi-sz_data:
VehicleNum,Stime,Lng,Lat,OpenStatus,Speed
车辆车牌，时间，纬度，经度，载客状态，速度

文件：Taxi_sz
VehicleNum,Stime,SLng,SLat,ELng,ELat,Etime
车辆车牌，开始时间，开始经度，开始纬度，结束时间，结束经度，结束纬度
'''
# 调用库
import pandas as pd
import time
import json
import webbrowser
# 读取数据
df = pd.read_csv(r'Taxi_sz.csv', encoding='utf-8')
# 通过求出上车地点的经纬度
# 想办法以 { "lat": 32.04671099494339, "lng": 118.80369003879538, "count": 16 },形式输出经纬度
# df_1 = pd.DataFrame(df,columns=['SLng','SLat'])

l = []
num = len(df['SLng'])
def add(lng, lat):
    dic = {"lat": lat, "lng": lng, "count": 1}
    l.append(dic)
    return
    pass

for i in range(0, num):
    try:
        if df['SLng'][i] == "" or df['SLat'][i] == "":
            continue
        else:
            add(float(df['SLng'][i]), float(df['SLat'][i]))
    except:
        continue
l_js = json.dumps(l)  # 转换格式为l_js

import webbrowser

f = open('2.html', 'w', encoding="utf-8")
message = """  <!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=GuYvQB29PygR5ab2fcbBNpoE9Aagn3xb"></script>
    <script type="text/javascript" src="http://api.map.baidu.com/library/Heatmap/2.0/src/Heatmap_min.js"></script>
    <title>热力图功能示例</title>
    <style type="text/css">
        ul,li{list-style: none;margin:0;padding:0;float:left;}
        html{height:100%}
        body{height:100%;margin:0px;padding:0px;font-family:"微软雅黑";}
        #container{height:90%;width:100%;}
        #r-result{width:100%;}
    </style>
</head>
<body>
    <script>
    var l = JSON.parse('""" + l_js + """');
    console.log(l);
    </script>
    <div id="container"></div>
    <div id="r-result">
        <input type="button"  onclick="openHeatmap();" value="显示热力图"/><input type="button"  onclick="closeHeatmap();" value="关闭热力图"/>
    </div>
</body>
</html>
<script type="text/javascript">
    var map = new BMap.Map("container");          // 创建地图实例

    var point = new BMap.Point(114.190598,22.6478);
    map.centerAndZoom(point, 12);             // 初始化地图，设置中心点坐标和地图级别
    map.enableScrollWheelZoom(); // 允许滚轮缩放

    var points = l
	

    if(!isSupportCanvas()){
        alert('热力图目前只支持有canvas支持的浏览器,您所使用的浏览器不能使用热力图功能~')
    }
    //详细的参数,可以查看heatmap.js的文档 https://github.com/pa7/heatmap.js/blob/master/README.md
    //参数说明如下:
    /* visible 热力图是否显示,默认为true
     * opacity 热力的透明度,1-100
     * radius 势力图的每个点的半径大小
     * gradient  {JSON} 热力图的渐变区间 . gradient如下所示
     *  {
            .2:'rgb(0, 255, 255)',
            .5:'rgb(0, 110, 255)',
            .8:'rgb(100, 0, 255)'
        }
        其中 key 表示插值的位置, 0~1.
            value 为颜色值.
     */
    heatmapOverlay = new BMapLib.HeatmapOverlay({"radius":7});
    map.addOverlay(heatmapOverlay);
    heatmapOverlay.setDataSet({data:points,max:100});
    //是否显示热力图
    function openHeatmap(){
        heatmapOverlay.show();
    }
    function closeHeatmap(){
        heatmapOverlay.hide();
    }
    closeHeatmap();
    function setGradient(){
        /*格式如下所示:
        {
            0:'rgb(102, 255, 0)',
            .5:'rgb(255, 170, 0)',
            1:'rgb(255, 0, 0)'
        }*/
        var gradient = {};
        var colors = document.querySelectorAll("input[type='color']");
        colors = [].slice.call(colors,0);
        colors.forEach(function(ele){
            gradient[ele.getAttribute("data-key")] = ele.value;
        });
        heatmapOverlay.setOptions({"gradient":gradient});
    }
    //判断浏览区是否支持canvas
    function isSupportCanvas(){
        var elem = document.createElement('canvas');
        return !!(elem.getContext && elem.getContext('2d'));
    }
</script>

"""

f.write(message)
f.close()

webbrowser.open_new_tab('2.html')
