import os
import sys
import pygame
from button import Button
from game_logic import GameLogic
from menu_screen import main_menu
from collision import *
from items import *

def get_font(size):
    return pygame.font.Font("../fonts/font.ttf", size)

WIDTH, HEIGHT = 1280, 720

def play_music(music_path, loop=True):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1 if loop else 0)
    pygame.mixer.music.set_volume(0.10)

def stop_music():
    pygame.mixer.music.stop()

def load_map2():
    # Initialize pygame
    pygame.init()

    # Play main game music
    play_music("../audios/one_vs_one_music.mp3")

    # Screen setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Sabotage Runners - Map 2")
    
    # Set the background image for map 2
    background = pygame.image.load("../Images/tilemapset/map2.png")  # Create this new background image
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    

    # Create game logic instance
    game_logic = GameLogic(WIDTH, HEIGHT, get_font)

    # Change to map 2
    game_logic.change_map(2)
    # Instantiate TeleportItem

    # Game loop
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
                if event.key == pygame.K_RIGHT:
                    game_logic.player2.facing_right = True
                if event.key == pygame.K_LEFT:
                    game_logic.player2.facing_right = False
                if event.key == pygame.K_t and not game_logic.player1.attack:
                    game_logic.player1.attack = True
                    timer_start = pygame.time.get_ticks()
                if event.key == pygame.K_SPACE and not game_logic.player2.attack:
                    game_logic.player2.attack = True
                    timer_start = pygame.time.get_ticks()

            # Reset item effects
            game_logic.reset_item_effects(event)

        # Handle attack timers
        current_time = pygame.time.get_ticks()
        if game_logic.player1.attack and current_time - timer_start >= 750:
            game_logic.player1.attack = False
            game_logic.player1.current_frame = 0
        if game_logic.player2.attack and current_time - timer_start >= 750:
            game_logic.player2.attack = False
            game_logic.player2.current_frame = 0

        # Handle player collisions
        if game_logic.player1.check_collision(game_logic.player2) and not game_logic.player2.getting_hit:
            game_logic.player1.knockback(game_logic.player2, knockback_force=150)
            game_logic.player2.getting_hit = True
            cooldown_start = pygame.time.get_ticks()
        
        if game_logic.player2.check_collision(game_logic.player1) and not game_logic.player1.getting_hit:
            game_logic.player2.knockback(game_logic.player1, knockback_force=150)
            game_logic.player1.getting_hit = True
            cooldown_start = pygame.time.get_ticks()

        # Handle wall collisions
        for rectangle in all_rectangles2:
            if rectangle.colliderect(game_logic.player2.get_rect()):
                game_logic.player2.x -= 30
            elif rectangle.colliderect(game_logic.player1.get_rect()):
                game_logic.player1.x += 30

        # Reset hit status after cooldown
        current_time = pygame.time.get_ticks()
        if game_logic.player1.getting_hit and current_time - cooldown_start >= 500:
            game_logic.player1.getting_hit = False
        if game_logic.player2.getting_hit and current_time - cooldown_start >= 500:
            game_logic.player2.getting_hit = False

        # Clear screen and draw background
        screen.blit(background, (0, 0))
        
        game_logic.render_platform(screen, "map2")
        # Render players
        game_logic.player1.render(screen)
        game_logic.player2.render(screen)

        
        # Render walls using map2 borders
        borders = render_border(map2_borders, screen)

        # Handle player movement
        game_logic.handle_movement(keys, borders)
        
        # Animate players
        game_logic.animate_players()

        # Check for scoring
        game_logic.check_scoring(screen)
        
        # Manage items
        game_logic.manage_items(screen, active_map=2)

        # Render scores
        game_logic.render_scores(screen)

        # Check game state
        game_state = game_logic.get_game_state()
        if game_state['game_over']:
            winner = game_state['winner']
            stop_music()
            from end_screen import show_end_screen
            show_end_screen(screen, game_logic, winner, get_font)
            play_music("../audios/main_music.mp3")



        # Update display
        pygame.display.flip()
        clock.tick(60)

    # Close pygame
    stop_music()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    load_map2()



