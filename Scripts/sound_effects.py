# sound_effects.py
import pygame

pygame.init()
pygame.mixer.init()

# Path to sound effects

freezed_fx = "../audios/freezed_fx.mp3"
speed_up_fx = "../audios/speed_up_fx.mp3"
slow_down_fx = "../audios/slow_down_fx.mp3"
teleport_fx = "../audios/teleport_fx.mp3"

mirrored_fx = "../audios/mirrored_fx.mp3"

class SoundEffects:
    def __init__(self):
        """Load sound effects into memory."""

        self.freezed = pygame.mixer.Sound(freezed_fx)
        self.speed_up = pygame.mixer.Sound(speed_up_fx)
        self.slow_down = pygame.mixer.Sound(slow_down_fx)
        self.teleport = pygame.mixer.Sound(teleport_fx)
        self.mirrored = pygame.mixer.Sound(mirrored_fx)
    
    
    def play_freeze(self):
        self.freezed.play()
    
    def play_speed_up(self):
        self.speed_up.play()
    
    def play_slow_down(self):
        self.slow_down.play()
    
    def play_teleport(self):
        self.teleport.play()
    
    def play_mirrored(self):
        self.mirrored.play()