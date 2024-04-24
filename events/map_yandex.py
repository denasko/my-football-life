import requests

map = 'https://static-maps.yandex.ru/v1?ll=37.620070,55.753630&lang=ru_RU&size=450,450&z=13&pt=37.620070,55.753630,pmwtm1~37.64,55.76363,pmwtm99&apikey=f42393d0-9fa6-47e9-8d8b-38fae634fe57'
my_map = requests.get(map)
