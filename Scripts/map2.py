import os
import sys
import pygame
from button import Button
from game_logic import GameLogic
from collision import *
from items import *
from menu_screen import screen  # Restored missing import!

# --- CONFIGURATION & CONSTANTS ---
WIDTH, HEIGHT = 1280, 720
FPS_LIMIT = 60
ATTACK_DURATION_MS = 750
HIT_COOLDOWN_MS = 500

MAP2_MUSIC = "../audios/one_vs_one_music.mp3"
MAIN_MUSIC = "../audios/main_music.mp3"
BACKGROUND_IMAGE_PATH = "../Images/tilemapset/map2.png"

def get_font(size):
    return pygame.font.Font("../fonts/font.ttf", size)

def play_music(music_path, loop=True):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1 if loop else 0)
    pygame.mixer.music.set_volume(0.5)

def stop_music():
    pygame.mixer.music.stop()

def handle_collisions(game_logic, current_time):
    """Handles logic for physical collisions and knockbacks between players and walls."""
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

    # Player vs Environment Bounds (Map 2 specific)
    for rectangle in all_rectangles2:
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


def load_map2():
    pygame.init()
    play_music(MAP2_MUSIC)
    
    # Load and scale background
    background = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    
    # Initialize game logic
    game_logic = GameLogic(WIDTH, HEIGHT, get_font)
    game_logic.change_map(2)
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
        
        # Determine player movement
        borders = render_border(map2_borders, screen) # Uses the imported screen
        game_logic.handle_movement(keys, borders)
        
        game_logic.animate_players()
        game_logic.check_scoring(screen)

        # ==========================================
        # 3. RENDERING
        # ==========================================
        screen.blit(background, (0, 0))
        game_logic.render_platform(screen, "map2")
        
        game_logic.render_shadow(screen, game_logic.player1)
        game_logic.render_shadow(screen, game_logic.player2)
        
        game_logic.player1.render(screen)
        game_logic.player2.render(screen)
        
        game_logic.manage_items(screen, active_map=2)
        game_logic.render_scores(screen)
        game_logic.render_instruction(screen)

        # Check Win State
        game_state = game_logic.get_game_state()
        if game_state['game_over']:
            stop_music()
            # Local import required to prevent circular dependency
            from end_screen import show_end_screen
            show_end_screen(screen, game_logic, game_state['winner'], get_font)
            play_music(MAIN_MUSIC)

        pygame.display.flip()
        clock.tick(FPS_LIMIT)

    stop_music()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    load_map2()