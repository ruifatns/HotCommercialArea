import csv
import geopandas as gpd
import pandas as pd
import requests
import time
from tqdm import tqdm             

hotspot = r"E:\gis\data\Poor_CommercialArea\04_出行平均时间\major_Carea_point\major_Carea_point.shp"
grid_loc = r"E:\gis\data\Poor_CommercialArea\04_出行平均时间\grid_location\data.shp"


def checkdata(p):
    ts = gpd.read_file(p, encoding='utf-8')
    print("字段列表:", ts.columns.tolist())
    print("数据量：", len(ts))
    print(ts[ts.columns.tolist()].head(1))


# 填写自己的高德web key
# key = gaodekey
def gaode(o, d, key):
    try:
        if o != 0:
            response = requests.get(f'https://restapi.amap.com/v3/direction/driving?origin={o}&destination={d}&key={key}')
            result = response.json()['route']['paths'][0]
            time = result['duration']
            return time
        else:
            return 0
    except Exception as e:
        return 0


hp = gpd.read_file(hotspot)
gl = gpd.read_file(grid_loc)
gl[['to农林', 'to北京', 'to西关', 'to珠江', 'to奥体', 'to广州', 'to江南', 'to环市', 'to白鹅', 'to金融', 'to广北', 'to广南']] = 0


# 高德API
for i, j in tqdm(gl.iterrows(), desc='grid_loc'):
    for k in tqdm(range(12), desc='hotspot'):
        time.sleep(0.4)
        o = str(gl.loc[i, 'o_lng']) + ',' + str(gl.loc[i, 'o_lat'])
        d = str(hp.loc[k, 'lng']) + ',' + str(hp.loc[k, 'lat'])
        t = gaode(o, d)
        if hp.loc[k, 'Major_Care'] == '天河路-珠江新城商圈':
            gl.loc[i, 'to珠江'] = t
        if hp.loc[k, 'Major_Care'] == '广州塔-琶洲商圈':
            gl.loc[i, 'to广州'] = t
        if hp.loc[k, 'Major_Care'] == '金融城-黄埔湾商圈':
            gl.loc[i, 'to金融'] = t
        if hp.loc[k, 'Major_Care'] == '白鹅潭商圈':
            gl.loc[i, 'to白鹅'] = t
        if hp.loc[k, 'Major_Care'] == '北京路-海珠广场商圈':
            gl.loc[i, 'to北京'] = t
        if hp.loc[k, 'Major_Care'] == '大西关(上下九-永庆坊)商圈':
            gl.loc[i, 'to西关'] = t
        if hp.loc[k, 'Major_Care'] == '农林下路-中山三路':
            gl.loc[i, 'to农林'] = t
        if hp.loc[k, 'Major_Care'] == '环市东':
            gl.loc[i, 'to环市'] = t
        if hp.loc[k, 'Major_Care'] == '江南西':
            gl.loc[i, 'to江南'] = t
        if hp.loc[k, 'Major_Care'] == '广州大道北':
            gl.loc[i, 'to广北'] = t
        if hp.loc[k, 'Major_Care'] == '广州大道南':
            gl.loc[i, 'to广南'] = t
        if hp.loc[k, 'Major_Care'] == '奥体':
            gl.loc[i, 'to奥体'] = t


# 计算加权出行时间
# '农林下', '北京路', '大西关', '珠江新', '奥体', '广州塔', '江南西', '环市东', '白鹅潭', '金融城', '广州北', '广州南'
gl['avetime'] = 0
for i, j in gl.iterrows():
    t = gl.loc[i, 'total']
    if t != 0:
        c1 = gl.loc[i, '农林下'] / t
        c2 = gl.loc[i, '北京路'] / t
        c3 = gl.loc[i, '大西关'] / t
        c4 = gl.loc[i, '珠江新'] / t
        c5 = gl.loc[i, '奥体'] / t
        c6 = gl.loc[i, '广州塔'] / t
        c7 = gl.loc[i, '江南西'] / t
        c8 = gl.loc[i, '环市东'] / t
        c9 = gl.loc[i, '白鹅潭'] / t
        c10 = gl.loc[i, '金融城'] / t
        c11 = gl.loc[i, '广州北'] / t
        c12 = gl.loc[i, '广州南'] / t
        a1 = int(gl.loc[i, 'to农林'])
        a2 = int(gl.loc[i, 'to北京'])
        a3 = int(gl.loc[i, 'to西关'])
        a4 = int(gl.loc[i, 'to珠江'])
        a5 = int(gl.loc[i, 'to奥体'])
        a6 = int(gl.loc[i, 'to广州'])
        a7 = int(gl.loc[i, 'to江南'])
        a8 = int(gl.loc[i, 'to环市'])
        a9 = int(gl.loc[i, 'to白鹅'])
        a10 = int(gl.loc[i, 'to金融'])
        a11 = int(gl.loc[i, 'to广北'])
        a12 = int(gl.loc[i, 'to广南'])
        gl.loc[i, 'avetime'] = c1*a1 + c2*a2 + c3*a3 + c4*4 + c5*a5 + c6*a6 + c7*a7 + c8*a8 + c9*a9 + c10*a10 + c11*a11 + c12*a12

gl.to_file(r'data\data1.shp')
checkdata(r'data\data1.shp')
