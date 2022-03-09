from _csv import reader
import pygame
from objects import ENEMY
from pygame.sprite import Group

def read(surface, screen, level):
    game_map = []
    data = 0
    enemies = Group()
    loc = open("Enemy_location", 'r')
    position = reader(loc, delimiter=' ')
    line = 0
    level_lines = []
    coords = []
    for row in position:
        line +=1
        if row == ['level1'] or row == ['level2']:
            level_lines.append(line)
        else:
            coords.append(row)
    if level == 1:
        data = open("карта1.csv", 'r')
        enemy1 = ENEMY(screen, float(coords[0][0]), float(coords[0][1]), 1,pygame.image.load('images/красный.png').convert_alpha())
        enemy2 = ENEMY(screen, float(coords[1][0]), float(coords[1][1]), 1,pygame.image.load('images/красный.png').convert_alpha())
        enemy3 = ENEMY(screen, float(coords[2][0]), float(coords[2][1]), 1,pygame.image.load('images/красный.png').convert_alpha())
        enemy4 = ENEMY(screen, float(coords[3][0]), float(coords[3][1]), 1,pygame.image.load('images/красный.png').convert_alpha())
        enemy5 = ENEMY(screen, float(coords[4][0]), float(coords[4][1]), 1,pygame.image.load('images/красный.png').convert_alpha())
    elif level == 2:
        data = open("карта2.csv", 'r')
        enemy1 = ENEMY(screen, float(coords[5][0]), float(coords[0][1]), 1,pygame.image.load('images/красный.png').convert_alpha())
        enemy2 = ENEMY(screen, float(coords[6][0]), float(coords[1][1]), 1,pygame.image.load('images/красный.png').convert_alpha())
        enemy3 = ENEMY(screen, float(coords[7][0]), float(coords[2][1]), 1,pygame.image.load('images/красный.png').convert_alpha())
        enemy4 = ENEMY(screen, float(coords[8][0]), float(coords[3][1]), 1,pygame.image.load('images/красный.png').convert_alpha())
        enemy5 = ENEMY(screen, float(coords[9][0]), float(coords[4][1]), 1,pygame.image.load('images/красный.png').convert_alpha())
    enemies.add(enemy1)
    enemies.add(enemy2)
    enemies.add(enemy3)
    enemies.add(enemy4)
    enemies.add(enemy5)
    a = reader(data, delimiter = ',')
    for row in a:
        game_map.append(list(row))
    TILE_SIZE =100
    tile_rects = []
    y = 0
    wall = '0'
    floor = '-1'
    for row in game_map:
        x = 0
        for tile in row:
            if tile == wall:
                surface.blit(pygame.image.load('images/камни.png'), (x * TILE_SIZE, y * TILE_SIZE))
            if tile == floor:
                surface.blit(pygame.image.load('images/магма.png'), (x * TILE_SIZE, y * TILE_SIZE))
            if tile != floor:
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1
    return tile_rects, enemies
