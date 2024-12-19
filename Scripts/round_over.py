import pygame
from button import Button
import sys

def round_over_screen(screen, game_logic, winner_name, get_font):
    """
    Display the round over screen with options to go to the main menu or the next map.

    Args:
        screen (pygame.Surface): The game screen.
        game_logic (GameLogic): Instance of GameLogic to manage transitions.
        winner_name (str): The name of the round winner.
        get_font (function): Function to load fonts.
    """
    running = True

    # Button setup
    font = get_font(50)
    button_font = get_font(30)

    main_menu_button = Button(
        None, (640, 500), "Main Menu", button_font, (255, 255, 255), (150, 150, 150)
    )
    next_map_button = Button(
        None, (640, 580), "Next Map", button_font, (255, 255, 255), (150, 150, 150)
    )

    while running:
        screen.fill((0, 0, 0))  # Clear screen with black
        round_over_text = font.render("Round Over!", True, (255, 255, 255))
        winner_text = font.render(f"Winner: {winner_name}", True, (255, 255, 0))

        # Blit text
        screen.blit(round_over_text, (screen.get_width() // 2 - round_over_text.get_width() // 2, 200))
        screen.blit(winner_text, (screen.get_width() // 2 - winner_text.get_width() // 2, 300))

        # Render buttons
        main_menu_button.update(screen)
        next_map_button.update(screen)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if main_menu_button.checkForInput(pos):
                    from menu_screen import main_menu
                    main_menu()
                elif next_map_button.checkForInput(pos):
                    # Logic to load the next map
                    game_logic.reset_players()  # Reset players
                    return

        pygame.display.flip()
