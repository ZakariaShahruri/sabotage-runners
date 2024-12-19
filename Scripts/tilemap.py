# Imports of other scripts/logics
import pygame
from state import State

# Initiliasation of pygame
pygame.init()

# Tile settings
tilesize = 32

# Tilemaps
tilemap_1 = [
    'SSSWW..............................WWSSS',
    'SSSWW..............................WWSSS',
    'SSS..................................SSS',
    'SSS..................................SSS',
    'SSS.......WWWWWWW.....WWWWWWWW.......SSS',
    'SSS.......WW................WW.......SSS',
    'SSS.......WW................WW.......SSS',
    'SSSHHHH...WW................WW...HHHHSSS',
    'WWWWWWW...WW................WW...WWWWWWW',
    '.................SSSSS..................',
    '.................SSSSS..................',
    '.................SSSSS.................',
    '..........WW................WW..........',
    'SSSWWWW...WW................WW...WWWWSSS',
    'SSS.......WW................WW.......SSS',
    'SSS.......WW................WW.......SSS',
    'SSS.......WWWWWWW.....WWWWWWWW.......SSS',
    'SSS..................................SSS',
    'SSS..................................SSS',
    'SSS..................................SSS',
    'SSSWW..............................WWSSS',
    'SSSWW..............................WWSSS',
    'SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS',
]

# drawing the map
def draw_map(tilemap, image, screen):
    walls = []

    for y, row in enumerate(tilemap):
        for x, tile in enumerate(row):
            if tile == 'W':
                wall = State(x * tilesize, y * tilesize, image, size=tilesize, is_collidable=True)
                walls.append(wall)

                # wall.render(screen)
            
            if tile == 'S':
                wall = State(x * tilesize, y * tilesize, '../Images/Assets/wall.png', size=tilesize, is_collidable=True)
                walls.append(wall)

                # wall.render(screen)
    
    return walls