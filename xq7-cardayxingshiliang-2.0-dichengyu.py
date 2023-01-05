'''
文件：Taxi-sz_data:
VehicleNum,Stime,Lng,Lat,OpenStatus,Speed
车辆车牌，时间，纬度，经度，载客状态，速度
'''
# 调用库
import pandas as pd
import matplotlib.pyplot as plt
import time

# python程序运行时间
start111 = time.perf_counter()
# 调用百度地图api最后返回值为距离，输入字符串

from haversine import haversine


def getDistance(start, end):
    # 计算经纬度的函数
    # 调用haversine 包中的方法
    # 输入的格式：经度，纬度
    dis = haversine(start, end)
    dis=round(dis,2)
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
h = [car_22271, car_24272, car_26454, car_36805,car_27261,car_34516,car_34141,car_22437,car_32312,car_32770]
hdist = {'car_22271': 0, 'car_24272': 0, 'car_26454': 0, 'car_36805': 0,'car_27261':0,'car_34516':0,'car_34141':0,'car_22437':0,'car_32312':0,'car_32770':0}  # 字典后续存入距离
for i in h:
    i = i.sort_values(by=['Stime'], na_position='first')  # 按时间对每个车进行排序
for j in h:
    hzifuchuan = "car_" + str(j.iloc[3]['VehicleNum'])
    # 这个确实想了好长时间，就是首先j是一个数据集，里面车牌都是一样的，就随机取第三行的车牌数据，并化成字符串，用字符串完成后续对字典的定位
    # 12月30号23.39成功把配额用完，说明还是不能全分析，只能分析十个
    li = int(len(j)) - 1  # 这里的-1是因为减去了标题行
    for m in range(1, li):  # 这里m的值是从1到li，所以不会超出索引的
        start =(j.iloc[m]["Lat"],j.iloc[m]['Lng'] ) # 读取表格中的经纬度并且规范格式
        end = (j.iloc[m + 1]["Lat"],j.iloc[m + 1]['Lng'])  # 调取上一个的下一行（最大到最后一行）的经纬度并且规范格式
        dist = getDistance(start, end)
        hdist[hzifuchuan] = int(hdist.get(hzifuchuan)) + dist
        end111 = time.perf_counter()
        print('----------Running time: {}s----------函数算出距离为{}m'.format(int(end111 - start111),
                                                                             dist))  # 输出start检测api配合，没办法数据太大

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
