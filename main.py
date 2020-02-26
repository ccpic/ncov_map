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

MYFONT = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc') #准备中文字体，默认英文字体可能出现乱码
D_MAP1 = {
    '阿坝州': '阿坝藏族羌族自治州',
    '阿克苏': '阿克苏地区',
    '安阳市': '安阳',
    '巴州': '巴彦卓尔蒙古自治州',
    '白银市': '白银',
    '包头市东河区': '包头',
    '昌平': '北京',
    '昌平区': '北京',
    '朝阳': '北京',
    '朝阳区': '北京',
    '大兴': '北京',
    '大兴区': '北京',
    '待明确地区': '北京',
    '东城': '北京',
    '东城区': '北京',
    '房山区': '北京',
    '丰台': '北京',
    '丰台区': '北京',
    '海淀': '北京',
    '海淀区': '北京',
    '怀柔区': '北京',
    '门头沟': '北京',
    '门头沟区': '北京',
    '密云区': '北京',
    '石景山': '北京',
    '石景山区': '北京',
    '顺义': '北京',
    '顺义区': '北京',
    '通州': '北京',
    '通州区': '北京',
    '外地来京人员': '北京',
    '未明确地区': '北京',
    '西城': '北京',
    '西城区': '北京',
    '延庆区': '北京',
    '毕节': '毕节地区',
    '昌吉': '昌吉回族自治州',
    '昌吉州': '昌吉回族自治州',
    '赤峰市松山区': '赤峰',
    '楚雄': '楚雄彝族自治州',
    '楚雄州': '楚雄彝族自治州',
    '大理': '大理白族自治州',
    '大理州': '大理白族自治州',
    '大兴安岭': '大兴安岭地区',
    '德宏': '德宏傣族景颇族自治州',
    '德宏州': '德宏傣族景颇族自治州',
    '鄂尔多斯东胜区': '鄂尔多斯',
    '鄂尔多斯鄂托克前旗': '鄂尔多斯',
    '恩施州': '恩施土家族苗族自治州',
    '甘南': '甘南藏族自治州',
    '甘孜州': '甘孜藏族自治州',
    '海北州': '海北藏族自治州',
    '邯郸市': '邯郸',
    '鹤壁市': '鹤壁',
    '红河': '红河哈尼族彝族自治州',
    '红河州': '红河哈尼族彝族自治州',
    '呼伦贝尔满洲里': '呼伦贝尔',
    '呼伦贝尔牙克石': '呼伦贝尔',
    '呼伦贝尔牙克石市': '呼伦贝尔',
    '吉林市': '吉林',
    '金昌市': '金昌',
    '丽江市': '丽江',
    '凉山': '凉山彝族自治州',
    '凉山州': '凉山彝族自治州',
    '临夏': '临夏回族自治州',
    '漯河市': '漯河',
    '平凉市': '平凉',
    '黔东南州': '黔东南苗族侗族自治州',
    '黔南州': '黔南布依族苗族自治州',
    '黔西南州': '黔西南布依族苗族自治州',
    '宝山区': '上海',
    '崇明区': '上海',
    '奉贤区': '上海',
    '虹口区': '上海',
    '黄浦区': '上海',
    '嘉定区': '上海',
    '金山': '上海',
    '金山区': '上海',
    '静安区': '上海',
    '闵行区': '上海',
    '浦东新区': '上海',
    '普陀区': '上海',
    '青浦区': '上海',
    '松江': '上海',
    '松江区': '上海',
    '外地来沪人员': '上海',
    '未知地区': '上海',
    '徐汇区': '上海',
    '杨浦': '上海',
    '杨浦区': '上海',
    '长宁区': '上海',
    '兵团第八师石河子市': '石河子',
    '兵团第七师': '石河子',
    '第八师': '石河子',
    '第八师石河子': '石河子',
    '第八师石河子市': '石河子',
    '胡杨河': '石河子',
    '石河子': '石河子',
    '公主岭': '四平',
    '四平市': '四平',
    '兵团第九师': '塔城地区',
    '第九师': '塔城地区',
    '塔城': '塔城地区',
    '宝坻区': '天津',
    '北辰区': '天津',
    '滨海新区': '天津',
    '待明确': '天津',
    '东丽区': '天津',
    '和平区': '天津',
    '河北区': '天津',
    '河东区': '天津',
    '河西区': '天津',
    '红桥区': '天津',
    '津南区': '天津',
    '南开区': '天津',
    '宁河区': '天津',
    '外地来津': '天津',
    '外地来津人员': '天津',
    '武清区': '天津',
    '西青区': '天津',
    '天水市': '天水',
    '梅河口': '通化',
    '通辽市经济开发区': '通辽',
    '铜仁': '铜仁地区',
    '吐鲁番': '吐鲁番地区',
    '吐鲁番市': '吐鲁番地区',
    '文山': '文山壮族苗族自治州',
    '文山州': '文山壮族苗族自治州',
    '乌海市': '乌海',
    '兵团第六师五家渠市': '乌鲁木齐',
    '兵团第十二师': '乌鲁木齐',
    '第六师': '乌鲁木齐',
    '第七师': '乌鲁木齐',
    '五家渠': '乌鲁木齐',
    '西双版纳': '西双版纳傣族自治州',
    '西双版纳州': '西双版纳傣族自治州',
    '锡林郭勒': '锡林郭勒盟',
    '锡林郭勒盟二连浩特': '锡林郭勒盟',
    '锡林郭勒盟锡林浩特': '锡林郭勒盟',
    '兴安盟乌兰浩特': '兴安盟',
    '延边': '延边朝鲜族自治州',
    '兵团第四师': '伊犁哈萨克自治州',
    '伊犁州': '伊犁哈萨克自治州',
    '宁东管委会': '银川',
    '巴南区': '重庆',
    '璧山区': '重庆',
    '城口县': '重庆',
    '大渡口区': '重庆',
    '大足区': '重庆',
    '垫江县': '重庆',
    '丰都县': '重庆',
    '奉节县': '重庆',
    '涪陵区': '重庆',
    '高新区': '重庆',
    '合川区': '重庆',
    '江北区': '重庆',
    '江津区': '重庆',
    '九龙坡区': '重庆',
    '开州区': '重庆',
    '梁平区': '重庆',
    '两江新区': '重庆',
    '南岸区': '重庆',
    '彭水县': '重庆',
    '綦江区': '重庆',
    '黔江区': '重庆',
    '荣昌区': '重庆',
    '沙坪坝区': '重庆',
    '石柱县': '重庆',
    '铜梁区': '重庆',
    '潼南区': '重庆',
    '万盛经开区': '重庆',
    '万州区': '重庆',
    '巫山县': '重庆',
    '巫溪县': '重庆',
    '武隆区': '重庆',
    '秀山县': '重庆',
    '永川区': '重庆',
    '酉阳': '重庆',
    '酉阳县': '重庆',
    '渝北区': '重庆',
    '渝中区': '重庆',
    '云阳县': '重庆',
    '长寿区': '重庆',
    '忠县': '重庆',
    '淄博市': '淄博',
    '万宁': '海南',
    '临高县': '海南',
    '儋州': '海南',
    '陵水县': '海南',
    '澄迈县': '海南',
    '琼海市': '海南',
    '东方市': '海南',
    '琼中县': '海南',
    '琼海': '海南',
    '陵水': '海南',
    '澄迈': '海南',
    '临高': '海南',
    '东方': '海南',
    '琼中': '海南',
    '定安': '海南',
    '昌江': '海南',
    '乐东': '海南',
    '文昌': '海南',
}

