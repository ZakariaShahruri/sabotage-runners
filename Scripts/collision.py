# Imports
import pygame
from state import State

# Initiliasation of pygame
pygame.init()

left_blocks = [
    (4,254),(4,398),(36,254),(36,398),
    (66,76),(66,108),(66,140),(66,172),
    (66,204),(66,430),(66,462),(66,494),
    (66,526),(66,558),(66,590),
    (68,254),(68,398),(98,12),(98,44),
    (98,642),(98,664),
    (100,254),(100,398),(132,254),(132,398),
    (136,642),(136,664),
    (164,254),(164,398),(196,254),
    (196,398),(136,12),(136,44),
    (337,129),(337,161),(337,193),
    (337,225),(337,257),(337,400),
    (337,432),(337,464),(337,496),
    (337,516),(369,129),(369,516),
    (401,516),(401,129),(433,129),
    (433,516),(465,129),(465,516),
    (497,129),(497,516),(526,129),
    (526,516)
    ]

# Calculate mirrored positions
right_blocks = [(1280-32-x, y) for x, y in left_blocks]

# Combine both lists
map1_borders = left_blocks + right_blocks

def render_border(map, screen):
    borders = []

    for tuple in map:
        x = tuple[0]
        y = tuple[1]
        
        border_block = State(x, y, '../Images/Assets/wall.png', size=32, is_collidable=True)
        border_block.render(screen)
        borders.append(border_block)
    
    return borders
