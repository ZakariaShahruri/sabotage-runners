import pygame
import sys
import random
from button import Button

# --- CONSTANTS ---
BACKGROUND_MUSIC_PATH = "../audios/end_screen_music.mp3"
CLICK_SOUND_PATH = "../audios/click_sound_fx.wav"
BACKGROUND_IMAGE_PATH = "../menu_images/background_darker.png"

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

FIREWORK_COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0),
    (128, 0, 128), (0, 255, 255), (255, 20, 147), (75, 0, 130),
    (255, 105, 180), (255, 255, 255), (255, 140, 0), (173, 216, 230),
    (144, 238, 144), (255, 182, 193)
]

FIREWORK_DIRECTIONS = [
    (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1),
    (2, 1), (1, 2), (-2, 1), (-1, 2), (-2, -1), (-1, -2), (2, -1), (1, -2)
]

class Fireworks:
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        self.fireworks = []
        self.projectiles = []
        self.counter = 0
        self.new_fireworks = True

    def _update_and_draw_particles(self, screen):
        """Handles physics updates and rendering for all firework particles."""
        
        # Iterate backwards through fireworks to safely pop elements without shifting indices
        for i in range(len(self.fireworks) - 1, -1, -1):
            firework = self.fireworks[i]
            x, y, explode_y, delay, color, speed = firework

            if delay < self.counter and y > explode_y:
                pygame.draw.rect(screen, color, [x, y, 10, 10], 0, 3)
                firework[1] -= speed  # Update Y position
            elif y <= explode_y:
                # Explode into projectiles
                for dx, dy in FIREWORK_DIRECTIONS:
                    self.projectiles.append([x, y, dx * 3, dy * 3, color, 60])
                self.fireworks.pop(i)

        # Iterate backwards through projectiles
        for i in range(len(self.projectiles) - 1, -1, -1):
            projectile = self.projectiles[i]
            px, py, dx, dy, color, lifetime = projectile

            # Calculate color fading
            faded_color = (
                max(0, color[0] - (60 - lifetime) * 4),
                max(0, color[1] - (60 - lifetime) * 4),
                max(0, color[2] - (60 - lifetime) * 4),
            )

            pygame.draw.circle(screen, faded_color, (int(px), int(py)), 3)
            
            # Update physics
            projectile[5] -= 1   # Decrease lifetime
            projectile[0] += dx  # Update X
            projectile[1] += dy  # Update Y
            projectile[3] += 0.1 # Apply gravity to dy

            # Remove if dead or off-screen
            if projectile[5] <= 0 or not (0 <= projectile[0] <= self.WIDTH and 0 <= projectile[1] <= self.HEIGHT):
                self.projectiles.pop(i)

    def update(self, screen):
        """Main update loop for the fireworks system."""
        self.counter += 1

        # Spawn new fireworks every 120 frames (2 seconds at 60 FPS)
        if self.counter % 120 == 0:
            self.new_fireworks = True

        if self.new_fireworks:
            for _ in range(30):
                self.fireworks.append([
                    random.randint(10, self.WIDTH - 10), 
                    self.HEIGHT, 
                    random.randint(100, self.HEIGHT // 2),
                    random.randint(0, 300), 
                    random.choice(FIREWORK_COLORS), 
                    random.randint(6, 11)
                ])
            self.new_fireworks = False

        self._update_and_draw_particles(screen)

        # Reset cycle if screen is clear
        if not self.fireworks and not self.projectiles:
            self.counter = 0
            self.new_fireworks = True


def show_end_screen(screen, game_logic, winner_name, get_font):
    """Displays the final game over screen with fireworks and menu options."""
    
    # Audio Setup
    try:
        pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
        pygame.mixer.music.set_volume(0.9)
        pygame.mixer.music.play(-1)
        
        click_sound = pygame.mixer.Sound(CLICK_SOUND_PATH)
        click_sound.set_volume(0.5)
    except pygame.error as e:
        print(f"Warning: Audio load failed in end_screen: {e}")

    # Initialization
    running = True
    clock = pygame.time.Clock()
    fireworks = Fireworks(screen.get_width(), screen.get_height())

    # Asset Loading
    background = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
    
    # Fireworks require an alpha channel surface
    fireworks_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)

    # Fonts & UI
    font_large = get_font(50)
    font_small = get_font(30)

    # True parameter enables antialiasing for smoother text
    round_over_text = font_large.render("Game Over!", True, WHITE)
    winner_text = font_large.render(f"Winner: {winner_name}", True, YELLOW)

    round_over_text_rect = round_over_text.get_rect(center=(screen.get_width() // 2, 200))
    winner_text_rect = winner_text.get_rect(center=(screen.get_width() // 2, 300))

    next_map_button = Button(
        image=None, pos=(640, 500), text_input="Play Again", 
        font=font_small, base_color=WHITE, hovering_color=YELLOW
    )
    main_menu_button = Button(
        image=None, pos=(640, 580), text_input="Main Menu", 
        font=font_small, base_color=WHITE, hovering_color=YELLOW
    )

    # Main Loop
    while running:
        mouse_pos = pygame.mouse.get_pos()

        # Render static background
        screen.blit(background, (0, 0))
        
        # Render dynamic fireworks
        fireworks_surface.fill((0, 0, 0, 0))
        fireworks.update(fireworks_surface)
        screen.blit(fireworks_surface, (0, 0))
        
        # Render UI
        screen.blit(round_over_text, round_over_text_rect)
        screen.blit(winner_text, winner_text_rect)

        for button in [next_map_button, main_menu_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_map_button.checkForInput(mouse_pos):
                    click_sound.play()
                    pygame.time.delay(200)
                    
                    # Local import strictly required here to prevent circular dependency
                    import main
                    main.game_loop()
                    return
                    
                elif main_menu_button.checkForInput(mouse_pos):
                    click_sound.play()
                    pygame.time.delay(200)
                    pygame.mixer.music.stop()
                    
                    # Local import strictly required here to prevent circular dependency
                    from menu_screen import main_menu
                    main_menu()
                    return

        pygame.display.flip()
        clock.tick(60)