path = 'ncov_area.csv'
df = pd.read_csv(path, encoding='UTF-8') # 读取数据文件到pandas
df['市'] = df['市'].map(D_MAP1).fillna(df['市'])  # 根据手动准备的字典清洗命名不规范的名称
pivoted = pd.pivot_table(df, index='市', values='新增确诊', aggfunc=sum) #汇总为数据透视表，行为地级市，值为新增确诊

data = pivoted['新增确诊']

fig, ax = plt.subplots(figsize=(9, 8))

m = Basemap(llcrnrlon=77, llcrnrlat=14, urcrnrlon=140, urcrnrlat=51, projection='lcc', lat_1=33, lat_2=45, lon_0=100) #中国地图为投影主体
m.readshapefile('CHN_adm_shp/CHN_adm1', 'states', drawbounds=True) # 绘制省级行政区轮廓
m.readshapefile('CHN_adm_shp/CHN_adm2', 'counties', drawbounds=False) # 绘制地级市，但不包含轮廓
m.readshapefile('TWN_adm_shp/TWN_adm0', 'taiwan', drawbounds=True)  # 政治正确，增加台湾

countynames = []
for shapedict in m.counties_info:

    # 提取地级市矢量图的所有名称
    countyname = shapedict['NL_NAME_2']

    # 有些城市有1个以上的别名，取最后那个
    p = countyname.split('|')
    if len(p) > 1:
        s = p[1]
    else:
        s = p[0]

    # 城市名称还需要一些手动调整
    D_NAP2 = {
        # 撤并/代管的县市
        '巢湖市': '合肥市',
        '天门市': '武汉市',
        '潜江市': '武汉市',
        '仙桃市': '武汉市',
        '济源市': '焦作市',
        '莱芜市': '济南市',
        # 繁体字导致的不匹配
        '益陽市': '益阳市',
        '邵陽市': '邵阳市',
        '衡陽市': '衡阳市',
        '岳陽市': '岳阳市',
        '張家界市': '张家界市',
        '長沙市': '长沙市',
        '懷化市': '怀化市',
        '婁底市': '娄底市',
        #县升格为市
        '运城县': '运城市',
        #别名
        '巴音郭愣蒙古自治州': '巴彦卓尔蒙古自治州',
        #改名
        '襄樊市': '襄阳市'
    }
    if s in D_NAP2.keys():
        s = D_NAP2[s]

    # Ncov数据不带“市”，为了匹配这里也删除
    if s[-1] == '市':
        s = s[:-1]

    countynames.append(s)

