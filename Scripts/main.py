import os
import sys
import pygame
from button import Button
from game_logic import GameLogic
from menu_screen import main_menu
from round_over import round_over_screen
from collision import *
from items import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- CONFIGURATION & CONSTANTS ---
WIDTH, HEIGHT = 1280, 720
FPS_LIMIT = 60
ATTACK_DURATION_MS = 750
HIT_COOLDOWN_MS = 500

MENU_MUSIC = "../audios/menu_music.mp3"
MAIN_MUSIC = "../audios/main_music.mp3"

def get_font(size):
    return pygame.font.Font("../fonts/font.ttf", size)

def play_music(music_path, loop=True):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1 if loop else 0)
    pygame.mixer.music.set_volume(0.5)

def stop_music():
    pygame.mixer.music.stop()

def handle_collisions(game_logic, current_time):
    """Handles logic for physical collisions and knockbacks between players."""
    p1, p2 = game_logic.player1, game_logic.player2
    
    # Player vs Player Knockback
    if p1.check_collision(p2) and not p2.getting_hit:
        p1.knockback(p2, knockback_force=150)
        p2.getting_hit = True
        p2.hit_cooldown_start = current_time

    if p2.check_collision(p1) and not p1.getting_hit:
        p2.knockback(p1, knockback_force=150)
        p1.getting_hit = True
        p1.hit_cooldown_start = current_time

    # Player vs Environment Bounds (from collision module)
    for rectangle in all_rectangles1:
        if rectangle.colliderect(p2.get_rect()):
            p2.x -= 30
        elif rectangle.colliderect(p1.get_rect()):
            p1.x += 30

def update_player_states(game_logic, current_time):
    """Updates attack timers and i-frame cooldowns for players."""
    for player in (game_logic.player1, game_logic.player2):
        # Reset attacks
        if player.attack and (current_time - player.attack_start_time >= ATTACK_DURATION_MS):
            player.attack = False
            player.current_frame = 0
            
        # Reset hit immunity cooldowns
        if player.getting_hit and (current_time - player.hit_cooldown_start >= HIT_COOLDOWN_MS):
            player.getting_hit = False


def game_loop():
    pygame.init()
    play_music(MAIN_MUSIC)

    # Screen setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Sabotage Runners")
    
    # Load and scale static background elements
    background = pygame.transform.scale(pygame.image.load("../Images/tilemapset/default_map.png").convert(), (WIDTH, HEIGHT))
    hedges = pygame.transform.scale(pygame.image.load("../Images/tilemapset/hedges.png").convert_alpha(), (WIDTH, HEIGHT))

    game_logic = GameLogic(WIDTH, HEIGHT, get_font)
    game_logic.player2.facing_right = False
    
    clock = pygame.time.Clock()
    running = True

    while running:
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        # ==========================================
        # 1. EVENT HANDLING
        # ==========================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                # Orientation
                if event.key == pygame.K_a: game_logic.player1.facing_right = False
                if event.key == pygame.K_d: game_logic.player1.facing_right = True
                if event.key == pygame.K_LEFT: game_logic.player2.facing_right = False
                if event.key == pygame.K_RIGHT: game_logic.player2.facing_right = True

                # Attacks
                if event.key == pygame.K_q and not game_logic.player1.attack:
                    game_logic.player1.attack = True
                    game_logic.player1.attack_start_time = current_time

                if event.key == pygame.K_RSHIFT and not game_logic.player2.attack:
                    game_logic.player2.attack = True
                    game_logic.player2.attack_start_time = current_time

            # Reset item effects
            game_logic.reset_item_effects(event)

        # ==========================================
        # 2. LOGIC UPDATES
        # ==========================================
        update_player_states(game_logic, current_time)
        handle_collisions(game_logic, current_time)
        
        # Player movement
        borders = render_border(map1_borders, screen) # Preserved external call
        game_logic.handle_movement(keys, borders)
        
        game_logic.animate_players()
        game_logic.check_scoring(screen)

        # ==========================================
        # 3. RENDERING
        # ==========================================
        screen.blit(background, (0, 0))
        game_logic.render_platform(screen, "map1")
        
        game_logic.render_shadow(screen, game_logic.player1)
        game_logic.render_shadow(screen, game_logic.player2)
        
        game_logic.player1.render(screen)
        game_logic.player2.render(screen)
        
        screen.blit(hedges, (0, 0))
        game_logic.manage_items(screen)
        game_logic.render_scores(screen)
        game_logic.render_instruction(screen)

        # Check Win State
        game_state = game_logic.get_game_state()
        if game_state['game_over']:
            stop_music()
            round_over_screen(screen, game_logic, game_state['winner'], get_font)
            play_music(MAIN_MUSIC) 

        pygame.display.flip()
        clock.tick(FPS_LIMIT)

    stop_music()
    pygame.quit()
    sys.exit()