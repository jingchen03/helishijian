'''
文件：Taxi_sz
VehicleNum,Stime,SLng,SLat,ELng,ELat,Etime
'''
import matplotlib.pyplot as plt
import transbigdata as tbd
import pandas as pd
#解决中文乱码
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
#读取出租车GPS数据
data = pd.read_csv('Taxi_sz.csv',low_memory=False)
bounds = [113.76666666666667, 22.45, 114.61666666666666,22.866666666666667]#定义研究范围
#剔除研究范围外的数据
data = tbd.clean_outofbounds(data,bounds = bounds,col = ['SLng','SLat'])
print(data)
params = tbd.area_to_params(bounds,accuracy = 700)#获取栅格化参数
print(params)
data['LONCOL'],data['LATCOL'] = tbd.GPS_to_grid(data['SLng'],data['SLat'],params)#将GPS数据对应至栅格
grid_agg = data.groupby(['LONCOL','LATCOL'])['VehicleNum'].count().reset_index()#聚合集计栅格内数据量
#生成栅格的几何图形
grid_agg['geometry'] = tbd.grid_to_polygon([grid_agg['LONCOL'],grid_agg['LATCOL']],params)
#转换为GeoDataFrame
import geopandas as gpd
grid_agg = gpd.GeoDataFrame(grid_agg)

#绘制栅格

grid_agg.plot(column = 'VehicleNum',cmap = 'Wistia')

plt.title('数据栅格化处理')
plt.show()

