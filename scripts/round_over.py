import sys
import pygame
from button import Button

# --- CONSTANTS ---
BACKGROUND_IMAGE_PATH = "../images/menu/background_darker.png"
MENU_MUSIC_PATH = "../assets/audio/menu_music.mp3"

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

def round_over_screen(screen, game_logic, winner_name, get_font):
    """
    Displays the round over screen, announcing the winner and 
    providing options to proceed to the next map or return to the main menu.
    """
    # --- AUDIO SETUP ---
    try:
        pygame.mixer.music.load(MENU_MUSIC_PATH)
        pygame.mixer.music.set_volume(0.10)
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"Warning: Could not load round over music: {e}")

    # --- ASSET LOADING ---
    # .convert() optimizes the image format for faster rendering
    background = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

    font_large = get_font(50)
    font_small = get_font(30)

    # --- TEXT RENDER SETUP ---
    # Set antialiasing to True for smoother, professional-looking text
    round_over_text = font_large.render("Round Over!", True, WHITE)
    round_over_rect = round_over_text.get_rect(center=(screen.get_width() // 2, 200))

    winner_text = font_large.render(f"Winner: {winner_name}", True, YELLOW)
    winner_rect = winner_text.get_rect(center=(screen.get_width() // 2, 300))

    # --- BUTTON SETUP ---
    next_map_button = Button(
        image=None, 
        pos=(640, 500), 
        text_input="Next Map", 
        font=font_small, 
        base_color=WHITE, 
        hovering_color=YELLOW
    )
    
    main_menu_button = Button(
        image=None, 
        pos=(640, 580), 
        text_input="Main Menu", 
        font=font_small, 
        base_color=WHITE, 
        hovering_color=YELLOW
    )

    clock = pygame.time.Clock()
    running = True

    # --- MAIN LOOP ---
    while running:
        mouse_pos = pygame.mouse.get_pos()

        # Draw background and text
        screen.blit(background, (0, 0))
        screen.blit(round_over_text, round_over_rect)
        screen.blit(winner_text, winner_rect)

        # Update and draw buttons
        for button in [next_map_button, main_menu_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_map_button.checkForInput(mouse_pos):
                    pygame.time.delay(200)  # Visual feedback delay
                    
                    # Local import strictly required here to prevent circular dependency
                    import map2
                    map2.load_map2()
                    return  
                    
                elif main_menu_button.checkForInput(mouse_pos):
                    pygame.time.delay(200)
                    pygame.mixer.music.stop()
                    
                    # Local import strictly required here to prevent circular dependency
                    from menu_screen import main_menu
                    main_menu()
                    return  

        pygame.display.flip()
        clock.tick(60)  # Cap frame rate