# 두 지점의 위경도로 두 지점 사이 거리 구하는 함수
# 코드 출처: https://ko.martech.zone/calculate-great-circle-distance/
from numpy import sin, cos, arccos, pi, round
import pandas as pd
import numpy as np
def rad2deg(radians):
    degrees = radians * 180 / pi
    return degrees

def deg2rad(degrees):
    radians = degrees * pi / 180
    return radians

def getDistanceBetweenPointsNew(latitude1, longitude1, latitude2, longitude2, unit = 'kilometers'):
    
    theta = longitude1 - longitude2
    
    distance = 60 * 1.1515 * rad2deg(
        arccos(
            (sin(deg2rad(latitude1)) * sin(deg2rad(latitude2))) + 
            (cos(deg2rad(latitude1)) * cos(deg2rad(latitude2)) * cos(deg2rad(theta)))
        )
    )
    
    if unit == 'miles':
        return round(distance, 2)
    if unit == 'kilometers':
        return round(distance * 1.609344, 2)


# 비상벨, 유흥업소, 경찰관서, 안심이cctv, 여성 안심 택배함, 여성 안심지킴이집

def calculate_dist_from_any(latitude, longitude, df_any):

    df_dist = pd.DataFrame(
        columns = ['count', 'addr', 'dist','long', 'lat']
    )

    n = 0
    for ind in df_any.index:
        any_lat = df_any['y'][ind]
        any_long = df_any['x'][ind]
        if 'road_addr' in df_any.columns:
            addr = df_any['road_addr'][ind]
        else:
            addr = df_any['address'][ind]

        dist = getDistanceBetweenPointsNew(latitude, longitude, any_lat, any_long, unit = 'kilometers')

        if dist < 1: 
            n += 1
            row = {
                'count': n,
                'addr': addr,
                'dist': dist,
                'long': any_long,
                'lat': any_lat
            }

            df_dist = df_dist.append(row, ignore_index = True)

    return df_dist

df_near = pd.DataFrame(
    columns = ['count','addr','distance','longitude','latitude(y)','type']
)

def calculate_near(row):
    long = row['x']
    lat = row['y']

    df_bell = pd.read_csv('Homey_Backend/dataset/emergency_bell/12_04_09_E_안전비상벨위치정보.csv')  
    df_near_bell =calculate_dist_from_any(lat, long, df_bell)
    df_near_bell['type'] = 'bell'

    df_entertain = pd.read_csv('Homey_Backend\dataset\entertainment_establishments\gwanak_entertainment_establishments_v2.csv')
    df_near_ent = calculate_dist_from_any(lat, long, df_entertain)
    df_near_ent['type'] = 'entertain'

    df_police = pd.read_csv('Homey_Backend\dataset\police_office\preprocessed_police_office_v1.csv')
    df_near_pol = calculate_dist_from_any(lat, long, df_police)
    df_near_pol['type'] ='police'

    df_cctv = pd.read_csv('Homey_Backend\dataset\seoul_ansimee_cctv\preprocessed_Gwanak-gu_cctv_addr.csv')
    df_near_cctv = calculate_dist_from_any(lat, long, df_cctv)
    df_near_cctv['type'] = 'cctv'

    df_wom_prot_house = pd.read_csv('Homey_Backend\dataset\women_protective_house\preprocessed_women_protective_house_v1.csv')
    df_near_prot_house = calculate_dist_from_any(lat, long,  df_wom_prot_house)
    df_near_prot_house['type'] = 'women_protective_house'


    df_wom_prot_parcel = pd.read_csv('Homey_Backend\dataset\women_protective_parcel\preprocessed_women_protective_parcel_v1.csv')
    df_near_prot_parcel = calculate_dist_from_any(lat, long, df_wom_prot_parcel)
    df_near_prot_parcel['type'] = 'women_protective_parcel'

    df_near = pd.concat([df_near_bell,df_near_ent,df_near_pol,df_near_cctv,df_near_prot_house,df_near_prot_parcel], axis = 0, ignore_index= True, )
    #df_near = df_near.append(row, ignore_index = True)
     
    return df_near




df = pd.read_csv('df_sample.csv')
for index, row in df.iterrows():
    df_re2 = calculate_near(row)
    df_re2.to_csv('df_result{}.csv'.format(index))
    #print(df_re2)
#df_re2 = calculate_near(df.iloc[0])
#df_re2.to_csv('df_res2.csv', )
#print(df_re2[:10])