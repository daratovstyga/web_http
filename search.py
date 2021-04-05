import sys
from io import BytesIO
import requests
from PIL import Image
import get_ap
from get_cord import get_cord

ll = get_cord()
org = get_ap.get_ap(ll)[0]

map_params = {
    "ll": ll,
    "l": "map",
    "pt": ll + ',round' + '~' + ','.join(map(str, org[3])) + ',comma'
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
print(f'Адрес: {org[2]}\nНазвание: {org[1]}\nВремя работы: {org[4]}\nРасстояние: {org[0]} м.')
if not response:
    print("Ошибка выполнения запроса:")
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)
else:
   Image.open(BytesIO(response.content)).show()
