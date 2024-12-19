import os
import sys
import pygame
from button import Button
from game_logic import GameLogic
from menu_screen import main_menu
from round_over import round_over_screen
from collision import *


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
    
    hedges = pygame.image.load("../Images/hedges.png")
    hedges = pygame.transform.scale(hedges, (WIDTH, HEIGHT))


    # Create game logic instance
    game_logic = GameLogic(WIDTH, HEIGHT, get_font)
    
    # The game loop
    running = True
    clock = pygame.time.Clock()

    timer_start = 0
    
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

            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                if not game_logic.player1.attack:  # Start attack only if not already active
                    game_logic.player1.attack = True
                    timer_start = pygame.time.get_ticks()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not game_logic.player2.attack:  # Start attack only if not already active
                    game_logic.player2.attack = True
                    timer_start = pygame.time.get_ticks()

            # Reset item effects
            game_logic.reset_item_effects(event)

        if game_logic.player1.attack:
            current_p1_time = pygame.time.get_ticks()
            elapsed_time = current_p1_time - timer_start
            if elapsed_time >= 750:  # End attack after 300 ms
                game_logic.player1.attack = False
                game_logic.player1.current_frame = 0

        if game_logic.player2.attack:
            current_p2_time = pygame.time.get_ticks()
            elapsed_time = current_p2_time - timer_start
            if elapsed_time >= 750:  # End attack after 300 ms
                game_logic.player2.attack = False
                game_logic.player2.current_frame = 0


        if game_logic.player1.check_collision(game_logic.player2) and game_logic.player2.getting_hit == False:       
            game_logic.player1.knockback(game_logic.player2, knockback_force=150)
            game_logic.player2.getting_hit = True
            cooldown_start = pygame.time.get_ticks()
        
        if game_logic.player2.check_collision(game_logic.player1) and game_logic.player1.getting_hit == False:       
            game_logic.player2.knockback(game_logic.player1, knockback_force=150)
            game_logic.player1.getting_hit = True
            cooldown_start = pygame.time.get_ticks()

        for rectangle in all_rectangles:
                if rectangle.colliderect(game_logic.player2.get_rect()):
                    game_logic.player2.x -= 30
                elif rectangle.colliderect(game_logic.player1.get_rect()):
                    game_logic.player1.x += 30

        if game_logic.player1.getting_hit:
            current_p2_cooldown = pygame.time.get_ticks()
            cooldown_elapsed = current_p2_cooldown - cooldown_start
            if cooldown_elapsed >= 500:
                game_logic.player1.getting_hit = False

        if game_logic.player2.getting_hit:
            current_p1_cooldown = pygame.time.get_ticks()
            cooldown_elapsed = current_p1_cooldown - cooldown_start
            if cooldown_elapsed >= 500:
                game_logic.player2.getting_hit = False

        # Clear the screen and draw the background
        screen.blit(background, (0, 0))
        
        # Render players
        game_logic.player1.render(screen)
        game_logic.player2.render(screen)
            
        screen.blit(hedges, (0,0))
        # Render walls
        borders = render_border(map1_borders, screen)

        # Handle player movement
        game_logic.handle_movement(keys, borders)
        
        # Animate players
        game_logic.animate_players()
        
        # Check for scoringdddddddddd
        game_logic.check_scoring()
        
        # Manage items
        game_logic.manage_items(screen)

        # Render scores
        game_logic.render_scores(screen)

        game_state = game_logic.get_game_state()
        if game_state['game_over']:
            winner = game_state['winner']
            stop_music()  # Stop current music if needed
            round_over_screen(screen, game_logic, winner, get_font)
            play_music(MAIN_MUSIC)  # Restart main music if returning to the game

        # Update display
        pygame.display.flip()

        # Limit FPS to 60
        clock.tick(60)

    # Close pygame
    stop_music()
    pygame.quit()
    sys.exit()
