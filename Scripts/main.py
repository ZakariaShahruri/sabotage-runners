import os
import sys
import pygame
from button import Button
from game_logic import GameLogic 
from tilemap import *


os.chdir(os.path.dirname(os.path.abspath(__file__)))

MENU_MUSIC = "../audios/menu_music.mp3"
MAIN_MUSIC = "../audios/main_music.mp3"

#getting fonts
def get_font(size):
    return pygame.font.Font("../fonts/font.ttf", size)

# Screen dimensions
WIDTH, HEIGHT = 1280, 720

# Function to play music
def play_music(music_path, loop=True):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1 if loop else 0)
    pygame.mixer.music.set_volume(0.15)

# Function to stop music
def stop_music():
    pygame.mixer.music.stop()


def game_loop():
    # Initialization of pygame
    pygame.init()

    # Play main game music
    play_music(MAIN_MUSIC)

    # Screen setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Sabotage Runners")
    
    # set the background image
    background = pygame.image.load("../Images/default_map.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Create game logic instance
    game_logic = GameLogic(WIDTH, HEIGHT, get_font)
    
    # The game loop
    running = True
    clock = pygame.time.Clock()
    
    # Assign the tilemaps
    first_map = tilemap_1
    
    game_logic.player2.facing_right = False
    while running:
        # Get pressed keys
        keys = pygame.key.get_pressed()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    game_logic.player1.facing_right = False
                if event.key == pygame.K_d:
                    game_logic.player1.facing_right = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    game_logic.player2.facing_right = True
                if event.key == pygame.K_LEFT:
                    game_logic.player2.facing_right = False
       
            # Reset item effects
            game_logic.reset_item_effects(event)
            
        
        # Clear the screen and draw the background
        screen.blit(background, (0, 0))
        # Render players
        game_logic.player1.render(screen)
        game_logic.player2.render(screen)
            
        
        # Render walls
        walls = draw_map(first_map, '../Images/Assets/stone.png', screen)

        # Handle player movement
        game_logic.handle_movement(keys, walls)
        
        # Animate players
        game_logic.animate_players()
        
        # Check for scoringdddddddddd
        game_logic.check_scoring()
        
        # Manage items
        game_logic.manage_items(screen)

        # Render scores
        game_logic.render_scores(screen)

        # Check for game over
        game_state = game_logic.get_game_state()
        if game_state['game_over']:
            # You can add a game over screen or restart logic here
            print(f"{game_state['winner']} wins!")
            menu()

        # Update display
        pygame.display.flip()

        # Limit FPS to 60
        clock.tick(60)

    # Close pygame
    stop_music()
    pygame.quit()
    sys.exit()

def menu():
    # Initialize Pygame
    pygame.init()

        # Play menu music
    play_music(MENU_MUSIC)

    # Screen setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sabotage Runners")
    menu_cover = pygame.image.load("../menu_images/menu_background.png")
    

        
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
                    stop_music()
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
