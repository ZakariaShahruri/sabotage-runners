import pygame
import random
from state import State

# --- CONSTANTS ---
ITEM_SIZE = 30
FREEZE_DURATION = 4000
SPEED_UP_DURATION = 5000
SLOW_DOWN_DURATION = 4000
MIRROR_DURATION = 5000

# Item image paths
IMAGE_PATHS = {
    "banana": "../images/items/banana_item.png",
    "freeze": "../Images/items/freeze_item.png",
    "mirror": "../Images/items/mirror_item.png",
    "slow": "../Images/items/slow_item.png",
    "speed": "../Images/items/speed_item.png",
    "teleport": "../Images/items/teleport_item.png"
}

class Item(State):
    """Base class for all collectable items in the game."""
    def __init__(self, x, y, image_path):
        super().__init__(x, y, path=image_path, size=40, is_collidable=True)
        self._scale_image()

    def _scale_image(self):
        """Scales the item image to maintain aspect ratio with a consistent height."""
        original_width, original_height = self.image.get_size()
        aspect_ratio = original_width / original_height
        new_width = int(ITEM_SIZE * aspect_ratio)
        self.image = pygame.transform.scale(self.image, (new_width, ITEM_SIZE))

    def use(self, activator, target):
        """
        Apply the item's effect. 
        :param activator: The player who picked up the item.
        :param target: The opposing player.
        """
        raise NotImplementedError("Subclasses must implement the 'use' method")

    def get_rect(self):
        # Slightly smaller hitbox than the render size
        return pygame.Rect(self.x, self.y, self.size - 10, self.size - 10)


class FreezeItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, IMAGE_PATHS["freeze"])

    def use(self, activator, target):
        target.speed = 0
        pygame.time.set_timer(pygame.USEREVENT + 1, FREEZE_DURATION)


class SpeedUpItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, IMAGE_PATHS["speed"])

    def use(self, activator, target):
        activator.speed *= 1.5
        pygame.time.set_timer(pygame.USEREVENT + 2, SPEED_UP_DURATION)


class SlowDownItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, IMAGE_PATHS["slow"])

    def use(self, activator, target):
        target.speed *= 0.3
        pygame.time.set_timer(pygame.USEREVENT + 3, SLOW_DOWN_DURATION)


class MirrorItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, IMAGE_PATHS["mirror"])

    def use(self, activator, target):
        target.controls_reversed = True
        pygame.time.set_timer(pygame.USEREVENT + 5, MIRROR_DURATION)


class TeleportItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, IMAGE_PATHS["teleport"])

    def use(self, activator, target):
        target.x, target.y = target.spawn_x, target.spawn_y


# Configuration for item spawning
ITEM_CLASSES = [FreezeItem, SpeedUpItem, SlowDownItem, MirrorItem, TeleportItem]

MAP_SPAWN_COORDINATES = {
    1: [(277, 548), (636, 548), (1011, 548), (1011, 126), (636, 126), (277, 126)],
    2: [(186, 173), (186, 480), (613, 151), (613, 500), (1049, 480), (1049, 173)]
}

# State tracker for spawn points
occupied_spawn_points = {1: {}, 2: {}}

def initialize_spawn_points(map_number):
    """Resets all spawn points for a specific map to unoccupied."""
    occupied_spawn_points[map_number] = {coord: False for coord in MAP_SPAWN_COORDINATES[map_number]}

def generate_random_item(width, height, active_map):
    """Selects a random unoccupied spawn point and returns a random Item instance."""
    if not occupied_spawn_points[active_map]:
        initialize_spawn_points(active_map)
    
    available_points = [coord for coord, is_occupied in occupied_spawn_points[active_map].items() if not is_occupied]

    if not available_points:
        return None  

    spawn_pos = random.choice(available_points)
    chosen_class = random.choice(ITEM_CLASSES)
    
    occupied_spawn_points[active_map][spawn_pos] = True
    return chosen_class(spawn_pos[0], spawn_pos[1])

def reset_spawn_points(map_number):
    initialize_spawn_points(map_number)