'''
文件：Taxi-sz_data:
VehicleNum,Stime,Lng,Lat,OpenStatus,Speed
车辆车牌，时间，纬度，经度，载客状态，速度

文件：Taxi_sz
VehicleNum,Stime,SLng,SLat,ELng,ELat,Etime
车辆车牌，开始时间，开始经度，开始纬度,结束经度，结束纬度，结束时间
'''
#调用库
import matplotlib.pyplot as plt
from datetime import datetime
import time
import  csv
start= time.perf_counter()
#解决中文乱码
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
data=[]
with open('Taxi_sz.csv', 'r') as csvfile:   #因为如果用iloc等读取函数处理，后续时间复杂度会增大，因此使用了将数据先读入列表这种方法
    reader = csv.reader(csvfile)  # 读取到reader里面
    # 忽略第一行
    next(reader)
    # 读取每一行数据
    for row in reader:
        data.append(row)


a=[]  #建一个空列表，用于存乘坐时间
for f in data:
    if f[1] and f[6]:##判断值是否存在
        stime = datetime.strptime(f[1], '%H:%M:%S')  ##时间转换
        s = stime.hour  # 算出所在小时，便与后续分列表
        etime = datetime.strptime(f[6], '%H:%M:%S')  ##时间转换
        times= str(etime - stime)  # 计算 etime 和 stime 的差值,为乘车时间
        ftime = int(times[-5:-3]) + int(times[-2:]) / 60# 切片字符串计算后化成int格式
        ftime=round(ftime,2)  #取两位小数
        a.append(ftime)#填充列表

plt.figure()
plt.boxplot(a)  #列表数据导入
#标题，横纵坐标标签
plt.title('乘车时间统计的箱形图(第五组)')
plt.ylabel('minutes')
plt.xlabel('Order time')
plt.grid(linestyle='--',axis ='y')#加入网格
plt.show()
end = time.perf_counter()
print('----------代码运行时间: {}s----------'.format(int(end - start)))
