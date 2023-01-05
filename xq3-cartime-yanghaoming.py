import csv #只能用这个了
import matplotlib.pyplot as plt
from datetime import datetime
import time
start= time.perf_counter()
#解决中文乱码

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
data = []
# 读取 CSV 文件
with open('Taxi_sz.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)  #读取到reader里面
    # 忽略第一行
    next(reader)
    # 读取每一行数据
    for row in reader:
        data.append(row)
print(data)
a = [[] for x in range(24)]#批量生成列表
#这是核心代码，因为pd不好处理，试了一个下午时间复杂度而有点高，所以用来列表嵌套列表这种方法
for row in data:
    # 进行非空判断
    if row[1] and row[6]:
        stime = datetime.strptime(row[1], '%H:%M:%S')##时间转换
        s = stime.hour#算出所在小时，便与后续分列表
        etime = datetime.strptime(row[6], '%H:%M:%S')##时间转换
        # 计算 etime 和 stime 的差值
        diff = str(etime - stime)#算出乘车时间，用minutes等函数直接取分钟可能会出错，所以有下面的一行
        diff = int(diff[-5:-3]) + round(int(diff[-2:]) / 60, 2)  #将时间格式换算一下通过切片字符串计算后化成int格式
        if diff >=0:
            a[s].append(diff)#这个地方就是本代码的巧妙之处，通过上面所处的小时知道位于那个时段，在a列表中的相应时间段精准加入diff
plt.figure()
plt.boxplot(a)  #列表导入到boxplots
#标题，横纵坐标标签
plt.title('按时间统计乘客的乘车时间箱形图(第五组)')
plt.ylabel('Order time(minutes)')
plt.xlabel('Order start time')

#下面三行是为了对照需求文档，改动的横坐标刻度,为了这个下面三行，csdn看烂了
xticks = plt.xticks()[0]
new_xtick_labels = [tick - 1 for tick in xticks]# 将每个横坐标刻度的数减一
plt.xticks(xticks[0:], new_xtick_labels)# 使用新的横坐标刻度更新坐标轴
# 显示图形，ok结束
plt.show()
end = time.perf_counter()
print('----------代码运行时间: {}s----------'.format(int(end - start)))

