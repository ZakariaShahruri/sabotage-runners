# Imports of other scripts/logics
import pygame

# Initiliasation of pygame
pygame.init()

# Display and Title settings
screen = pygame.display.set_mode((400, 800), pygame.RESIZABLE)
Title = pygame.display.set_caption("Game")

# The game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False