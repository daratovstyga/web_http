import math
import sys
import requests


def dist(cord1, cord2):
    dx = abs(cord1[0] - cord2[0]) * 111 * 1000 * math.cos(math.radians((cord1[1] + cord2[1]) / 2))
    dy = abs(cord1[1] - cord2[1]) * 111 * 1000
    return int((dx * dx + dy * dy) ** 0.5)


def get_ap(ll, k=1):
    ll_float = list(map(float, ll.split(',')))
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "920e2579-8aef-445d-a34d-ed523688c844"
    search_params = {
        "apikey": api_key,
        "text": "аптека",
        "lang": "ru_RU",
        "ll": ll,
        "type": "biz",
        "results": 100
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    else:
        json_response = response.json()
        list1 = []
        for organization in json_response["features"]:
            org_name = organization["properties"]["CompanyMetaData"]["name"]
            org_address = organization["properties"]["CompanyMetaData"]["address"]
            org_point = organization["geometry"]["coordinates"]
            if 'Hours' in organization['properties']['CompanyMetaData']:
                org_times = organization['properties']['CompanyMetaData']['Hours']['text']
            else:
                org_times = ''

            org_dist = dist(ll_float, org_point)
            list1.append((org_dist, org_name, org_address, org_point, org_times))

        return list(sorted(list1, key=lambda x: (x[0], x[1], x[2], x[3], x[4])))[:k]
