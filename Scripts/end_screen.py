import pygame
import sys
import main
import menu_screen
from button import Button

# Screen dimensions (you can adjust this)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Colors
WHITE = (255, 255, 255)

# Game outcomes
def show_end_screen(winner, score, victory=True):
    """Display the end screen with the winner, score, and options."""
    # Initialize pygame mixer for background music
    pygame.mixer.init()

    # Load background image
    END_SCREEN_BACKGROUND = pygame.image.load("../menu_images/background_darker.png")
    END_SCREEN_BACKGROUND = pygame.transform.scale(END_SCREEN_BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Play background music
    pygame.mixer.music.load("../audios/end_screen_music.mp3")
    pygame.mixer.music.play(-1, 0.0)  # Loop the music indefinitely

    # Font for the message and score
    end_font = pygame.font.Font(None, 100)
    score_font = pygame.font.Font(None, 50)

    # Render the winner message
    end_text = f"{winner} Wins!" if victory else "Game Over"
    end_text_surface = end_font.render(end_text, True, WHITE)
    end_text_rect = end_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

    # Render the score message
    score_text_surface = score_font.render(f"Score: {score}", True, WHITE)
    score_text_rect = score_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Render the thank you message
    thank_you_text = "Thank you for playing!"
    thank_you_surface = score_font.render(thank_you_text, True, WHITE)
    thank_you_rect = thank_you_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5))

    # Create buttons for replay and exit
    replay_button = Button("Play Again", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 80, 200, 50, replay_game)
    exit_button = Button("Main Menu", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 50, back_to_menu)

    # Draw the end screen
    while True:
        screen.blit(END_SCREEN_BACKGROUND, (0, 0))

        # Draw the winner message and score
        screen.blit(end_text_surface, end_text_rect)
        screen.blit(score_text_surface, score_text_rect)
        screen.blit(thank_you_surface, thank_you_rect)

        # Draw buttons
        replay_button.draw(screen)
        exit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        detect_button_click([replay_button, exit_button])
        pygame.display.update()

def replay_game():
    """Reset the game and start again."""
    main.game_loop()

def back_to_menu():
    """Return to the main menu."""
    menu_screen.main_menu()

# Function to detect button click, assuming Button class is defined
def detect_button_click(buttons):
    """Detect button clicks and handle events."""
    for button in buttons:
        if button.is_hovered():
            if pygame.mouse.get_pressed()[0]:  # Left click
                button.callback()

# Main program to initialize pygame and the screen
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("End Screen")