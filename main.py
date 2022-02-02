import os
#import sys

import pygame
import requests

coords = ['37.620070', '55.753630']
spn = ['0.1', '0.1']
speed = 0.005

map_api_server = "http://static-maps.yandex.ru/1.x/"

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((500, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
if __name__ == '__main__':
    lon = coords[0]
    lat = coords[1]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and float(coords[1]) < 85:
                    lat = str(float(lat) + speed)
                elif event.key == pygame.K_DOWN and float(coords[1]) > -85:
                    lat = str(float(lat) - speed)
                elif event.key == pygame.K_LEFT and float(coords[0]) < 180:
                    lon = str(float(lon) - speed)
                elif event.key == pygame.K_RIGHT and float(coords[0]) > -180:
                    lon = str(float(lon) + speed)

        coords = [lon, lat]

        map_api_params = {
            "ll": ",".join(coords),
            "spn": ",".join(spn),
            "l": "map"
        }
        response = requests.get(map_api_server, params=map_api_params)
        if not response:
            pass

        # Запишем полученное изображение в файл.
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        screen.blit(pygame.image.load(map_file), (0, 0))
        # Переключаем экран и ждем закрытия окна.
        pygame.display.flip()
    os.remove(map_file)
