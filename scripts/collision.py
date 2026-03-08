import pygame
from state import State

# Raw coordinate data
left_blocks1 = [
    (4,254),(4,398),(36,254),(36,398), (66,76),(66,108),(66,140),(66,172),
    (66,204),(66,430),(66,462),(66,494), (66,526),(66,558),(66,590),(68,254),
    (68,398),(98,12),(98,44),(98,642), (98,664),(100,254),(100,398),
    (132,254),(132,398),(136,642), (136,664),(164,254),(164,398),
    (196,254),(196,398),(136,12), (136,44),(337,129),(337,161),
    (337,193),(337,225),(337,257), (337,400),(337,432),(337,464),
    (337,496),(337,516),(369,129), (369,516),(401,516),(401,129),
    (433,129),(433,516),(465,129), (465,516),(497,129),(497,516),
    (526,129),(526,516),(164,700), (196,700),(228,700),(260,700),
    (292,700),(324,700),(356,700), (388,700),(420,700),(452,700),
    (484,700),(516,700),(548,700), (580,700),(612,700),(562,294),
    (562,326),(562,358),(594,294), (594,358)
]

left_blocks2 = [
    # Top half of map
    (4,222),(36,222),(68,222),(100,222), (132,222),(132,190),(132,158),
    (132,126),(132,94),(132,62), (132,30),(164,24),(196,24),
    (228,24),(260,24),(292,24), (324,24),(356,24),(388,24),
    (420,24),(452,24),(484,24), (516,24),(548,24),(580,24), (612,24),
    
    # Middle of the map
    (484,232),(516,232),(548,232), (580,232),(612,232),(484,264),
    (516,264),(548,264),(580,264), (612,264),(484,296),(516,296),
    (548,296),(580,296),(612,296), (484,328),(516,328),(548,328),
    (580,328),(612,328),(484,360), (516,360),(548,360),(580,360),
    (612,360),(484,392),(516,392), (548,392),(580,392),(612,392),
    (484,424),(516,424),(548,424), (580,424),(612,424),(484,456),
    (516,456),(548,456),(580,456), (612,456),

    # Anything in between top and bottom
    (48,318),(80,318),(112,318), (144,318),(176,318),(208,318),
    (240,318),(260,318),(48,350), (80,350),(112,350),(144,350),
    (176,350),(208,350),(240,350), (260,350),(48,382),(80,382),
    (112,382),(144,382),(176,382), (208,382),(240,382),(260,382),
    (250,123),(250,155),(250,187), (282,123),(282,155),(282,187),
    (314,123),(314,155),(314,187), (330,123),(330,155),(330,187),
    (250,491),(250,523),(250,555), (282,491),(282,523),(282,555),
    (314,491),(314,523),(314,555), (330,491),(330,523),(330,555),

    # Bottom half of map
    (4,460),(36,460),(68,460),(100,460), (132,460),(132,492),(132,524),
    (132,556),(132,588),(132,620), (132,652),(164,652),(196,652),
    (228,652),(260,652),(292,652), (324,652),(356,652),(388,652),
    (420,652),(452,652),(484,652), (516,652),(548,652),(580,652), (612,652)
]

# Calculate mirrored positions dynamically
SCREEN_WIDTH = 1280
BLOCK_SIZE = 32

right_blocks1 = [(SCREEN_WIDTH - BLOCK_SIZE - x, y) for x, y in left_blocks1]
right_blocks2 = [(SCREEN_WIDTH - BLOCK_SIZE - x, y) for x, y in left_blocks2]

# Map borders (Coordinate Tuples)
map1_borders = left_blocks1 + right_blocks1
map2_borders = left_blocks2 + right_blocks2

# Hitboxes (pygame.Rects)
all_rectangles1 = [pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE) for x, y in map1_borders]
all_rectangles2 = [pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE) for x, y in map2_borders]

# Global cache to prevent re-initializing State objects every frame
_border_cache = {}

def render_border(map_coords, screen):
    """
    Renders border blocks efficiently by caching the State objects.
    Returns the list of instantiated border State objects for collision handling.
    """
    # Use the memory address of the map list as a unique cache key
    cache_key = id(map_coords)
    
    if cache_key not in _border_cache:
        # Initialize the State objects only ONCE per map
        _border_cache[cache_key] = [
            State(x, y, '../assets/wall.png', size=BLOCK_SIZE, is_collidable=True)
            for x, y in map_coords
        ]
        
    borders = _border_cache[cache_key]
    
    # Render the cached blocks
    for border_block in borders:
        border_block.render(screen)
        
    return borders