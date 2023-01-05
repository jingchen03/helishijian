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

# python程序运行时间
start = time.perf_counter()
##读取数据
sale_df = pd.read_csv(r'Taxi-sz_data.csv', encoding='utf-8')
# 选取车辆
car_22271 = sale_df.loc[sale_df['VehicleNum'] == 27261]
# 对时间进行排序
car_22271 = car_22271.sort_values(by=['Stime'], na_position='first')
s = len(car_22271)
l = []
for i in range(s):
    a = []
    a1 = car_22271.iloc[i]['Lng']
    a2 = car_22271.iloc[i]['Lat']
    a.append(a1)
    a.append(a2)
    l.append(a)
l_js = json.dumps(l)  # 转换格式为l_js
import webbrowser

f = open('1.html', 'w', encoding="utf-8")
message = """<!doctype html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no, width=device-width">
    <title>轨迹回放(第五组）</title>
    <audio
    autoplay="autoplay"
    loop="loop"
    preload="auto"
    src="bgm.mp3">
    </audio>

    <link rel="stylesheet" href="https://a.amap.com/jsapi_demos/static/demo-center/css/demo-center.css"/>
    <style>
        html, body, #container {
            height: 100%;
            width: 100%;
        }

        .input-card .btn{
            margin-right: 1.2rem;
            width: 9rem;
        }

        .input-card .btn:last-child{
            margin-right: 0;
        }
    </style>
</head>
<body>

<script>
  var l = JSON.parse('""" + l_js + """');
  console.log(l);
</script>  


<div id="container"></div>
<div class="input-card">
    <h4>轨迹回放控制</h4>
    <div class="input-item">
        <input type="button" class="btn" value="开始动画" id="start" onclick="startAnimation()"/>
        <input type="button" class="btn" value="暂停动画" id="pause" onclick="pauseAnimation()"/>
    </div>
    <div class="input-item">
        <input type="button" class="btn" value="继续动画" id="resume" onclick="resumeAnimation()"/>
        <input type="button" class="btn" value="停止动画" id="stop" onclick="stopAnimation()"/>
    </div>
</div>
<script type="text/javascript" src="https://webapi.amap.com/maps?v=2.0&key=bdbc41f0511a3da8b56e550ee305e61c"></script>

<script>
    // JSAPI2.0 使用覆盖物动画必须先加载动画插件
    AMap.plugin('AMap.MoveAnimation', function(){
        var marker, lineArr =  l     //传入的列表
         var map = new AMap.Map("container", {
            resizeEnable: true,
            center: [116.397428, 39.90923],
            zoom: 17
        });

        marker = new AMap.Marker({
            map: map,
            position: [114.136497, 22.567499],
            icon: "https://a.amap.com/jsapi_demos/static/demo-center-v2/car.png",
            offset: new AMap.Pixel(-13, -26),
        });

        // 绘制轨迹
        var polyline = new AMap.Polyline({
            map: map,
            path: lineArr,
            showDir:true,
            strokeColor: "#28F",  //线颜色
            // strokeOpacity: 1,     //线透明度
            strokeWeight: 6,      //线宽
            // strokeStyle: "solid"  //线样式
        });

        var passedPolyline = new AMap.Polyline({
            map: map,
            strokeColor: "#AF5",  //线颜色
            strokeWeight: 6,      //线宽
        });


        marker.on('moving', function (e) {
            passedPolyline.setPath(e.passedPath);
            map.setCenter(e.target.getPosition(),true)
        });

        map.setFitView();

        window.startAnimation = function startAnimation () {
            marker.moveAlong(lineArr, {
                // 每一段的时长
                duration: 500,//可根据实际采集时间间隔设置
                // JSAPI2.0 是否延道路自动设置角度在 moveAlong 里设置
                autoRotation: true,
            });
        };

        window.pauseAnimation = function () {
            marker.pauseMove();
        };

        window.resumeAnimation = function () {
            marker.resumeMove();
        };

        window.stopAnimation = function () {
            marker.stopMove();
        };
    });
</script>
</body>
</html>
"""

f.write(message)
f.close()

webbrowser.open_new_tab('1.html')
