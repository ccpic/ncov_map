# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from data import get_data

path = 'ncov_area.csv'
df = pd.read_csv(path, encoding='UTF-8')  # 读取数据文件到pandas
df = df[~df['省'].isin(['台湾省', '澳门'])]
mask = df['省'] == '新疆维吾尔自治区'
df.loc[mask, '省'] = '新疆维吾尔族自治区'
mask = df['省'] == '内蒙古自治区'
df.loc[mask, '省'] = '内蒙古蒙古族自治区'
mask = df['省'] == '西藏自治区'
df.loc[mask, '省'] = '西藏藏族自治区'

fig = plt.figure()
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
m = Basemap(llcrnrlon=115, llcrnrlat=29, urcrnrlon=120, urcrnrlat=35,
               projection='lcc', lat_1=33, lat_2=45, lon_0=120, ax=ax1)
m.readshapefile('CHN_adm_shp/CHN_adm2', 'states', drawbounds=False)

data = get_data(df, basemap=m, level='市')


for info, shp in zip(m.states_info, m.states):
    proid = info['NAME_1']
    if proid == 'Anhui':
        poly = Polygon(shp, facecolor='w', edgecolor='b', lw=0.2)
        ax1.add_patch(poly)

# bmap.drawcoastlines()
# m.drawcountries()
# bmap.drawparallels(np.arange(23, 29, 2), labels=[1, 0, 0, 0])
# bmap.drawmeridians(np.arange(115, 121, 2), labels=[0, 0, 0, 1])
plt.title('Fujian Province')
plt.savefig('heatmaps/fig_province.png', dpi=100, bbox_inches='tight')
plt.clf()
plt.close()