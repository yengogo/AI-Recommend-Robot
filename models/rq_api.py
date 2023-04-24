import requests
import json
from utils.token import Token
from liontk.sql.pgsql import PGSQLMgr
from liontk.enum.pgsql import PGSQL
import random

s_token = Token()
token = s_token.get_token()


def weather_api(data, idx, tourid):

    if tourid == '21TSKHH001':
        api_url = f"http://10.35.2.42/api/pic/weather?lng={data['Lng']}&lat={data['Lat']}"
    elif tourid == '21TWIELA01':
        api_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={data['Lat']}&lon={data['Lng']}&appid=9164d5c98ffcf6e3171c0a6f9d89e4b5"
    else:
        citys = ["高雄市", "台中市", "新北市", "基隆市", "台東縣"]
        api_url = f"http://10.1.1.181/other/api/weather/city/?City={random.choices(citys)}&ElementName=MaxT,MinT,Wx,PoP24h"
    # api_url = f"http://10.1.1.181/other/api/weather/latlon/?Lng={data['Lng']}&Lat={data['Lat']}&ElementName=MaxT,MinT,Wx,PoP24h"
    res = requests.get(api_url)
    result = json.loads(res.text)

    if tourid == '21TWIELA01':
        arr = []
        for w in range(len(result["list"])):
            rain = result["list"][w]['rain']['3h'] if result["list"][w].get('rain') is not None else 0
            if '12:00:00' in result["list"][w]['dt_txt']: 
                tmp = {
                    # "time": result["list"][w]['dt_txt'],
                    "temp_min": int(result["list"][w]['main']['temp_min'] - 273.15),
                    "temp_max": int(result["list"][w]['main']['temp_max'] - 273.15),
                    "desc": result["list"][w]['weather'][0]['description'],
                    "rain_rate": rain
                }
                arr.append(tmp)
        tmp = {
            'location': result["city"]['name'],
            'weather': [
                arr[idx]['temp_max'],
                arr[idx]['temp_min'],
                arr[idx]['desc'],
                str(arr[idx]['rain_rate']),
            ],
        }
        return tmp
    else:
        tmp = []
        for ele in result['Data'][0]['weather']:
            tmp.append(ele['time'][idx + 1]['elementValue'][0]['value'])

        return {"weather": tmp, "location": result['Data'][0]['location'][:3]}


def product_api(group_id):

    api_url = f'http://10.35.2.42/api/pic/product?_id={group_id}'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    res = requests.get(api_url, headers=headers)
    # res = requests.get(api_url)
    prod_info = json.loads(res.text)

    # try:
    #     pg_mgr = PGSQLMgr.get_mgr(PGSQL.DEV_DS)
    #     sql_str = f"SELECT jsonb_object_keys(labels) FROM grp_tourid_labels WHERE tourid = '{prod_info['Data']['results'][0]['plist'][0]['TOUR_ID']}';"
    #     result = list(pg_mgr.query(sql_str, to_dict=True))

    # except Exception as e:
    #     print(e)

    # finally:
    #     pg_mgr.close()

    return prod_info['Data']['results'][0]['plist'][0]


def similar_api(text):

    api_url = f'http://10.35.2.42/api/pic/similar?_id={text}'

    # res = requests.get(api_url, headers=headers)
    res = requests.get(api_url)
    if res.status_code == 200:
        result = json.loads(res.text)

        return result
