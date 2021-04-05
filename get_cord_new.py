import sys
import requests


def optimal_spn(toponym):
    to = toponym["boundedBy"]["Envelope"]
    lc = list(map(float, to["lowerCorner"].split()))
    uc = list(map(float, to["upperCorner"].split()))
    spn = ','.join([str(abs(uc[0] - lc[0]) / 50), str(abs(uc[1] - lc[1]) / 50)])
    return spn


def get_cord(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    else:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        spn = optimal_spn(toponym)
        return (','.join(toponym['Point']['pos'].split()), spn)
