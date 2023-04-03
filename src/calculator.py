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

# 비상벨
def calculate_dist_from_any(latitude, longitude, df_any):

    df_dist = pd.DataFrame(
        columns = ['road_addr', 'lat','long','dist']
    )

    for ind in df_any.index:
        any_lat = df_any['y'][ind]
        any_long = df_any['x'][ind]
        dist = getDistanceBetweenPointsNew(latitude, longitude, any_lat, any_long, unit = 'kilometers')
        row = {
            df_any['road_addr'],
            any_lat,
            any_long,
            dist
        }

        df_dist = df_dist.append(row, ignore_index = True)

    return df_dist
    
#해당 지점으로부터 반경 3km 이내 있는 안심벨 수와 위치 구하기
def calculate_any(latitude, longitude, df_any):

    df_dist = calculate_dist_from_any(latitude, longitude, df_any)

    df_dist = df_dist.sort_values('dist')

    n = 0

    df_near = pd.DataFrame(
    columns= ['road_addr', #도로명주소
              'addr',  #지번주소
              'dist' #해당 지점으로부터 안심벨까지 거리
              ]
    )

    for ind in df_dist.index:
        if df_dist['distance'][ind] < 1:
            n += 1
            row = {
                df_dist['any_road_addr'], 
                df_dist['dist'],
                df_dist['any_lat'], 
                df_dist['any_long']
            }
    
    return n, df_near

df_near = pd.DataFrame(
    columns = ['emergency_bell', 'entertainment_establishments', 'police_office', 'cctv', 'women_protective_house', 'women_protective_parcel']
)

def calculate_near(df):
    long = df['x']
    lat = df['y']

    df_bell = pd.read_csv('Homey_Backend/dataset/emergency_bell/12_04_09_E_안전비상벨위치정보.csv')
    
    a, df_near_bell =calculate_any(lat, long, df_bell)

    df_enterain = pd.read_csv('Homey_Backend/dataset/emergency_bell/gwanak_entertainment_establishments_v2.csv')

    b, df_near_ent = calculate_any(lat, long, df_enterain)

    df_police = pd.read_csv('Homey_Backend/dataset/police_office/preprocessed_police_office_v1')

    c, df_near_pol = calculate_any(lat, long, df_police)

    df_cctv = pd.read_csv('Homey-Backend\Homey_Backend\dataset\seoul_ansimee_cctv\preprocessed_Gwanak-gu_cctv_addr.csv')

    d, df_near_cctv = calculate_any(lat, long, df_cctv)

    df_wom_prot_house = pd.read_csv('Homey_Backend\dataset\women_protective_house\preprocessed_women_protective_house_v1.csv')

    e, df_near_prot_house = calculate_any(lat, long, df_cctv)
    
    df_wom_prot_parcel = pd.read_csv('Homey_Backend\dataset\women_protective_parcel\preprocessed_women_protective_parcel_v1.csv')

    f, df_near_prot_parcel = calculate_any(lat, long, df_cctv)

    row = {
        a, b, c, d, e, f
    }

    df_near = df_near.append(row, ignore_index = True)

    return df_near


