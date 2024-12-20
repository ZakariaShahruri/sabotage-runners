import pygame
from button import Button
import sys
import random

class Fireworks:
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        self.fireworks = []
        self.projectiles = []
        self.counter = 0
        self.new_fireworks = True
        self.colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0),
            (128, 0, 128), (0, 255, 255), (255, 20, 147), (75, 0, 130),
            (255, 105, 180), (255, 255, 255), (255, 140, 0), (173, 216, 230),
            (144, 238, 144), (255, 182, 193)
        ]
        self.directions = [
            (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1),
            (2, 1), (1, 2), (-2, 1), (-1, 2), (-2, -1), (-1, -2), (2, -1), (1, -2)
        ]

    def draw_fireworks(self, screen):
        remove_fireworks = []

        for i in range(len(self.fireworks)):
            firework = self.fireworks[i]
            x, y, explode_y, delay, color, speed = firework

            if delay < self.counter and y > explode_y:
                pygame.draw.rect(screen, color, [x, y, 10, 10], 0, 3)
                firework[1] -= speed
            elif y <= explode_y:
                for direction in self.directions:
                    dx, dy = direction
                    self.projectiles.append([x, y, dx * 3, dy * 3, color, 60])
                remove_fireworks.append(i)

        for index in reversed(remove_fireworks):
            self.fireworks.pop(index)

        remove_projectiles = []
        for i in range(len(self.projectiles)):
            projectile = self.projectiles[i]
            px, py, dx, dy, color, lifetime = projectile

            faded_color = (
                max(0, color[0] - (60 - lifetime) * 4),
                max(0, color[1] - (60 - lifetime) * 4),
                max(0, color[2] - (60 - lifetime) * 4),
            )

            pygame.draw.circle(screen, faded_color, (int(px), int(py)), 3)
            projectile[5] -= 1
            projectile[0] += dx
            projectile[1] += dy
            projectile[3] += 0.1

            if lifetime <= 0 or not (0 <= px <= self.WIDTH and 0 <= py <= self.HEIGHT):
                remove_projectiles.append(i)

        for index in reversed(remove_projectiles):
            self.projectiles.pop(index)

    def update(self, screen):
        self.counter += 1

    # Spawn new fireworks every 120 frames (2 seconds at 60 FPS)
        if self.counter % 120 == 0:
            self.new_fireworks = True

        if self.new_fireworks:
            for _ in range(30):  # Reduced number of fireworks for less intensity
                self.fireworks.append([
                    random.randint(10, self.WIDTH - 10), 
                    self.HEIGHT, 
                    random.randint(100, self.HEIGHT // 2),
                    random.randint(0, 300), 
                    random.choice(self.colors), 
                    random.randint(6, 11)
                ])
            self.new_fireworks = False

        self.draw_fireworks(screen)

        if len(self.fireworks) == 0 and len(self.projectiles) == 0:
            self.counter = 0
            self.new_fireworks = True

def show_end_screen(screen, game_logic, winner_name, get_font):
    # Load background music
    pygame.mixer.music.load("../audios/end_screen_music.mp3")
    pygame.mixer.music.set_volume(0.9)
    pygame.mixer.music.play(-1)

    # Load click sound effect
    click_sound = pygame.mixer.Sound("../audios/click_sound_fx.wav")
    click_sound.set_volume(0.5)  # Adjust volume as needed

    running = True
    clock = pygame.time.Clock()
    
    # Initialize fireworks
    fireworks = Fireworks(screen.get_width(), screen.get_height())

    # Load background image
    background = pygame.image.load("../menu_images/background_darker.png")
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

    # Button setup
    font = get_font(50)
    button_font = get_font(30)

    next_map_button = Button(
        None, (640, 500), "Play Again", button_font, (255, 255, 255), (255, 255, 0)
    )
    main_menu_button = Button(
        None, (640, 580), "Main Menu", button_font, (255, 255, 255), (255, 255, 0)
    )

    # Create text
    round_over_text = font.render("Game Over!", False, (255, 255, 255))
    winner_text = font.render(f"Winner: {winner_name}", False, (255, 255, 0))

    round_over_text_rect = round_over_text.get_rect(center=(screen.get_width() // 2, 200))
    winner_text_rect = winner_text.get_rect(center=(screen.get_width() // 2, 300))

    # Create a separate surface for fireworks with alpha
    fireworks_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)

    while running:
        # Draw background and UI elements on main screen
        screen.blit(background, (0, 0))
        
        # Clear fireworks surface
        fireworks_surface.fill((0, 0, 0, 0))
        
        # Update and draw fireworks on separate surface
        fireworks.update(fireworks_surface)
        
        # Draw UI elements
        screen.blit(round_over_text, round_over_text_rect)
        screen.blit(winner_text, winner_text_rect)

        # Blit fireworks surface onto main screen
        screen.blit(fireworks_surface, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        next_map_button.changeColor(mouse_pos)
        main_menu_button.changeColor(mouse_pos)
        next_map_button.update(screen)
        main_menu_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if next_map_button.checkForInput(pos):
                    click_sound.play()  # Play click sound
                    pygame.time.delay(200)
                    import main
                    main.game_loop()
                    return
                elif main_menu_button.checkForInput(pos):
                    click_sound.play()  # Play click sound
                    pygame.time.delay(200)
                    pygame.mixer.music.stop()
                    from menu_screen import main_menu
                    main_menu()
                    return

        pygame.display.flip()
        clock.tick(60)