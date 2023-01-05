'''
文件：Taxi_sz
VehicleNum,Stime,SLng,SLat,ELng,ELat,Etime
'''
import matplotlib.pyplot as plt
import transbigdata as tbd
import pandas as pd
import time
import json
#Set your mapboxtoken with the following code
tbd.set_mapboxtoken('pk.eyJ1IjoiYmluZy10YW5nIiwiYSI6ImNsY2lrMHNqMzB6NXQzcHF1OGoybDFxYnMifQ.uq8EJpaSTyuvD0kCT7bTkQ')
# The token you applied for must be set in it.
# Copying this line of code directly is invalid
# Set your map basemap storage path
# On linux or mac, the path is written like this.
# Note that there is a backslash at the end
tbd.set_imgsavepath(r'C:\Users\77684\Desktop')
#解决中文乱码
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
#读取出租车GPS数据
data = pd.read_csv('Taxi_sz.csv',low_memory=False)
bounds = [113.76666666666667, 22.45, 114.61666666666666,22.866666666666667]#定义研究范围
#剔除研究范围外的数据
data = tbd.clean_outofbounds(data,bounds = bounds,col = ['SLng','SLat'])
#print(data)
params = tbd.area_to_params(bounds,accuracy = 1000)#获取栅格化参数
#print(params)
params['theta'] = 30
#设置为六边形网格
params['method'] = 'hexa'
#设置为三角形网格: params['method'] = 'tri'
#三角形和六边形网格要求三列存储栅格ID信息
data['loncol_1'],data['loncol_2'],data['loncol_3'] = tbd.GPS_to_grid(data['SLng'],data['SLat'],params)
#聚合集计栅格内数据量
grid_agg = data.groupby(['loncol_1','loncol_2','loncol_3'])['VehicleNum'].count().reset_index()
#聚合集计栅格内数据量
grid_agg = data.groupby(['loncol_1','loncol_2','loncol_3'])['VehicleNum'].count().reset_index()
#print(grid_agg)
#生成栅格的几何图形
grid_agg['geometry'] = tbd.grid_to_polygon([grid_agg['loncol_1'],grid_agg['loncol_2'],grid_agg['loncol_3']],params)
'''
#转换为GeoDataFrame
data['LONCOL'],data['LATCOL'] = tbd.GPS_to_grid(data['SLng'],data['SLat'],params)#将GPS数据对应至栅格
grid_agg = data.groupby(['LONCOL','LATCOL'])['VehicleNum'].count().reset_index()#聚合集计栅格内数据量
#生成栅格的几何图形
grid_agg['geometry'] = tbd.grid_to_polygon([grid_agg['LONCOL'],grid_agg['LATCOL']],params)
'''
l = [grid_agg]
#转换为GeoDataFrame
import geopandas as gpd
grid_agg = gpd.GeoDataFrame(grid_agg)

#绘制栅格
grid_agg.plot(column = 'VehicleNum',cmap = 'autumn_r')

plt.title('数据栅格化处理')
#绘制底图
fig =plt.figure(1,(10,8),dpi=300)
ax =plt.subplot(111)
plt.sca(ax)
#加载地图底图
tbd.plot_map(plt,bounds,zoom = 11,style = 4)
#定义色条位置
cax = plt.axes([0.05, 0.33, 0.02, 0.3])
plt.title('Data count')
plt.sca(ax)
#绘制数据
grid_agg.plot(column = 'VehicleNum',cmap = 'autumn_r',ax = ax,cax = cax,legend = True)
#添加指北针和比例尺
tbd.plotscale(ax,bounds = bounds,textsize = 10,compasssize = 1,accuracy = 2000,rect = [0.06,0.03],zorder = 10)
plt.axis('off')
plt.xlim(bounds[0],bounds[2])
plt.ylim(bounds[1],bounds[3])


plt.show()
