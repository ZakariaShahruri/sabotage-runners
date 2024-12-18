# Imports of other scripts/logics
import pygame
from state import State

# Initiliasation of pygame
pygame.init()

# Tile settings
tilesize = 32

# Tilemaps
tilemap_1 = [
    'FFFFFFFFFFFFWFFFFFFFFFFFFFFWFFFFFFFFFFFF',
    '............W..............W............',
    '............W..............W............',
    '........................................',
    '........................................',
    '.....SSSSSSSSS............SSSSSSSSS.....',
    '.....WWWWWWWWW............WWWWWWWWW.....',
    '........W......................W........',
    '........W......................W........',
    '........W.....S..........S.....W........',
    '..............W....SS....W..............',
    '..............W....WW....W..............',
    '..............W....WW....W..............',
    '..............W....WW....W..............',
    '..........S...W..........W...S..........',
    '..........W..................W..........',
    '..........W..................W..........',
    '..........W..................W..........',
    '..........W..................W..........',
    '..........W..................W..........',
    'SSSSSSSSSSWSSSSSSSSSSSSSSSSSSWSSSSSSSSSS',
    'SSSSSSSSSSWSSSSSSSSSSSSSSSSSSWSSSSSSSSSS',
    'FFFFFFFFFFWFFFFFFFFFFFFFFFFFFWFFFFFFFFFF',
]

tilemap_2 = [
    'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF',
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
    'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF',
]

# drawing the map
def draw_map(tilemap, image, screen):
    walls = []

    for y, row in enumerate(tilemap):
        for x, tile in enumerate(row):
            if tile == 'F':
                wall = State(x * tilesize, y * tilesize, '../Images/Assets/fence.png', size=tilesize, is_collidable=True)
                walls.append(wall)

                wall.render(screen)
            
            if tile == 'W':
                wall = State(x * tilesize, y * tilesize, image, size=tilesize, is_collidable=True)
                walls.append(wall)

                wall.render(screen)
            
            if tile == 'S':
                wall = State(x * tilesize, y * tilesize, '../Images/Assets/wall.png', size=tilesize, is_collidable=True)
                walls.append(wall)
    
    return walls