import sys
from io import BytesIO
import requests
from PIL import Image
from get_cord import get_cord
import get_ap

ll = get_cord()
info = get_ap.get_ap(ll, 10)

rc = ',pm2gnm~'.join([','.join(map(str, org[3])) for org in info if org[4] == 'круглосуточно'])
if rc:
    rc += ',pm2gnm~'

rcn = ',pm2blm~'.join([','.join(map(str, org[3])) for org in info if org[4]])
if rcn:
    rcn += ',pm2blm~'

no_data = ',pm2grm~'.join([','.join(map(str, org[3])) for org in info if org[4] == ''])
if no_data:
    no_data += ',pm2grm'


map_params = {
    "ll": ll,
    "l": "map",
    "pt": rc + rcn + no_data
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
if not response:
    print("Ошибка выполнения запроса:")
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)
else:
   Image.open(BytesIO(response.content)).show()
