# Imports of other scripts/logics
import pygame
from state import State

# Initiliasation of pygame
pygame.init()

# Tile settings
tilesize = 32

# Tilemaps
tilemap_1 = [
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    '.............W............W.............',
    '.............W............W.............',
    '.............W............W.............',
    '.............W............W.............',
    '.............W............W.............',
    '.............W............W.............',
    '...........WWW....SSSS....WWW...........',
    '..................SSSS..................',
    '..................WWWW..................',
    '.....................W..................',
    '.....................W..................',
    '..................SSSW..................',
    '..................SSSW..................',
    '..................WWWW..................',
    '........................................',
    '...........WWW............WWW...........',
    '.............W............W.............',
    '.............W............W.............',
    '.............W............W.............',
    'SSSSSSSSSSSSSWSSSSSSSSSSSSWSSSSSSSSSSSSS',
    'SSSSSSSSSSSSSWSSSSSSSSSSSSWSSSSSSSSSSSSS',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
]

tilemap_2 = [
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    '........................................',
    '........................................',
    '........................................',
    '........................................',
    '........................................',
    '........................................',
    '........................................',
    '........................................',
    'SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS',
    'SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    '........................................',
    '........................................',
    '........................................',
    '........................................',
    '........................................',
    '........................................',
    '........................................',
    '........................................',
    'SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS',
    'SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
]

def draw_map(tilemap, image, screen):
    walls = []

    for y, row in enumerate(tilemap):
        for x, tile in enumerate(row):
            if tile == 'W':
                wall = State(x * tilesize, y * tilesize, image, size=tilesize, is_collidable=True)
                walls.append(wall)

                wall.render(screen)
            
            if tile == 'S':
                wall = State(x * tilesize, y * tilesize, '../Images/Assets/wall.png', size=tilesize, is_collidable=True)
                walls.append(wall)
    
    return walls