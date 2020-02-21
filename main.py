import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Polygon
from matplotlib.colors import rgb2hex
import numpy as np
from matplotlib.ticker import FuncFormatter
import csv
import matplotlib.font_manager as fm

myfont = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')

# Create URL to JSON file (alternatively this can be a filepath)
path = 'ncov_area.csv'
df = pd.read_csv(path, encoding='UTF-8')
# df = df[df['省'] != '湖北省']
pivoted = pd.pivot_table(df, index='市', values='新增确诊', aggfunc=sum)

data = pivoted['新增确诊']

# city_list = df['市'].unique()
fig, ax = plt.subplots(figsize=(9, 8))

m = Basemap(llcrnrlon=77, llcrnrlat=14, urcrnrlon=140, urcrnrlat=51, projection='lcc', lat_1=33, lat_2=45, lon_0=100)
m.readshapefile('CHN_adm_shp/CHN_adm1', 'states', drawbounds=True)
m.readshapefile('CHN_adm_shp/CHN_adm2', 'counties', drawbounds=False)
m.readshapefile('TWN_adm_shp/TWN_adm0', 'taiwan', drawbounds=True)  # 增加台湾

countynames = []
for shapedict in m.counties_info:
    countyname = shapedict['NL_NAME_2']
    p = countyname.split('|')
    if len(p) > 1:
        s = p[1]
    else:
        s = p[0]
    # #直辖市命名问题
    # if s in ['北京', '上海', '天津', '重庆']:
    #     s = s+'市'
    #撤并的县市
    if s == '巢湖市':
        s = '合肥市'
    if s == '天门市':
        s = '武汉市'
    if s == '潜江市':
        s = '武汉市'
    if s == '仙桃市':
        s = '武汉市'
    if s == '济源市':
        s = '焦作市'
    #部分省直辖区域无法归类，归于最近的城市
    if s == '海南':
        s = '海口市'
    # if s == '神农架林区':
    #     s = '恩施土家族苗族自治州'
    #繁体字导致的错误
    if s == '益陽市':
        s = '益阳市'
    if s == '邵陽市':
        s = '邵阳市'
    if s == '衡陽市':
        s = '衡阳市'
    if s == '岳陽市':
        s = '岳阳市'
    if s == '張家界市':
        s = '张家界市'
    if s == '長沙市':
        s = '长沙市'
    if s == '懷化市':
        s = '怀化市'
    if s == '婁底市':
        s = '娄底市'
    #撤县并市
    if s == '运城县':
        s = '运城市'
    #用字不同
    if s == '巴音郭愣蒙古自治州':
        s = '巴彦卓尔蒙古自治州'
    # #少'市'字
    # if s == '滨州':
    #     s = '滨州市'

    if s[-1] == '市':
        s = s[:-1]
    countynames.append(s)
countynames_nodup = list(set(countynames)) #去除重复

data = data.reindex(countynames_nodup) #根据adm_shp的县级市名重命名

colors = {}
cmap1 = LinearSegmentedColormap.from_list('mycmap', ['green', 'white'])  # 定义负值colormap,红白渐变
vmax1 = 0
vmin1 = 0
norm1 = mpl.colors.Normalize(vmin=vmin1, vmax=vmax1)
cmap2 = LinearSegmentedColormap.from_list('mycmap', ['white', 'red'])  # 定义正值colormap,白绿渐变
vmax2 = 1500
vmin2 = 0
norm2 = mpl.colors.Normalize(vmin=vmin2, vmax=vmax2)

#每个值根据正负和正态分布中的给定颜色
for index, value in data.iteritems():
    if value < 0:
        colors[index] = cmap1(np.sqrt((value - vmin1) / (vmax1 - vmin1)))[:3]
    else:
        colors[index] = cmap2(np.sqrt((value - vmin2) / (vmax2 - vmin2)))[:3]

print(colors)
#每个区域绘图
for nshape, seg in enumerate(m.counties):
    color = rgb2hex(colors[countynames[nshape]])
    poly = Polygon(seg, facecolor=color, edgecolor=color)
    ax.add_patch(poly)
plt.title('111', fontproperties=myfont, fontsize=16, y=0.9)

#生产渐变色legend colorbar
cax1 = fig.add_axes([0.18, 0.15, 0.36, 0.01])
cax2 = fig.add_axes([0.54, 0.15, 0.36, 0.01])
comma_fmt = FuncFormatter(lambda x, p: format(int(x), ','))
cb1 = mpl.colorbar.ColorbarBase(cax1, cmap=cmap1, norm=norm1, spacing='proportional', orientation='horizontal', format=comma_fmt)
cb2 = mpl.colorbar.ColorbarBase(cax2, cmap=cmap2, norm=norm2, spacing='proportional', orientation='horizontal', format=comma_fmt)
cb1.set_label('111',x=1, fontproperties=myfont)
# if metric == '销售额净增长':
#     unit_label = '（千元）'
# elif metric == '销售额份额变化':
#     unit_label = '（%）'
cb2.set_label('（%）', fontproperties=myfont, x=1)

#去除图片边框re
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

#保存图片，去掉边缘白色区域，透明
plt.savefig('heatmaps/111.png', format='png', bbox_inches='tight', transparent=True, dpi=600)
print('finished plot')
# with open('bbb.csv', 'w', newline='') as myfile:
#     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#     wr.writerow(countynames_nodup)