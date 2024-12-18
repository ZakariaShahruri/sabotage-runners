from music_manager import MusicManager, menu_music
import pygame
import sys

# Initialize Pygame
pygame.init()

# Main Menu Function
def main_menu():
    # Play menu music when entering the menu
    MusicManager.play_music(menu_music)

    # Button Instances
    buttons = [
        Button("Play", SCREEN_WIDTH // 2 - 100, 150, 200, 50, play_game),
        Button("Controls", SCREEN_WIDTH // 2 - 100, 220, 200, 50, show_controls),
        Button("Objective", SCREEN_WIDTH // 2 - 100, 290, 200, 50, show_objective),
        Button("Options", SCREEN_WIDTH // 2 - 100, 360, 200, 50, show_options),
        Button("Credits", SCREEN_WIDTH // 2 - 100, 430, 200, 50, show_credits),
        Button("Quit", SCREEN_WIDTH // 2 - 100, 500, 200, 50, quit_game)
    ]

    # Main Menu Loop
    while True:
        screen.blit(BACKGROUND_IMAGE, (0, 0))  # Draw the background image

        # Draw Buttons
        for button in buttons:
            button.draw(screen)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()  # Stop music when quitting
                pygame.quit()
                sys.exit()

        # Detect button click
        detect_button_click(buttons)

        # Update the Screen
        pygame.display.update()

# Screen Settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Game Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_PURPLE = (35, 9, 35)  # RGB for #230922
BRIGHT_PURPLE = (45, 19, 45)  # Lighter version of #230922 for hover effect
LIGHT_BLUE = (100, 149, 237)

# Fonts
pygame.font.init()
font = pygame.font.Font(None, 50)
text_font = pygame.font.SysFont("Arial", 24)
header_font = pygame.font.SysFont("Arial", 30, bold=True)

# Load Background Image
BACKGROUND_IMAGE = pygame.image.load("../menu_images/menu_screen.png")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Controls Image
CONTROLS_IMAGE = pygame.image.load("../menu_images/controls_image.png")
CONTROLS_IMAGE = pygame.transform.scale(CONTROLS_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load Darker Background Image
background_image = pygame.image.load("../menu_images/background_darker.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Gradient Text Drawing Function
def draw_text_gradient(surface, text, font, rect_center, color_start, color_end):
    """Draw text with a vertical gradient."""
    # Split gradient into lines
    text_surface = font.render(text, True, (0, 0, 0))  # Render text to get dimensions
    text_width, text_height = text_surface.get_size()
    gradient_surface = pygame.Surface((text_width, text_height), pygame.SRCALPHA)

    # Calculate the gradient step for each pixel row
    r1, g1, b1 = color_start
    r2, g2, b2 = color_end
    for y in range(text_height):
        t = y / text_height
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        pygame.draw.line(gradient_surface, (r, g, b), (0, y), (text_width, y))

    # Blit the text on top of the gradient
    text_alpha = font.render(text, True, (255, 255, 255))
    gradient_surface.blit(text_alpha, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    # Center the gradient text on the button
    text_rect = gradient_surface.get_rect(center=rect_center)
    surface.blit(gradient_surface, text_rect)

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
        """Draw button with hover effect, semi-transparent rectangle, and gradient text."""
        mouse_pos = pygame.mouse.get_pos()

        # Check if mouse is hovering over the button
        if self.rect.collidepoint(mouse_pos):
            # Scale the button on hover (increase size by 10%)
            new_width = int(self.original_width * self.scale_factor)
            new_height = int(self.original_height * self.scale_factor)
            new_x = self.rect.centerx - new_width // 2
            new_y = self.rect.centery - new_height // 2

            # Create new rect with the scaled size
            scaled_rect = pygame.Rect(new_x, new_y, new_width, new_height)
            pygame.draw.rect(surface, self.hover_color, scaled_rect)  # Hover color
        else:
            # Draw the button with original size and the dark purple color
            pygame.draw.rect(surface, self.color, self.rect)

        # Semi-transparent black rectangle (RGBA format for transparency)
        rect_color = (0, 0, 0, 240)  # 240 alpha for a bit of transparency
        if self.rect.collidepoint(mouse_pos):
            # Slightly brighter color on hover
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            # Draw semi-transparent dark purple rectangle
            pygame.draw.rect(surface, rect_color, self.rect)  # Semi-transparent rectangle
        
        # Draw gradient text
        color_start = (253, 162, 117)  # #fda275
        color_end = (250, 250, 158)    # #fafa9e
        draw_text_gradient(surface, self.text, font, self.rect.center, color_start, color_end)

# Button Click Detection
def detect_button_click(buttons):
    """Check if any button is clicked."""
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    # Check for mouse click on any button
    if mouse_pressed[0]:  # Left-click
        for button in buttons:
            if button.rect.collidepoint(mouse_pos):
                button.callback()

# Callbacks for Buttons
def play_game():
    print("Play button clicked! Start the game...")

def show_controls():
    while True:
        # Draw the controls image
        screen.blit(CONTROLS_IMAGE, (0, 0))

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Exit controls screen on ESC key
                    return

        # Update the Screen
        pygame.display.update()

def show_objective():


def show_options():
    print("Options button clicked! Show the options menu...")

# Define the credits text
credits_text = [
    "Credits",
    "A Sabotage Runners Production",
    "Zakaria Shahruri – Director of Chaotic Strategies",
    " Mastermind of mayhem and the driving force behind the game's sabotage mechanics.",
    "Ayden Schwindt – Lead Maze Architect",
    " Crafted the twisting labyrinths that will leave players puzzled and panicked.",
    "Mouad Khaouili – Sabotage Specialist",
    " Expert in designing devilish traps and dastardly power-ups.",
    "Sebastian Brink – Speed Enthusiast and Lightning Consultant",
    " Ensured the game’s pace keeps you on the edge of your seat—literally and figuratively.",
    "Jens Benoit – Control Reversal Technician",
    " Perfected the art of confusion with the legendary inverted controls.",
    "Brought to you by a team who knows that chaos, competition, and a little bit of sabotage are the perfect recipe for fun.",
    "Thanks for playing!"
]

def draw_credits():
    screen.blit(background_image, (0, 0))  # Draw background image

    # Draw header text
    header = header_font.render(credits_text[0], True, (255, 255, 255))
    screen.blit(header, (SCREEN_WIDTH // 2 - header.get_width() // 2, 30))

    # Draw the remaining credits text
    y_offset = 100  # Start position for text
    for line in credits_text[1:]:
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (50, y_offset))
        y_offset += 35  # Move down for the next line

    pygame.display.update()  # Update the screen

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
        Button("Credits", SCREEN_WIDTH // 2 - 100, 430, 200, 50, show_credits),
        Button("Quit", SCREEN_WIDTH // 2 - 100, 500, 200, 50, quit_game)
    ]

    # Main Menu Loop
    while True:
        screen.blit(BACKGROUND_IMAGE, (0, 0))  # Draw the background image

        # Draw Buttons
        for button in buttons:
            button.draw(screen)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Detect button click
        detect_button_click(buttons)

        # Update the Screen
        pygame.display.update()

# Run Main Menu
if __name__ == "__main__":
    main_menu()
