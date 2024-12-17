import pygame

pygame.init()
pygame.mixer.init()

# Path to sound effects
banana_slip_fx = "../audios/banana_slip_fx.mp3"
freezed_fx = "../audios/freezed_fx.mp3"
speed_up_fx = "../audios/speed_up_fx.mp3"
slow_down_fx = "../audios/slow_down_fx.mp3"
teleport_fx = "../audios/teleport_fx.mp3"
shield_fx = "../audios/shield_fx.mp3"
mirrored_fx = "../audios/mirrored_fx.mp3"

# Sound Effect Manager Class
class SoundEffects:
    def __init__(self):
        """Load sound effects into memory."""
        self.banana_slip = pygame.mixer.Sound(banana_slip_fx)
        self.freezed = pygame.mixer.Sound(freezed_fx)
        self.speed_up = pygame.mixer.Sound(speed_up_fx)
        self.slow_down = pygame.mixer.Sound(slow_down_fx)
        self.teleport = pygame.mixer.Sound(teleport_fx)
        self.shield = pygame.mixer.Sound(shield_fx)
        self.mirrored = pygame.mixer.Sound(mirrored_fx)
    
    def play_banana_slip(self):
        """Play the banana slip sound effect."""
        self.banana_slip.play()
    
    def play_freeze(self):
        """Play the freeze power-up sound effect."""
        self.freezed.play()
    
    def play_speed_up(self):
        """Play the speed-up power-up sound effect."""
        self.speed_up.play()
    
    def play_slow_down(self):
        """Play the slow-down power-up sound effect."""
        self.slow_down.play()
    
    def play_teleport(self):
        """Play the teleport sound effect."""
        self.teleport.play()

    def play_shield(self):
        """Play the shield sound effect."""
        self.shield.play()
    
    def play_mirrored(self):
        """Play the mirrored power-up sound effect."""
        self.mirrored.play()