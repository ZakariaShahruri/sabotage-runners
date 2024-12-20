import pygame
from button import Button
import sys

pygame.mixer.init()



def round_over_screen(screen, game_logic, winner_name, get_font):
    """
    Display the round over screen with options to go to the main menu or the next map.
    """
    running = True

    pygame.mixer.music.load("../audios/menu_music.mp3")
    pygame.mixer.music.set_volume(0.05)  # Optional: Set volume between 0.0 and 1.0
    pygame.mixer.music.play(-1)  # Start the music

    # Load background image
    background = pygame.image.load("../menu_images/background_darker.png")
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

    # Button setup
    font = get_font(50)
    button_font = get_font(30)

    # Create buttons, Next Map comes before Main Menu
    next_map_button = Button(
        None, (640, 500), "Next Map", button_font, (255, 255, 255), (255, 255, 0)  # Yellow hover color
    )
    main_menu_button = Button(
        None, (640, 580), "Main Menu", button_font, (255, 255, 255), (255, 255, 0)  # Yellow hover color
    )

    # Create the round over and winner text
    round_over_text = font.render("Round Over!", False, (255, 255, 255))
    winner_text = font.render(f"Winner: {winner_name}", False, (255, 255, 0))

    # Get the rect positions for text
    round_over_text_rect = round_over_text.get_rect(center=(screen.get_width() // 2, 200))
    winner_text_rect = winner_text.get_rect(center=(screen.get_width() // 2, 300))

    while running:
        screen.blit(background, (0, 0))

        # Draw the round over text
        screen.blit(round_over_text, round_over_text_rect)
        screen.blit(winner_text, winner_text_rect)

        # Update buttons with hover effects
        mouse_pos = pygame.mouse.get_pos()

        # Change button colors when hovered over
        next_map_button.changeColor(mouse_pos)
        main_menu_button.changeColor(mouse_pos)

        # Render the buttons with the updated colors
        next_map_button.update(screen)
        main_menu_button.update(screen)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if next_map_button.checkForInput(pos):
                    pygame.time.delay(200)  # Add a small delay for button feedback
                    import map2
                    map2.load_map2()
                    return  # Ensure we exit this screen
                elif main_menu_button.checkForInput(pos):
                    pygame.time.delay(200)  # Add a small delay for button feedback
                    pygame.mixer.music.stop()
                    from menu_screen import main_menu
                    main_menu()
                    return  # Ensure we exit this screen

        pygame.display.flip()
        pygame.time.Clock().tick(60)  # Add frame rate control