countynames_nodup = list(set(countynames)) #去除重复

data = data.reindex(countynames_nodup) #根据adm_shp的县级市名重命名

cmap1 = LinearSegmentedColormap.from_list('mycmap', ['green', 'white'])  # 定义负值colormap,绿白渐变
vmax1 = 0
vmin1 = min(data)
norm1 = mpl.colors.Normalize(vmin=vmin1, vmax=vmax1) #正态分布
cmap2 = LinearSegmentedColormap.from_list('mycmap', ['white', 'red'])  # 定义正值colormap,白红渐变
vmax2 = 2000 # 累计确诊书阈值，高于1500都为最深红色
vmin2 = 0
norm2 = mpl.colors.Normalize(vmin=vmin2, vmax=vmax2)

#每个值根据正负和正态分布中的给定颜色
colors = {}
for index, value in data.iteritems():
    if value < 0:
        colors[index] = cmap1(np.sqrt((value - vmin1) / (vmax1 - vmin1)))[:3]
    else:
        colors[index] = cmap2(np.sqrt((value - vmin2) / (vmax2 - vmin2)))[:3]


#遍历每个地级市区域绘图
for nshape, seg in enumerate(m.counties):
    color = rgb2hex(colors[countynames[nshape]]) # 颜色格式由RGB转为16位HEX
    poly = Polygon(seg, facecolor=color, edgecolor=color) # 绘制带有颜色的地级市多边形
    ax.add_patch(poly) # 将绘制多边形添加到画布上
plt.title('COVID-19累计确诊人数疫情地图\n（截至2月23日）', fontproperties=MYFONT, fontsize=16, y=0.9)

#生产渐变色legend colorbar
# cax1 = fig.add_axes([0.18, 0.15, 0.36, 0.01])
cax2 = fig.add_axes([0.18, 0.15, 0.36, 0.01])
comma_fmt = FuncFormatter(lambda x, p: format(int(x), ',')) #colorbar数字加上千位符
# cb1 = mpl.colorbar.ColorbarBase(cax1, cmap=cmap1, norm=norm1, spacing='proportional', orientation='horizontal', format=comma_fmt)
cb2 = mpl.colorbar.ColorbarBase(cax2, cmap=cmap2, norm=norm2, spacing='proportional', orientation='horizontal', format=comma_fmt)
cb2.set_label('累计确诊病人',x=1, fontproperties=MYFONT)
# if metric == '销售额净增长':
#     unit_label = '（千元）'
# elif metric == '销售额份额变化':
#     unit_label = '（%）'
# cb2.set_label('（%）', fontproperties=MYFONT, x=1)

#去除图片边框re
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

#保存图片，去掉边缘白色区域，透明
plt.savefig('heatmaps/COVID_19_map_0223.png', format='png', bbox_inches='tight', transparent=True, dpi=600)
print('finished plot')