import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Polygon
from matplotlib.colors import rgb2hex
import numpy as np
from matplotlib.ticker import FuncFormatter
import matplotlib.font_manager as fm
from matplotlib import gridspec
from data import *

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
MYFONT = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc') #准备中文字体，默认英文字体可能出现乱码

path = 'ncov_area.csv'
df = pd.read_csv(path, encoding='UTF-8')  # 读取数据文件到pandas
df = df[~df['省'].isin(['台湾省', '澳门'])]
mask = df['省'] == '新疆维吾尔自治区'
df.loc[mask, '省'] = '新疆维吾尔族自治区'
mask = df['省'] == '内蒙古自治区'
df.loc[mask, '省'] = '内蒙古蒙古族自治区'
mask = df['省'] == '西藏自治区'
df.loc[mask, '省'] = '西藏藏族自治区'


def plot_province(df, date, provc, prove, fig_width=16, fig_height=9, width_ratios=[2, 1],
                  llcrnrlon=77, llcrnrlat=14, urcnlon=140, urcrnrlat=51):
    df = df[df['省'] == provc]

    # 准备画布
    fig = plt.figure(figsize=(fig_width, fig_height))
    gs = gridspec.GridSpec(1, 2, width_ratios=width_ratios) # 准备grid，画布分为左右两侧，左侧为右侧宽度的2.7倍

    # 准备左侧画布
    ax0 = plt.subplot(gs[0])

    # 准备地图投影并读取矢量文件数据
    m = Basemap(llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcnlon, urcrnrlat=urcrnrlat, projection='lcc', lat_1=33, lat_2=45,
                lon_0=120)  # 中国地图为投影主体
    m.readshapefile('CHN_adm_shp/CHN_adm1', 'states', drawbounds=True)  # 绘制省级行政区轮廓
    m.readshapefile('CHN_adm_shp/CHN_adm2', 'counties', drawbounds=False)  # 绘制地级市，但不包含轮廓
    m.readshapefile('TWN_adm_shp/TWN_adm0', 'taiwan', drawbounds=True)  # 政治正确，增加台湾

    data = get_data(df, basemap=m, level='市', prov=prove)
    colormap =get_colormap(data, vmax_pos=2000)

    # 遍历每个地级市区域绘图
    for info, seg in zip(m.counties_info, m.counties):
        prov_id = info['NAME_1']
        if prove == prov_id:
            if info['NL_NAME_2'][-1] == '市':
                county = info['NL_NAME_2'][:-1]
            else:
                county = info['NL_NAME_2']
            if county == '巢湖':
                color = rgb2hex(colormap[0]['合肥'])
            else:
                color = rgb2hex(colormap[0][county]) # 颜色格式由RGB转为16位HEX
            poly = Polygon(seg, facecolor=color, edgecolor=color) # 绘制带有颜色的地级市多边形
            ax0.add_patch(poly) # 将绘制多边形添加到画布上

    # # 生产渐变色legend colorbar
    # # cax1 = fig.add_axes([0.18, 0.15, 0.36, 0.01])
    # cax2 = fig.add_axes([0.18, 0.1, 0.45, 0.01])
    # comma_fmt = FuncFormatter(lambda x, p: format(int(x), ',')) #colorbar数字加上千位符
    # # cb1 = mpl.colorbar.ColorbarBase(cax1, cmap=cmap1, norm=norm1, spacing='proportional', orientation='horizontal', format=comma_fmt)
    # cb2 = mpl.colorbar.ColorbarBase(cax2, cmap=colormap[2], norm=colormap[4], spacing='proportional', orientation='horizontal', format=comma_fmt)
    # cb2.set_label('累计确诊病例数', x=1, y=1, fontproperties=MYFONT)
    # # if metric == '销售额净增长':
    # #     unit_label = '（千元）'
    # # elif metric == '销售额份额变化':
    # #     unit_label = '（%）'
    # # cb2.set_label('（%）', fontproperties=MYFONT, x=1)

    #去除图片边框
    # ax0.axis('off')

    # 准备右侧画布
    ax1 = plt.subplot(gs[1])

    # 准备表格内容
    data_raw = get_data(df, basemap='level', level='市', raw=True)
    data_raw = data_raw.sort_values(ascending=False)
    data_prop = ['{:.1%}'.format(x/sum(data_raw)) for x in data_raw]

    cell_text = list(zip(data_raw, data_prop))
    column_labels = ['累计确诊', '全省占比']
    row_labels = data_raw.index

    # 每个值根据正负和正态分布中的给定颜色
    colors_province = list(get_colormap(data_raw, vmax_pos=2000)[0].values())

    # 在右侧画布生成表格
    table = ax1.table(cellText=cell_text,
                         rowLabels=row_labels,
                         colLabels=column_labels,
                         rowColours=colors_province,
                         bbox=[0.0, 0.0, 0.8, 1.0])
    table.auto_set_font_size(False) # 手动设置表格字体大小前必须有这句
    table.set_fontsize(11)

    # 去除图片边框
    ax1.axis('off')

    # 标题
    st = fig.suptitle('COVID-19'+ provc +'累计确诊人数疫情地图（截至'+ '%s月%s日' % (date[2], date[2:]) + '）', fontproperties=MYFONT, fontsize=24, y=0.95)

    # 保存图片，去掉边缘白色区域，透明
    plt.savefig('heatmaps/COVID_19_map_table_' + date + '_' + prove + '.png', format='png', bbox_inches='tight', transparent=True, dpi=600)
    print('finished plot')


if __name__ == "__main__":
    plot_province(df=df, date='0229', provc='甘肃省', prove='Gansu', width_ratios=[3, 1], llcrnrlon=95, llcrnrlat=30, urcnlon=108, urcrnrlat=45)
