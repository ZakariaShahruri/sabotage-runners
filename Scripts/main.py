import os
import pygame
from player import Player
from state import State
# Set working directory to main.py's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():
    # Initialization of pygame
    pygame.init()

    # Screen setup
    screen_width, screen_height = 800, 533
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Sabotage Runners")
    
    screen_color = (0, 0, 0)

    # Create player
    player1 = Player(x=300, y=200)
    player2 = Player(x=300, y=150)

    # The game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Clear the screen
        screen.fill(screen_color)
        background = pygame.image.load("../Images/background.webp")
        screen.blit(background, (0,0))
        if player1.check_collision(player2):
            print("HI")
        # Handle player movement
        player1.handle_movement("WASD",keys, screen_width, screen_height)
        player2.handle_movement("arrows",keys, screen_width, screen_height)

        # Render player
        player1.render(screen)
        player2.render(screen)

        # Update display
        pygame.display.flip()

        # Limit FPS to 60
        clock.tick(60)

    # Close pygame
    pygame.quit()

if __name__ == "__main__":
    main()
