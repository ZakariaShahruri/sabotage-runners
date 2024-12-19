import pygame
import sys
import main

# Initialize Pygame
pygame.init()

# Screen Settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Game Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_PURPLE = (35, 9, 35)  # RGB for #230922
BRIGHT_PURPLE = (45, 19, 45)  # Lighter version of #230922 for hover effect

# Fonts
font = pygame.font.Font(None, 50)
header_font = pygame.font.SysFont("Arial", 30, bold=True)

# Load Background Image
BACKGROUND_IMAGE = pygame.image.load("../menu_images/menu_background.png")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load Darker Background Image
BACKGROUND_DARKER = pygame.image.load("../menu_images/background_darker.png")
BACKGROUND_DARKER = pygame.transform.scale(BACKGROUND_DARKER, (SCREEN_WIDTH, SCREEN_HEIGHT))

class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = DARK_PURPLE
        self.hover_color = BRIGHT_PURPLE
        self.callback = callback
        self.original_width = width
        self.original_height = height
        self.scale_factor = 1.1

    def draw(self, surface):
        """Draw button with hover effect and gradient text."""
        mouse_pos = pygame.mouse.get_pos()

        # Check if mouse is hovering over the button
        is_hovered = self.rect.collidepoint(mouse_pos)
        rect_color = self.hover_color if is_hovered else self.color

        # Scale the button on hover
        if is_hovered:
            new_width = int(self.original_width * self.scale_factor)
            new_height = int(self.original_height * self.scale_factor)
            scaled_rect = self.rect.inflate(
                new_width - self.original_width, new_height - self.original_height
            )
            pygame.draw.rect(surface, rect_color, scaled_rect)
        else:
            pygame.draw.rect(surface, rect_color, self.rect)

        # Draw text
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

# Button Click Detection
def detect_button_click(buttons):
    """Check if any button is clicked."""
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    if mouse_pressed[0]:  # Left-click
        for button in buttons:
            if button.rect.collidepoint(mouse_pos):
                button.callback()

# Callbacks for Buttons
def play_game():
    main.game_loop()

def show_controls():
    print("Controls button clicked! Show controls screen...")

def show_objective():
    print("Objective button clicked! Show objectives screen...")

def show_options():
    print("Options button clicked! Show options menu...")

def draw_credits():
    """Render credits with better alignment and scrollable feature."""
    scroll_y = 0  # Add scrolling logic here if needed
    screen.blit(BACKGROUND_DARKER, (0, 0))

    y_offset = 100
    for line in credits_text:
        text_surface = font.render(line, True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += 35

    pygame.display.update()

def quit_game():
    print("Quit button clicked! Exiting the game...")
    pygame.quit()
    sys.exit()

# Main Menu Function
def main_menu():
    # Button Instances
    buttons = [
        Button("Play", SCREEN_WIDTH // 2 - 100, 150, 200, 50, play_game),
        Button("Controls", SCREEN_WIDTH // 2 - 100, 220, 200, 50, show_controls),
        Button("Objective", SCREEN_WIDTH // 2 - 100, 290, 200, 50, show_objective),
        Button("Options", SCREEN_WIDTH // 2 - 100, 360, 200, 50, show_options),
        Button("Credits", SCREEN_WIDTH // 2 - 100, 430, 200, 50, draw_credits),
        Button("Quit", SCREEN_WIDTH // 2 - 100, 500, 200, 50, quit_game),
    ]

    # Main Menu Loop
    while True:
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        for button in buttons:
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        detect_button_click(buttons)
        pygame.display.update()

if __name__ == "__main__":
    main_menu()