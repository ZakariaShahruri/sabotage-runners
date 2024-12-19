import pygame
import sys
import main
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen Settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
pygame.display.set_caption("Sabotage Runners")

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

OPTIONS_BACKGROUND = pygame.image.load("../menu_images/background_darker.png")
OPTIONS_BACKGROUND = pygame.transform.scale(OPTIONS_BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load Music
pygame.mixer.music.load("../audios/menu_music.mp3")
pygame.mixer.music.set_volume(0.5)  # Optional: Set volume between 0.0 and 1.0
pygame.mixer.music.play(-1)  # Start the music
pygame.mixer.music.set_volume(0.05)


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
    # Load and display the controls image
    controls_image = pygame.image.load("../menu_images/controls_image.png")
    controls_image = pygame.transform.scale(controls_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    while True:
        screen.blit(controls_image, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  # Go back to the main menu

        pygame.display.update()

def show_objective():
    # Load multiple images for objectives
    objective_images = [
        pygame.image.load("../menu_images/objective_image.png"),
        pygame.image.load("../menu_images/items_image.png")
    ]
    objective_images = [pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT)) for img in objective_images]
    
    current_image_index = 0

    while True:
        screen.blit(objective_images[current_image_index], (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:  # Next image
                    current_image_index = (current_image_index + 1) % len(objective_images)
                elif event.key == pygame.K_LEFT:  # Previous image
                    current_image_index = (current_image_index - 1) % len(objective_images)
                elif event.key == pygame.K_ESCAPE:  # Exit to menu
                    return

        pygame.display.update()

def back_to_menu():
    pygame.time.delay(200)  # Optional, for smooth transition
    main_menu()  # Call main menu again to reset the state


def show_options():
    """Display the options menu."""
    # Options settings
    options = {
        "Music": True,  # Example toggle for music
        "Fullscreen": False,  # Example toggle for fullscreen
    }
    
    # Create buttons for each option
    option_buttons = []
    y_offset = 150
    for option, value in options.items():
        button = Button(
            f"{option}: {'ON' if value else 'OFF'}",
            SCREEN_WIDTH // 2 - 200,
            y_offset,
            400,
            50,
            lambda opt=option: toggle_option(opt, options, option_buttons)
        )
        option_buttons.append(button)
        y_offset += 70

    back_button = Button(
        "Back to Menu",
        SCREEN_WIDTH // 2 - 100,
        y_offset,
        200,
        50,
        back_to_menu
    )
    option_buttons.append(back_button)

    # Options menu loop
    while True:
        screen.blit(OPTIONS_BACKGROUND, (0, 0))

        header_surface = header_font.render("Options Menu", True, WHITE)
        header_rect = header_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(header_surface, header_rect)

        for button in option_buttons:
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        detect_button_click(option_buttons)
        pygame.display.update()

def toggle_option(option, options, buttons):
    """Toggle the specified option and update button text."""
    options[option] = not options[option]
    
    # Handle specific option changes
    if option == "Music":
        if options[option]:
            pygame.mixer.music.play(-1)  # Start the music
        else:
            pygame.mixer.music.stop()
    elif option == "Fullscreen":
        if options[option]:
            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    for button in buttons:
        if option in button.text:
            button.text = f"{option}: {'ON' if options[option] else 'OFF'}" 

def draw_credits():
    # Load and display the credits image
    credits_image = pygame.image.load("../menu_images/credits_image.png")
    credits_image = pygame.transform.scale(credits_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    while True:
        screen.blit(credits_image, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  # Go back to the main menu

        pygame.display.update()

def quit_game():
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