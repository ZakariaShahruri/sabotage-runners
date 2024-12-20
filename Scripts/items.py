import os
import pygame
import random
from state import State

# Paths to power-up images
banana_image = "../images/items/banana_item.png"
freeze_image = "../Images/items/freeze_item.png"
mirror_image = "../Images/items/mirror_item.png"
slow_image = "../Images/items/slow_item.png"
speed_image = "../Images/items/speed_item.png"
teleport_image = "../Images/items/teleport_item.png"

# Timer durations (in milliseconds)
FREEZE_DURATION = 4000
SPEED_UP_DURATION = 5000
SLOW_DOWN_DURATION = 4000
MIRROR_DURATION = 5000

class Item(State):
    def __init__(self, x, y, image_path):
        """Base class for all items."""
        super().__init__(x, y, path=image_path, size=40, is_collidable=True)
        # Resize the image to a consistent size
        original_width, original_height = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(30*(original_width / original_height)), 30))
        
    def use(self, player1, player2):
        """Base method to be overridden by specific item types"""
        raise NotImplementedError("Subclasses must implement use method")

    def get_rect(self):
        return pygame.Rect(self.x , self.y, self.size-10, self.size-10)
    
class FreezeItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, freeze_image)

    def use(self, player1, player2):
        """Freeze the opponent instantly."""
        target = player2 if player1 == player2.opponent else player1
        target.speed = 0  # Freeze the player
        pygame.time.set_timer(pygame.USEREVENT + 1, FREEZE_DURATION)  # Unfreeze after the duration


class SpeedUpItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, speed_image)

    def use(self, player1, player2):
        """Increase the player's speed temporarily."""
        player = player1
        player.speed *= 1.5  # Boost speed
        pygame.time.set_timer(pygame.USEREVENT + 2, SPEED_UP_DURATION)  # Reset speed after the duration


class SlowDownItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, slow_image)

    def use(self, player1, player2):
        """Slow down the opponent temporarily."""
        target = player2 if player1 == player2.opponent else player1
        target.speed *= 0.3  # Slow down
        pygame.time.set_timer(pygame.USEREVENT + 3, SLOW_DOWN_DURATION)  # Reset speed after the duration


class MirrorItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, mirror_image)

    def use(self, player1, player2):
        """Reverse the opponent's controls."""
        target = player2 if player1 == player2.opponent else player1
        target.controls_reversed = True
        pygame.time.set_timer(pygame.USEREVENT + 5, MIRROR_DURATION)  # Reset controls after the duration


class TeleportItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, teleport_image)

    def use(self, player1, player2):
        """Teleport the opponent to their spawn point."""
        target = player2 if player1 == player2.opponent else player1
        target.x, target.y = target.spawn_x, target.spawn_y

item_classes = [
    FreezeItem,
    SpeedUpItem,
    SlowDownItem,
    MirrorItem,
    TeleportItem
]
    
map_spawn_coordinates = {
    1: [(277, 548),
        (636, 548),
        (1011, 548),
        (1011, 126),
        (636, 126),
        (277, 126)
        ]
,
    2: [(186, 173),
        (186, 480),
        (613, 151),
        (613, 500),
        (1049, 480),
        (1049, 173)
        ]
}

# Dictionary to track occupied spawn points for each map
occupied_spawn_points = {
    1: {},  # Will be initialized when needed
    2: {}   # Will be initialized when needed
}

def initialize_spawn_points(map_number):
    """Initialize or reset spawn points for a specific map"""
    occupied_spawn_points[map_number] = {coord: False for coord in map_spawn_coordinates[map_number]}

def generate_random_item(width, height, active_map):
    """Generate a random item for the specified map"""
    global occupied_spawn_points
    
    # Initialize spawn points for the map if not already done
    if not occupied_spawn_points[active_map]:
        initialize_spawn_points(active_map)
    
    # Get available spawn points for the current map
    available_spawn_points = [coord for coord, occupied in occupied_spawn_points[active_map].items() 
                            if not occupied]

    if not available_spawn_points:
        return None  # No available spawn points

    # Randomly choose an item class
    chosen_item_class = random.choice(item_classes)

    # Randomly select one of the available spawn coordinates
    x, y = random.choice(available_spawn_points)

    # Mark the spawn point as occupied for the current map
    occupied_spawn_points[active_map][(x, y)] = True

    # Return the chosen item class instantiated with the selected coordinates
    return chosen_item_class(x, y)

def reset_spawn_points(map_number):
    """Reset all spawn points for a specific map"""
    initialize_spawn_points(map_number)
    

