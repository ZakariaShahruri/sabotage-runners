import pygame
import sys
import main
import menu_screen
from button import Button

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Colors
WHITE = (255, 255, 255)
BASE_COLOR = (200, 200, 200)
HOVER_COLOR = (255, 255, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sabotage Runners")


def show_end_screen(winner, victory=True):
    """Display the end screen with the winner, score, and options."""
    pygame.mixer.init()

    try:
        # Load background image
        END_SCREEN_BACKGROUND = pygame.image.load("../menu_images/background_darker.png")
        END_SCREEN_BACKGROUND = pygame.transform.scale(END_SCREEN_BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Play background music
        pygame.mixer.music.load("../audios/end_screen_music.mp3")
        pygame.mixer.music.play(-1, 0.0)  # Loop the music indefinitely
    except pygame.error as e:
        print(f"Error loading assets: {e}")
        return

    # Font for the message and buttons
    end_font = pygame.font.Font(None, 100)
    button_font = pygame.font.Font(None, 40)

    # Render the winner message
    end_text = f"{winner} Wins!" if victory else "Game Over"
    end_text_surface = end_font.render(end_text, True, WHITE)
    end_text_rect = end_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

    # Create buttons for replay and exit
    replay_button = Button(
        image=None,
        pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80),
        text_input="Play Again",
        font=button_font,
        base_color=BASE_COLOR,
        hovering_color=HOVER_COLOR,
    )

    exit_button = Button(
        image=None,
        pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150),
        text_input="Main Menu",
        font=button_font,
        base_color=BASE_COLOR,
        hovering_color=HOVER_COLOR,
    )

    # Draw the end screen
    clock = pygame.time.Clock()
    while True:
        screen.blit(END_SCREEN_BACKGROUND, (0, 0))

        # Draw the winner message and score
        screen.blit(end_text_surface, end_text_rect)

        # Update buttons
        mouse_pos = pygame.mouse.get_pos()
        replay_button.changeColor(mouse_pos)
        exit_button.changeColor(mouse_pos)
        replay_button.update(screen)
        exit_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.checkForInput(mouse_pos):
                    replay_game()
                if exit_button.checkForInput(mouse_pos):
                    back_to_menu()

        pygame.display.update()
        clock.tick(60)


def replay_game():
    """Reset the game and start again."""
    pygame.mixer.music.stop()
    main.game_loop()


def back_to_menu():
    """Return to the main menu."""
    pygame.time.delay(200)
    pygame.mixer.music.stop()
    menu_screen.main_menu()


if __name__ == "__main__":
    show_end_screen()
