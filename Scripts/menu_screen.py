import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame UI Example")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (170, 170, 170)
BLUE = (0, 122, 204)

# Fonts
pygame.font.init()
font = pygame.font.Font(None, 60)
# Button data (modified for center alignment)
button_width = 200
button_height = 60
button_padding = 20  # Space between buttons
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


def main():
    """Main loop for the UI."""
    running = True
    while running:
        screen.fill(WHITE)  # Clear screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        if button["label"] == "Play":
                            print("Play button clicked")
                        elif button["label"] == "Options":
                            print("Options button clicked")
                        elif button["label"] == "Commands":
                            print("Commands button clicked")
                        elif button["label"] == "Quit":
                            print("Quit button clicked")
                            running = False

        draw_buttons()
        pygame.display.flip()  # Update display

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
