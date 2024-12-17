import os
import sys
import pygame
from player import Player
from items import generate_random_item

# Set working directory to main.py's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Screen dimensions
WIDTH, HEIGHT = 1280, 720

def game_loop():
    """This function handles the main game logic."""
    # Initialization of pygame
    pygame.init()

    # Screen setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Sabotage Runners")
    
    # Colors
    screen_color = (0, 0, 0)
    background = pygame.image.load("../Images/background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Create players
    player1 = Player(path="../Images/players/player1_idle1.png", x=20, y=300)
    player2 = Player(path="../Images/players/player2_idle1.png", x=1200, y=300)

    # Set opponents
    player1.opponent = player2
    player2.opponent = player1

    # Item management
    current_item = generate_random_item(WIDTH, HEIGHT)
    item_spawned = True

    # The game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Reset item effects
            if event.type == pygame.USEREVENT:
                player1.speed = 10
                player2.speed = 10
            if event.type in [pygame.USEREVENT + i for i in range(1, 6)]:
                player1.speed = 10
                player2.speed = 10
                player1.controls_reversed = False
                player2.controls_reversed = False

        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Clear the screen and draw the background
        screen.fill(screen_color)
        screen.blit(background, (0, 0))

        # Handle player movement
        player1.handle_movement("WASD", keys, WIDTH, HEIGHT)
        player2.handle_movement("arrows", keys, WIDTH, HEIGHT)

        # Render and check item collision
        if item_spawned:
            current_item.render(screen)
            if player1.check_collision(current_item):
                current_item.use(player1, player2)
                item_spawned = False
            if player2.check_collision(current_item):
                current_item.use(player2, player1)
                item_spawned = False

        # Render players
        player1.render(screen)
        player2.render(screen)

        # Update display
        pygame.display.flip()

        # Limit FPS to 60
        clock.tick(60)

    # Close pygame
    pygame.quit()
    sys.exit()

def menu():
    """Main menu for Sabotage Runners."""
    # Initialize Pygame
    pygame.init()

    # Screen setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sabotage Runners")
    menu_cover = pygame.image.load("../Images/menucover.png")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    LIGHT_GRAY = (170, 170, 170)
    BLUE = (0, 122, 204)

    # Button data
    button_width, button_height = 200, 60
    button_padding = 20
    font = pygame.font.Font(None, 60)

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

    # Menu loop
    running = True
    while running:
        screen.blit(menu_cover, (0, 0))
        draw_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        if button["label"] == "Play":
                            game_loop()  # Start the game loop
                        elif button["label"] == "Options":
                            print("Options button clicked")
                        elif button["label"] == "Commands":
                            print("Commands button clicked")
                        elif button["label"] == "Quit":
                            running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    menu()
