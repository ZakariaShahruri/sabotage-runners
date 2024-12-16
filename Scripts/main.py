# Imports of other scripts/logics
import pygame
from player import Player

# Initiliasation of pygame
pygame.init()

# Display and Title settings
screen = pygame.display.set_mode((1950, 1300), pygame.RESIZABLE)
screen_color = (0, 0, 0)
Title = pygame.display.set_caption("Sabotage Runners")
clock = pygame.time.Clock()
background_surface = pygame.image.load('images/dcbc8b76-6720-4fe2-91fd-0b418cedfa3e.webp')

player = Player(x=300, y=200, size=40, speed=7)
# The game loop
running = True
while running:

    # Set the screen's color
    screen.fill(screen_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(background_surface,(0,0))
    keys = pygame.key.get_pressed()
    # Update player position
    player.handle_movement(keys, screen.get_width(), screen.get_height())
    # Draw the player
    player.draw(screen)
    
    
    # Update the display
    pygame.display.update()
    clock.tick(120)

class State:
    def __init__(self):
        self.x = 0

    def update(self, value):
        if value >= 0 :
            self.x += value
        else:
            self.x -= value
