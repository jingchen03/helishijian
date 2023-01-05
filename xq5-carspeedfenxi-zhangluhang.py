'''
文件：Taxi-sz_data:
VehicleNum,Stime,Lng,Lat,OpenStatus,Speed
车辆车牌，时间，纬度，经度，载客状态，速度

文件：Taxi_sz
VehicleNum,Stime,SLng,SLat,ELng,ELat,Etime
车辆车牌，开始时间，开始经度，开始纬度，结束时间，结束经度，结束纬度
'''
#调用库
import pandas as  pd
import matplotlib.pyplot as plt
#解决中文乱码
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
sale_df = pd.read_csv(r'Taxi-sz_data.csv',encoding='utf-8')##读取数据
#print(sale_df)
salem=sale_df[sale_df['OpenStatus'] > 0]  #筛查有乘客的数据
salem = pd.DataFrame(salem,columns=['VehicleNum','Speed']) #取出有乘客数据的所有行的车牌和速度
#print(salem)
s=salem.groupby('VehicleNum').mean()   #合并相同车牌号相同车牌的速度取均值
#print(s)
list1=s['Speed'].values.tolist()
#print(list1)
zidian={'[0,10)':0,'[10,20)':0,'[20,30)':0,'[30,40)':0,'[40,50)':0,'[50,60)':0,'[60,70)':0,'[70,80)':0,'[80,90)':0,'[90,100)':0,'[100,110)':0,'[110,120)':0}
#限速应该是70，写到90了,算了写到120吧
for i  in list1:#计数
    if 0<=i<10:
        zidian['[0,10)']+=1
    elif 10<=i<20:
        zidian['[10,20)']+=1
    elif 20<=i<30:
        zidian['[20,30)']+=1
    elif 30<=i<40:
        zidian['[30,40)']+=1
    elif 40<=i<50:
        zidian['[40,50)']+=1
    elif 50<=i<60:
        zidian['[50,60)']+=1
    elif 70<=i<80:
        zidian['[70,80)']+=1
    elif 80<=i<90:
        zidian['[80,90)']+=1
    elif 90<=i<100:
        zidian['[90,100)']+=1
    elif 100<=i<110:
        zidian['[100,110)']+=1
    elif 110<=i<=120:
        zidian['[110,120)']+=1

#再验证一下我的速度划分其实没有问题，嘻嘻
sum = 0
sum0=len(list1)
for i in zidian:
    sum = sum + zidian[i]
if sum==sum0:
    print("字典速度划分合理，数据具有强参考意义")
plt.figure()
for i  in  zidian:
    plt.bar(i,zidian[i],color='blue')
    plt.text(i,zidian[i],zidian[i],ha = 'center',va = 'bottom',fontsize=10)#显示数据
plt.grid(linestyle='--',axis ='y')#网格图
plt.title('汽车载客时车速分布柱状图(第五组)')
plt.xlabel("速度区间")
plt.ylabel("汽车数量")
plt.xticks(rotation=30) #解决纵坐标重叠问题
plt.show()




