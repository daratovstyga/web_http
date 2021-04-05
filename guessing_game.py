import os
import sys
import random
import pygame
import requests
from get_cord_new import get_cord

map_files = []
cities = ['Москва', 'Курган', 'Санкт-Петербург', 'Владивосток', 'Калининград']
pos = [get_cord(i) for i in cities]

for i in range(len(pos)):
    map_params = {"ll": pos[i][0],
                  "spn": pos[i][1],
                  "size": '600,450',
                  "l": random.choice(["map", "sat"])}
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    else:
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        map_files.append(pygame.image.load(map_file))
        os.remove(map_file)

i = 0
random.shuffle(map_files)
pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(map_files[i], (0, 0))
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            i = (i + 1) % len(map_files)
    screen.blit(map_files[i], (0, 0))
    pygame.display.flip()
pygame.quit()
