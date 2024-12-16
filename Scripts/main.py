# Imports of other scripts/logics
import pygame
import player

# Initiliasation of pygame
pygame.init()

# Display and Title settings
screen = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
screen_color = (0, 0, 0)
Title = pygame.display.set_caption("Sabotage Runners")


# The game loop
running = True
while running:

    

    # Set the screen's color
    screen.fill(screen_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
    # Update the display
    pygame.display.flip()