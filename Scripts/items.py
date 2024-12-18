import os
import pygame
import random
from state import State

# Paths to power-up images
ITEM_DIR = "../Images/items/"
banana_image = "../images/items/banana_item.png"
freeze_image = "../Images/items/freeze_item.png"
mirror_image = "../Images/items/mirror_item.png"
slow_image = "../Images/items/slow_item.png"
speed_image = "../Images/items/speed_item.png"
teleport_image = "../Images/items/teleport_item.png"

class Item(State):
    def __init__(self, x, y, image_path):
        """Base class for all items."""
        super().__init__(x, y, path=image_path, size=40, is_collidable=True)
        # Resize the image to a consistent size
        self.image = pygame.transform.scale(self.image, (50, 50))
        

    def use(self, player1, player2):
        """Base method to be overridden by specific item types"""
        raise NotImplementedError("Subclasses must implement use method")

class BananaItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, banana_image)

    def use(self, player1, player2):
        """Throw the banana to stun the opponent when they collide."""
        target = player2 if player1 == player2.opponent else player1
        target.speed = 0  # Temporarily stop the player
        pygame.time.set_timer(pygame.USEREVENT, 2000)  # Reset speed after 2 seconds

class FreezeItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, freeze_image)

    def use(self, player1, player2):
        """Freeze the opponent instantly."""
        target = player2 if player1 == player2.opponent else player1
        target.speed = 0  # Freeze the player
        pygame.time.set_timer(pygame.USEREVENT + 1, 3000)  # Unfreeze after 3 seconds

class SpeedUpItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, speed_image)

    def use(self, player1, player2):
        """Increase the player's speed temporarily."""
        player = player1
        player.speed *= 1.5  # Boost speed
        pygame.time.set_timer(pygame.USEREVENT + 2, 5000)  # Reset speed after 5 seconds

class SlowDownItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, slow_image)

    def use(self, player1, player2):
        """Slow down the opponent temporarily."""
        target = player2 if player1 == player2.opponent else player1
        target.speed *= 0.5  # Slow down
        pygame.time.set_timer(pygame.USEREVENT + 3, 3000)  # Reset speed after 3 seconds

class MirrorItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, mirror_image)

    def use(self, player1, player2):
        """Reverse the opponent's controls."""
        target = player2 if player1 == player2.opponent else player1
        target.controls_reversed = True
        pygame.time.set_timer(pygame.USEREVENT + 5, 3000)  # Reset controls after 3 seconds

class TeleportItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, teleport_image)

    def use(self, player1, player2):
        """Teleport the opponent to their spawn point."""
        target = player2 if player1 == player2.opponent else player1
        target.x, target.y = target.spawn_x, target.spawn_y

def generate_random_item(screen_width, screen_height):
    """
    Generate a random item at a random location on the screen
    
    Args:
        screen_width (int): Width of the game screen
        screen_height (int): Height of the game screen
    
    Returns:
        Item: A randomly selected item
    """
    item_classes = [
        FreezeItem,
        SpeedUpItem,
        SlowDownItem,
        MirrorItem,
        TeleportItem
    ]
    
    # Randomly choose an item class
    chosen_item_class = random.choice(item_classes)
    
    # Generate random position, ensuring some padding from screen edges
    x = random.randint(50, screen_width - 100)
    y = random.randint(50, screen_height - 100)
    
    return chosen_item_class(x, y)