import os
import pygame
from player import Player
from state import State
import sys

# Set working directory to main.py's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def menu():
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sabotage Runners")
    menu_cover = pygame.image.load("../Images/menucover.png")
    

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    LIGHT_GRAY = (170, 170, 170)
    BLUE = (0, 122, 204)
    
    # Button data (modified for center alignment)
    button_width = 200
    button_height = 60
    button_padding = 20  # Space between buttons

    # Fonts
    pygame.font.init()
    font = pygame.font.Font(None, 60)

    # Button data
    buttons = [
        {"label": "Play", "rect": pygame.Rect((WIDTH - button_width) // 2, 150, button_width, button_height), "color": GRAY},
        {"label": "Options", "rect": pygame.Rect((WIDTH - button_width) // 2, 150 + button_height + button_padding, button_width, button_height), "color": GRAY},
        {"label": "Commands", "rect": pygame.Rect((WIDTH - button_width) // 2, 150 + 2 * (button_height + button_padding), button_width, button_height), "color": GRAY},
        {"label": "Quit", "rect": pygame.Rect((WIDTH - button_width) // 2, 150 + 3 * (button_height + button_padding), button_width, button_height), "color": GRAY},
    ]

    def draw_buttons():
        """Render buttons with labels."""
        for button in buttons:
            color = LIGHT_GRAY if button["rect"].collidepoint(pygame.mouse.get_pos()) else button["color"]
            pygame.draw.rect(screen, color, button["rect"])
            pygame.draw.rect(screen, BLUE, button["rect"], 3)  # Border
            label = font.render(button["label"], True, BLACK)
            screen.blit(label, (button["rect"].x + (button["rect"].width - label.get_width()) // 2,
                                button["rect"].y + (button["rect"].height - label.get_height()) // 2))

    def game_loop():
        """This function handles the main game logic."""
        running = True
        screen_width, screen_height = 1280, 720
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Sabotage Runners")

        # Create player
        player1 = Player(path="../Images/players/player1_idle1.png", x=20, y=300)
        player2 = Player(path="../Images/players/player2_idle1.png", x=1200, y=300)

        # The game loop
        clock = pygame.time.Clock()

        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Get pressed keys
            keys = pygame.key.get_pressed()

            # Clear the screen
            screen.blit(menu_cover, (0,0))
            background = pygame.image.load("../Images/background.png")
            background = pygame.transform.scale(background, (1280, 720))
            screen.blit(background, (0, 0))

            # Handle player movement
            player1.handle_movement("WASD", keys, screen_width, screen_height)
            player2.handle_movement("arrows", keys, screen_width, screen_height)

            # Render player
            player1.render(screen)
            player2.render(screen)

            # Update display
            pygame.display.flip()

            # Limit FPS to 60
            clock.tick(60)

        # Close pygame
        pygame.quit()
        sys.exit()

    # Main loop for the UI
    running = True
    while running:
        screen.blit(menu_cover, (0,0))    
    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        if button["label"] == "Play":
                            game_loop()  # Start the game loop when Play is clicked
                        elif button["label"] == "Options":
                            print("Options button clicked")
                        elif button["label"] == "Commands":
                            print("Commands button clicked")
                        elif button["label"] == "Quit":
                            running = False

        draw_buttons()
        pygame.display.flip()  # Update display

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    menu()
