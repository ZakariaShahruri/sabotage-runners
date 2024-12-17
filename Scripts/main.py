# Imports of other scripts/logics
import os
import pygame
from player import Player
from config import *

# Initiliasation of pygame
pygame.init()

# Set working directory to main.py's directory. This makes sure the game will always launch from the right directory, making sure that we don't get
# weird errors saying that "there is no such file in this directory" or something alike
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Display and Title settings
screen = pygame.display.set_mode((screen_w, screen_h), fullscreen)
Title = pygame.display.set_caption("Sabotage Runners")
background_surface = pygame.image.load('../Images/dcbc8b76-6720-4fe2-91fd-0b418cedfa3e.webp')

player = Player(x=300, y=200, size=40, speed=7)

# The game loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the background
    screen.blit(background_surface,(0,0))

    # Player handling
    keys = pygame.key.get_pressed()
    player.handle_movement(keys, screen.get_width(), screen.get_height())
    player.draw(screen)
    
    # Update the display and set FPS to 120
    pygame.display.update()
    clock.tick(120)

# This is essentially the opposite of pygame.init() and closes the pygame library, might have to be moved to the bottom of the script.
# [Quick note, I am not sure if this is even necessary, I added it just in case]
pygame.quit()

# Not sure if we should switch this around with the game loop or not. It feels weird to me to define classes and stuff after having started the game loop.
class State:
    def __init__(self):
        self.x = 0

    def update(self, value):
        if value >= 0 :
            self.x += value
        else:
            self.x -= value
