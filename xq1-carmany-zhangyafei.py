'''
文件：Taxi-sz_data:
VehicleNum,Stime,Lng,Lat,OpenStatus,Speed
车辆车牌，时间，纬度，经度，载客状态，速度

文件：Taxi_sz
VehicleNum,Stime,SLng,SLat,ELng,ELat,Etime
车辆车牌，开始时间，开始经度，开始纬度，结束时间，结束经度，结束纬度
'''
import csv  # 只能用这个了
import matplotlib.pyplot as plt
from datetime import datetime
import time
start= time.perf_counter()

# 解决中文乱码

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
data = []
# 读取 CSV 文件
with open('Taxi-sz_data.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)  # 读取到reader里面
    # 忽略第一行
    next(reader)
    # 读取每一行数据
    for row in reader:
        data.append(row)

a = [[0] for x in range(24)]#批量生成列表
for row in data:
    if row[1]:
    # 进行非空判断
        stime = datetime.strptime(row[1], '%H:%M:%S')  ##时间转换
        s = stime.hour  # 算出所在小时，便于分组
        a[s][0] = a[s][0] + 1
        #车辆累加
#分列表
x=[]
y=[]
for i in range(24):
    x.append(str(i))
    y.append(a[i][0])
#画图
plt.figure()
plt.plot(x, y,c='r')
plt.title('按时间统计车辆数量折线图(第五组)')
plt.ylabel('车辆数量')
plt.xlabel('时间')
plt.show()#ok了
end = time.perf_counter()
print('----------代码运行时间: {}s----------'.format(int(end - start)))
