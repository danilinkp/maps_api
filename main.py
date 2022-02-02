import os
import sys

import pygame
import requests

coords = ['37.620070', '55.753630']
spn = ['0.1', '0.1']

map_api_server = "http://static-maps.yandex.ru/1.x/"

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

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((500, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
