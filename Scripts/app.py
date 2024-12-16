# This is going to be the file to initiate the app, and it will be on the starting menu by default.
# Imports of other scripts/logics
import os
import pygame

# Initiliasation of pygame
pygame.init()

# Set working directory to main.py's directory. This makes sure the game will always launch from the right directory, making sure that we don't get
# weird errors saying that "there is no such file in this directory" or something alike
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Function to create the main window
def create_main_surface():
    screen = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
    pygame.display.set_caption("Sabotage Runners")
    return screen

# Create the main game surface
screen = create_main_surface()

# [Commented this out because it is redundant. I haven't deleted it because I don't know if we'd still need it for something else?]
# # Screen background color
# screen_color = (0, 0, 0)


# # The game loop
# running = True
# while running:

#     # Set the screen's color
#     screen.fill(screen_color)

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
    
    
#     # Update the display
#     pygame.display.flip()
    
# Button data
buttons = [
    {"label": "Play", "rect": pygame.Rect(300, 150, 200, 60), "color": (200, 200, 200)},
    {"label": "Options", "rect": pygame.Rect(300, 250, 200, 60), "color": (200, 200, 200)},
    {"label": "Commands", "rect": pygame.Rect(300, 350, 200, 60), "color": (200, 200, 200)},
    {"label": "Quit", "rect": pygame.Rect(300, 450, 200, 60), "color": (200, 200, 200)},
]

def draw_buttons():
    """Render buttons with labels."""
    for button in buttons:
        color = (170, 170, 170) if button["rect"].collidepoint(pygame.mouse.get_pos()) else button["color"]
        pygame.draw.rect(screen, color, button["rect"])
        pygame.draw.rect(screen, (0, 122, 204), button["rect"], 3)  # Border
        label = pygame.font.Font(None, 60).render(button["label"], True, (0, 0, 0))
        screen.blit(label, (button["rect"].x + (button["rect"].width - label.get_width()) // 2,
                            button["rect"].y + (button["rect"].height - label.get_height()) // 2))
        
def main():
    """Main loop for the UI."""
    running = True
    while running:
        screen.fill((255, 255, 255))  # Clear screen

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


if __name__ == "__main__":
    main()