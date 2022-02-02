import os
# import sys

import pygame
import requests

coords = ['37.620070', '55.753630']
spn = ['0.1', '0.1']
speed = 0.005

map_api_server = "http://static-maps.yandex.ru/1.x/"

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((500, 650))
# Рисуем картинку, загружаемую из только что созданного файла.


def text_writter(x, y, text):
    font = pygame.font.Font(None, 32)
    text = font.render(text, True, 'GREEN')
    screen.blit(text, (x, y))


if __name__ == '__main__':
    screen.fill('WHITE', rect=(0, 450, 500, 650))
    searchname_rect = pygame.Rect(325, 580, 140, 50)
    name_rect = pygame.Rect(25, 500, 140, 50)
    active = False
    flag = False
    base_font = pygame.font.Font(None, 32)
    search_text = ''
    lon = coords[0]
    lat = coords[1]
    running = True
    while running:
        #screen.fill('WHITE', rect=(0, 450, 500, 650))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if name_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    active = True
                    search_text = search_text[:-1]
                else:
                    if active:
                        search_text += event.unicode
                if event.key == pygame.K_UP and float(coords[1]) < 85:
                    lat = str(float(lat) + speed)
                elif event.key == pygame.K_DOWN and float(coords[1]) > -85:
                    lat = str(float(lat) - speed)
                elif event.key == pygame.K_LEFT and float(coords[0]) < 180:
                    lon = str(float(lon) - speed)
                elif event.key == pygame.K_RIGHT and float(coords[0]) > -180:
                    lon = str(float(lon) + speed)
        screen.fill('WHITE', rect=(0, 450, 500, 650))
        pygame.draw.rect(screen, 'BLACK', searchname_rect)
        pygame.draw.rect(screen, 'BLACK', name_rect)

        text_surface = base_font.render(search_text, True, (255, 255, 255))
        screen.blit(text_surface, (name_rect.x + 5, name_rect.y + 5))
        search_surface = base_font.render('Search', True, (255, 255, 255))
        screen.blit(search_surface, (searchname_rect.x + 5, searchname_rect.y + 5))
        name_rect.w = max(100, text_surface.get_width() + 10)

        if search_text and searchname_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1:
            toponym_to_find = search_text

            geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

            geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": toponym_to_find,
                "format": "json"}

            response = requests.get(geocoder_api_server, params=geocoder_params)

            if not response:
                # обработка ошибочной ситуации
                pass

            # Преобразуем ответ в json-объект
            json_response = response.json()
            # Получаем первый топоним из ответа геокодера.
            toponym = json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]
            # Координаты центра топонима:
            toponym_coodrinates = toponym["Point"]["pos"]
            # Долгота и широта:
            lon, lat = toponym_coodrinates.split(" ")
            coords = [lon, lat]

        coords = [lon, lat]
        map_api_params = {
            "ll": ",".join(coords),
            "spn": ",".join(spn),
            "l": "map",
            "pt": ','.join([coords[0], coords[1], 'pmwtm'])
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
