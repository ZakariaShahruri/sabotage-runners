import os
import sys
import pygame
from button import Button
from game_logic import GameLogic 
from tilemap import *


os.chdir(os.path.dirname(os.path.abspath(__file__)))

#getting fonts
def get_font(size):
    return pygame.font.Font("../fonts/font.ttf", size)

# Screen dimensions
WIDTH, HEIGHT = 1280, 720

def game_loop():
    # Initialization of pygame
    pygame.init()

    # Screen setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Sabotage Runners")
    
    # set the background image
    background = pygame.image.load("../Images/background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Create game logic instance
    game_logic = GameLogic(WIDTH, HEIGHT, get_font)
    
    # The game loop
    running = True
    clock = pygame.time.Clock()
    
    # Draw the map
    first_map = tilemap_1
    walls = draw_map(first_map)

    while running:
        # Get pressed keys
        keys = pygame.key.get_pressed()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Reset item effects
            game_logic.reset_item_effects(event)

        # Clear the screen and draw the background
        screen.blit(background, (0, 0))

        # Handle player movement
        game_logic.handle_movement(keys, walls)
        
        # Animate players
        game_logic.animate_players()
        
        # Check for scoringdddddddddd
        game_logic.check_scoring()
        
        # Manage items
        game_logic.manage_items(screen)

        # Render players
        game_logic.player1.render(screen)
        game_logic.player2.render(screen)

        # Render scores
        game_logic.render_scores(screen)

        # Check for game over
        game_state = game_logic.get_game_state()
        if game_state['game_over']:
            # You can add a game over screen or restart logic here
            print(f"{game_state['winner']} wins!")
            running = False

        # Update display
        pygame.display.flip()

        # Limit FPS to 60
        clock.tick(60)

    # Close pygame
    pygame.quit()
    sys.exit()

def menu():
    # Initialize Pygame
    pygame.init()

    # Screen setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sabotage Runners")
    menu_cover = pygame.image.load("../Images/menucover.png")
    

        
    play_button = Button(image=pygame.image.load("../Images/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    option_button = Button(image=pygame.image.load("../Images/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    quit_button = Button(image=pygame.image.load("../Images/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

    # Menu loop
    running = True
    while running:
        screen.blit(menu_cover, (0, 0))
        
        menu_text = get_font(70).render("Sabotage Runners", True, "#FFD300")
        menu_rect = menu_text.get_rect(center=(640, 100))
        
        screen.blit(menu_text, menu_rect)
        
        menu_mouse_pos = pygame.mouse.get_pos()

        for button in [play_button, option_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    game_loop()
                if option_button.checkForInput(menu_mouse_pos):
                    pass
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
            

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    menu()
