# Imports of other scripts/logics
import os
import pygame
from player import Player

# Initiliasation of pygame
pygame.init()

# Set working directory to main.py's directory. This makes sure the game will always launch from the right directory, making sure that we don't get
# weird errors saying that "there is no such file in this directory" or something alike
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Display and Title settings
screen = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
screen_color = (0, 0, 0)
Title = pygame.display.set_caption("Sabotage Runners")

# Defined player in main [Adds more readability this way imo, also sped up the player as it felt quite slow :)]
player = Player(x=300, y=200, size=40, color=(0, 255, 0), speed=3)

# The game loop
running = True
while running == True:

    # Set the screen's color
    screen.fill(screen_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Player handling [potentially better way to section this off? just a suggestion]
    keys = pygame.key.get_pressed()
    # Update player position
    player.handle_movement(keys, screen.get_width(), screen.get_height())
    # Draw the player
    player.draw(screen)
    
    
    # Update the display
    pygame.display.flip()

    # Limit FPS to 60 [This should fix the weird feeling of the player movement]
    pygame.time.Clock().tick(60)

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
