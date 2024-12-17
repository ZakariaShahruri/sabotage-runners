import pygame
from random import choice
from sound_effects import SoundEffects

pygame.init()

# Paths to power-up images
banana_image = "../items/banana_item.png"
freeze_image = "../items/freeze_item.png"
mirror_image = "../items/mirror_item.png"
shield_image = "../items/shield_item.png"
slow_image = "../items/slow_item.png"
speed_image = "../items/speed_item.png"
teleport_image = "../items/teleport_item.png"

class Item(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        """Base class for all items."""
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class BananaItem(Item):
    def __init__(self, x, y):
        super().__init__(banana_image, x, y)
        self.sound_effect = SoundEffects()

    def use(self, opponent):
        """Throw the banana to stun the opponent when they step on it."""
        self.sound_effect.play_banana_slip()
        # Code to stun opponent for a short duration, e.g., temporarily disable movement

class FreezeItem(Item):
    def __init__(self, x, y):
        super().__init__(freeze_image, x, y)
        self.sound_effect = SoundEffects()

    def use(self, opponent):
        """Freeze the opponent instantly."""
        self.sound_effect.play_freeze()
        # Code to freeze the opponent for a short time, e.g., disable movement

class SpeedUpItem(Item):
    def __init__(self, x, y):
        super().__init__(speed_image, x, y)
        self.sound_effect = SoundEffects()

    def use(self, player):
        """Increase the player's speed temporarily."""
        self.sound_effect.play_speed_up()
        # Code to speed up the player for a short duration

class SlowDownItem(Item):
    def __init__(self, x, y):
        super().__init__(slow_image, x, y)
        self.sound_effect = SoundEffects()

    def use(self, opponent):
        """Slow down the opponent temporarily."""
        self.sound_effect.play_slow_down()
        # Code to slow down the opponent for a short duration

class ShieldItem(Item):
    def __init__(self, x, y):
        super().__init__(shield_image, x, y)
        self.sound_effect = SoundEffects()

    def use(self, player):
        """Give the player a shield to protect from items."""
        self.sound_effect.play_shield()
        # Code to grant the player a shield, e.g., immunity for a short duration

class MirrorItem(Item):
    def __init__(self, x, y):
        super().__init__(mirror_image, x, y)
        self.sound_effect = SoundEffects()

    def use(self, opponent):
        """Reverse the opponent's controls."""
        self.sound_effect.play_mirrored()
        # Code to reverse the opponent's controls for a short duration

class TeleportItem(Item):
    def __init__(self, x, y):
        super().__init__(teleport_image, x, y)
        self.sound_effect = SoundEffects()

    def use(self, opponent):
        """Teleport the opponent to their spawn point."""
        self.sound_effect.play_teleport()
        # Code to teleport the opponent back to their spawn

# Example usage in the game loop:
if __name__ == "__main__":
    # Example to test power-up usage
    sound_effects = SoundEffects()
    
    # Create items
    banana = BananaItem(100, 100)
    freeze = FreezeItem(200, 200)
    speed_up = SpeedUpItem(300, 300)
    slow_down = SlowDownItem(400, 400)
    shield = ShieldItem(500, 500)
    mirror = MirrorItem(600, 600)
    teleport = TeleportItem(700, 700)
    
    # Simulate using the items
    banana.use(opponent="Player2")
    freeze.use(opponent="Player2")
    speed_up.use(player="Player1")
    slow_down.use(opponent="Player2")
    shield.use(player="Player1")
    mirror.use(opponent="Player2")
    teleport.use(opponent="Player2")

    pygame.quit()