import csv  # 只能用这个了
import matplotlib.pyplot as plt
from datetime import datetime
import time
import matplotlib.pyplot as plt
import pandas as  pd
import json
# 解决中文乱码

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def info_print():
    print('---------------第五组实训数据分析系统----------------')
    print('1.按时间统计车辆数量-----------------（功能实现：张亚飞）')
    print('2.乘车时间统计----------------------（功能实现：许晓贤）')
    print('3.按时间统计乘客的乘车时间-------------(功能实现：杨浩铭）')
    print('4.根据汽车坐标绘制车辆的行驶轨迹--------（功能实现：狄城聿）')
    print('5.根据数据分析汽车载客时的车速分布------（功能实现：张路航）')
    print('6.根据乘客上车地点绘制乘客需求量的热力图--（功能实现：李卓言）')
    print('7.根据汽车经纬度变化算出汽车一天行驶总距离-（功能实现：狄城聿）')
    print('8.栅格化处理-------------------------（功能实现：李卓言）')
    print('9.退出系统')
    print('-' * 20)
def xq1():#.按时间统计车辆数量（功能实现：张亚飞
    data = []
    start = time.perf_counter()
    with open('Taxi-sz_data.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)  # 读取到reader里面
        # 忽略第一行
        next(reader)
        # 读取每一行数据
        for row in reader:
            data.append(row)

    a = [[0] for x in range(24)]  # 批量生成列表
    for row in data:
        if row[1]:
            # 进行非空判断
            stime = datetime.strptime(row[1], '%H:%M:%S')  ##时间转换
            s = stime.hour  # 算出所在小时，便于分组
            a[s][0] = a[s][0] + 1
            # 车辆累加
    # 分列表
    x = []
    y = []
    for i in range(24):
        x.append(str(i))
        y.append(a[i][0])
    # 画图
    plt.figure()
    plt.plot(x, y, c='r')
    plt.title('按时间统计车辆数量折线图(第五组)')
    plt.ylabel('车辆数量')
    plt.xlabel('时间')
    plt.show()  # ok了
    end = time.perf_counter()
    print('----------代码运行时间: {}s----------'.format(int(end - start)))
def xq2():#2.乘车时间统计（功能实现：许晓贤）
    start = time.perf_counter()
    data = []
    with open('Taxi_sz.csv', 'r') as csvfile:  # 因为如果用iloc等读取函数处理，后续时间复杂度会增大，因此使用了将数据先读入列表这种方法
        reader = csv.reader(csvfile)  # 读取到reader里面
        # 忽略第一行
        next(reader)
        # 读取每一行数据
        for row in reader:
            data.append(row)

    a = []  # 建一个空列表，用于存乘坐时间
    for f in data:
        if f[1] and f[6]:  ##判断值是否存在
            stime = datetime.strptime(f[1], '%H:%M:%S')  ##时间转换
            s = stime.hour  # 算出所在小时，便与后续分列表
            etime = datetime.strptime(f[6], '%H:%M:%S')  ##时间转换
            times = str(etime - stime)  # 计算 etime 和 stime 的差值,为乘车时间
            ftime = int(times[-5:-3]) + int(times[-2:]) / 60  # 切片字符串计算后化成int格式
            ftime = round(ftime, 2)  # 取两位小数
            a.append(ftime)  # 填充列表

    plt.figure()
    plt.boxplot(a)  # 列表数据导入
    # 标题，横纵坐标标签
    plt.title('乘车时间统计的箱形图(第五组)')
    plt.ylabel('minutes')
    plt.xlabel('Order time')
    plt.grid(linestyle='--', axis='y')  # 加入网格
    plt.show()
    end = time.perf_counter()
    print('----------代码运行时间: {}s----------'.format(int(end - start)))



def xq3():#按时间统计乘客的乘车时间(功能实现：杨浩铭）
    start = time.perf_counter()
    data = []
    # 读取 CSV 文件
    with open('Taxi_sz.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)  # 读取到reader里面
        # 忽略第一行
        next(reader)
        # 读取每一行数据
        for row in reader:
            data.append(row)
    a = [[] for x in range(24)]  # 批量生成列表
    # 这是核心代码，因为pd不好处理，试了一个下午时间复杂度而有点高，所以用来列表嵌套列表这种方法
    for row in data:
        # 进行非空判断
        if row[1] and row[6]:
            stime = datetime.strptime(row[1], '%H:%M:%S')  ##时间转换
            s = stime.hour  # 算出所在小时，便与后续分列表
            etime = datetime.strptime(row[6], '%H:%M:%S')  ##时间转换
            # 计算 etime 和 stime 的差值
            diff = str(etime - stime)  # 算出乘车时间，用minutes等函数直接取分钟可能会出错，所以有下面的一行
            diff = int(diff[-5:-3]) + round(int(diff[-2:]) / 60, 2)  # 将时间格式换算一下通过切片字符串计算后化成int格式
            if diff >= 0:
                a[s].append(diff)  # 这个地方就是本代码的巧妙之处，通过上面所处的小时知道位于那个时段，在a列表中的相应时间段精准加入diff
    plt.figure()
    plt.boxplot(a)  # 列表导入到boxplots
    # 标题，横纵坐标标签
    plt.title('按时间统计乘客的乘车时间箱形图(第五组)')
    plt.ylabel('Order time(minutes)')
    plt.xlabel('Order start time')

    # 下面三行是为了对照需求文档，改动的横坐标刻度,为了这个下面三行，csdn看烂了
    xticks = plt.xticks()[0]
    new_xtick_labels = [tick - 1 for tick in xticks]  # 将每个横坐标刻度的数减一
    plt.xticks(xticks[0:], new_xtick_labels)  # 使用新的横坐标刻度更新坐标轴
    # 显示图形，ok结束
    plt.show()
    end = time.perf_counter()
    print('----------代码运行时间: {}s----------'.format(int(end - start)))
def xq4():#根据汽车坐标绘制车辆的行驶轨迹（功能实现：狄城聿）
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
        <title>车辆轨迹(第五组）</title>
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
    end = time.perf_counter()
    print('----------代码运行时间: {}s----------'.format(int(end - start)))
    f.close()
    webbrowser.open_new_tab('1.html')



def xq5():#根据数据分析汽车载客时的车速分布（功能实现：张路航）
    start = time.perf_counter()
    sale_df =pd.read_csv(r'Taxi-sz_data.csv', encoding='utf-8')  ##读取数据
    # print(sale_df)
    salem = sale_df[sale_df['OpenStatus'] > 0]  # 筛查有乘客的数据
    salem = pd.DataFrame(salem, columns=['VehicleNum', 'Speed'])  # 取出有乘客数据的所有行的车牌和速度
    # print(salem)
    s = salem.groupby('VehicleNum').mean()  # 合并相同车牌号相同车牌的速度取均值
    # print(s)
    list1 = s['Speed'].values.tolist()
    # print(list1)
    zidian = {'[0,10)': 0, '[10,20)': 0, '[20,30)': 0, '[30,40)': 0, '[40,50)': 0, '[50,60)': 0, '[60,70)': 0,
              '[70,80)': 0, '[80,90)': 0, '[90,100)': 0, '[100,110)': 0, '[110,120)': 0}
    # 限速应该是70，写到90了,算了写到120吧
    for i in list1:  # 计数
        if 0 <= i < 10:
            zidian['[0,10)'] += 1
        elif 10 <= i < 20:
            zidian['[10,20)'] += 1
        elif 20 <= i < 30:
            zidian['[20,30)'] += 1
        elif 30 <= i < 40:
            zidian['[30,40)'] += 1
        elif 40 <= i < 50:
            zidian['[40,50)'] += 1
        elif 50 <= i < 60:
            zidian['[50,60)'] += 1
        elif 70 <= i < 80:
            zidian['[70,80)'] += 1
        elif 80 <= i < 90:
            zidian['[80,90)'] += 1
        elif 90 <= i < 100:
            zidian['[90,100)'] += 1
        elif 100 <= i < 110:
            zidian['[100,110)'] += 1
        elif 110 <= i <= 120:
            zidian['[110,120)'] += 1

    # 再验证一下我的速度划分其实没有问题，嘻嘻
    sum = 0
    sum0 = len(list1)
    for i in zidian:
        sum = sum + zidian[i]
    plt.figure()
    for i in zidian:
        plt.bar(i, zidian[i], color='blue')
        plt.text(i, zidian[i], zidian[i], ha='center', va='bottom', fontsize=10)  # 显示数据
    plt.grid(linestyle='--', axis='y')  # 网格图
    plt.title('汽车载客时车速分布柱状图(第五组)')
    plt.xlabel("速度区间")
    plt.ylabel("汽车数量")
    plt.xticks(rotation=30)  # 解决纵坐标重叠问题
    plt.show()
    end = time.perf_counter()
    print('----------代码运行时间: {}s----------'.format(int(end - start)))

def xq6():#根据乘客上车地点绘制乘客需求量的热力图（功能实现：李卓言）
    start = time.perf_counter()
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
        <title>热力图(第五组)</title>
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
    end = time.perf_counter()
    print('----------代码运行时间: {}s----------'.format(int(end - start)))
    f.close()
    webbrowser.open_new_tab('2.html')
def xq7():#根据汽车经纬度变化算出汽车一天行驶总距离（功能实现：狄城聿）

    # python程序运行时间
    start111 = time.perf_counter()
    # 调用百度地图api最后返回值为距离，输入字符串

    from haversine import haversine

    def getDistance(start, end):
        # 计算经纬度的函数
        # 调用haversine 包中的方法
        # 输入的格式：经度，纬度
        dis = haversine(start, end)
        dis = round(dis, 2)
        return dis

    # 解决中文乱码
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    ##读取数据
    sale_df = pd.read_csv(r'Taxi-sz_data.csv', encoding='utf-8')
    # 其实可以做出来全部的，但是免费api一天也就给几万额度，根本不够用
    car_22271 = sale_df.loc[sale_df['VehicleNum'] == 22271]  # 1
    car_24272 = sale_df.loc[sale_df['VehicleNum'] == 24272]  # 2
    car_26454 = sale_df.loc[sale_df['VehicleNum'] == 26454]  # 3
    car_36805 = sale_df.loc[sale_df['VehicleNum'] == 36805]  # 4
    car_27261 = sale_df.loc[sale_df['VehicleNum'] == 27261]  # 5
    car_34516 = sale_df.loc[sale_df['VehicleNum'] == 34516]  # 6
    car_34141 = sale_df.loc[sale_df['VehicleNum'] == 34141]  # 7
    car_22437 = sale_df.loc[sale_df['VehicleNum'] == 22437]  # 8
    car_32312 = sale_df.loc[sale_df['VehicleNum'] == 32312]  # 9
    car_32770 = sale_df.loc[sale_df['VehicleNum'] == 32770]  # 10
    # 建一个列表把一个一个搞太难了
    h = [car_22271, car_24272, car_26454, car_36805, car_27261, car_34516, car_34141, car_22437, car_32312, car_32770]
    hdist = {'car_22271': 0, 'car_24272': 0, 'car_26454': 0, 'car_36805': 0, 'car_27261': 0, 'car_34516': 0,
             'car_34141': 0, 'car_22437': 0, 'car_32312': 0, 'car_32770': 0}  # 字典后续存入距离
    for i in h:
        i = i.sort_values(by=['Stime'], na_position='first')  # 按时间对每个车进行排序
    for j in h:
        hzifuchuan = "car_" + str(j.iloc[3]['VehicleNum'])
        # 这个确实想了好长时间，就是首先j是一个数据集，里面车牌都是一样的，就随机取第三行的车牌数据，并化成字符串，用字符串完成后续对字典的定位
        # 12月30号23.39成功把配额用完，说明还是不能全分析，只能分析十个
        li = int(len(j)) - 1  # 这里的-1是因为减去了标题行
        for m in range(1, li):  # 这里m的值是从1到li，所以不会超出索引的
            start = (j.iloc[m]["Lat"], j.iloc[m]['Lng'])  # 读取表格中的经纬度并且规范格式
            end = (j.iloc[m + 1]["Lat"], j.iloc[m + 1]['Lng'])  # 调取上一个的下一行（最大到最后一行）的经纬度并且规范格式
            dist = getDistance(start, end)
            hdist[hzifuchuan] = int(hdist.get(hzifuchuan)) + dist
            # 输出start检测api配合，没办法数据太大

    plt.figure()
    for l in h:
        hzifuchuan2 = "car_" + str(l.iloc[3]['VehicleNum'])
        plt.bar(hzifuchuan2, hdist[hzifuchuan2], color='green')
        plt.text(hzifuchuan2, hdist[hzifuchuan2], hdist[hzifuchuan2], ha='center', va='bottom', fontsize=10)  # 显示数据
    plt.grid(linestyle='--', axis='y')  # 网格图
    plt.title('分析十辆汽车一天行驶里程数的柱状图(第五组)')
    plt.xlabel("汽车标号")
    plt.ylabel("汽车行驶总距离/m")
    plt.xticks(rotation=30)  # 解决纵坐标重叠问题
    ##晚上23.54成功拿下，那年我双手插兜，不知道什么是对手
    ##由于数据大，api用完了，正在借，目前凌晨0.42
    ##目前凌晨2点整，只能通过截取老师给的数据降低运算，太多了，api也不够用，实在不行写一个自动换ak函数
    ##api时间复杂度拉满了，今天跑了1个多小时还没跑完，只能用函数了
    plt.show()
    end111 = time.perf_counter()
    print('----------代码运行时间: {}s----------'.format(int(end111 - start111)))
def xq8():
    '''
    文件：Taxi_sz
    VehicleNum,Stime,SLng,SLat,ELng,ELat,Etime
    '''
    import matplotlib.pyplot as plt
    import transbigdata as tbd
    import pandas as pd
    # 解决中文乱码
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 读取出租车GPS数据
    data = pd.read_csv('Taxi_sz.csv', low_memory=False)
    bounds = [113.76666666666667, 22.45, 114.61666666666666, 22.866666666666667]  # 定义研究范围
    # 剔除研究范围外的数据
    data = tbd.clean_outofbounds(data, bounds=bounds, col=['SLng', 'SLat'])
    print(data)
    params = tbd.area_to_params(bounds, accuracy=700)  # 获取栅格化参数
    print(params)
    data['LONCOL'], data['LATCOL'] = tbd.GPS_to_grid(data['SLng'], data['SLat'], params)  # 将GPS数据对应至栅格
    grid_agg = data.groupby(['LONCOL', 'LATCOL'])['VehicleNum'].count().reset_index()  # 聚合集计栅格内数据量
    # 生成栅格的几何图形
    grid_agg['geometry'] = tbd.grid_to_polygon([grid_agg['LONCOL'], grid_agg['LATCOL']], params)
    # 转换为GeoDataFrame
    import geopandas as gpd
    grid_agg = gpd.GeoDataFrame(grid_agg)

    # 绘制栅格

    grid_agg.plot(column='VehicleNum', cmap='Wistia')

    plt.title('数据栅格化处理')
    plt.show()


while True:

    info_print()

    # 2.用户输入选项(1~7)，选择不同的操作
    choice = eval(input('输入操作选项:'))

    # 3.根据用户的选项进行相应的操作
    if choice == 1:#1.按时间统计车辆数量（功能实现：张亚飞）
        print('请耐心等待，正在运行...')
        xq1()
    elif choice == 2:#2.乘车时间统计（功能实现：许晓贤）
        print('请耐心等待，正在运行...')
        xq2()

    elif choice == 3:#按时间统计乘客的乘车时间(功能实现：杨浩铭）
        print('请耐心等待，正在运行...')
        xq3()
    elif choice == 4:#根据汽车坐标绘制车辆的行驶轨迹（功能实现：狄城聿）
        print('请耐心等待，正在运行...')
        xq4()
    elif choice == 5:#根据数据分析汽车载客时的车速分布（功能实现：张路航）
        print('请耐心等待，正在运行...')
        xq5()
    elif choice == 6:#根据乘客上车地点绘制乘客需求量的热力图（功能实现：李卓言）
        print('请耐心等待，正在运行...')
        xq6()
    elif choice == 7:#根据汽车经纬度变化算出汽车一天行驶总距离（功能实现：狄城聿）
        print('请耐心等待，正在运行...')
        xq7()
    elif choice == 8:  # 根据汽车经纬度变化算出汽车一天行驶总距离（功能实现：狄城聿）
        print('请耐心等待，正在运行...')
        xq8()

    elif choice == 9:
        flag = input("确定是否退出吗？yes/no:")
        if flag == 'yes':
            print('谢谢使用！')
            break
    else:
        print('输入有误，请重新选择')
