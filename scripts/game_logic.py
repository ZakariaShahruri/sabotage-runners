import pygame
from player import Player
from items import *
from sound_effects import SoundEffects

class GameLogic:
    def __init__(self, width, height, get_font):
        self.width = width
        self.height = height
        self.get_font = get_font
        
        self.player1_score = 0
        self.player2_score = 0
        self.max_score = 3 
        self.game_over = False
        
        self.spawn_positions = {
            1: {'player1': (20, 300), 'player2': (1200, 300)},
            2: {'player1': (0, 322), 'player2': (1280, 322)}
        }
        
        self.active_map = 1
        
        # Initialize players
        p1_spawn = self.spawn_positions[self.active_map]['player1']
        p2_spawn = self.spawn_positions[self.active_map]['player2']
        
        self.player1 = Player(x=p1_spawn[0], y=p1_spawn[1], path="../images/player1/player1_idle1.png")
        self.player2 = Player(x=p2_spawn[0], y=p2_spawn[1], path="../images/player2/player2_idle1.png")
        self.player2.image = pygame.transform.flip(self.player2.image, True, False)
        
        self.player1.opponent = self.player2
        self.player2.opponent = self.player1
        
        # Load animations into memory ONCE to prevent severe FPS drops
        self.animations = {
            'p1_idle': self._load_frames("../images/player1/player1_idle", 4),
            'p1_walk': self._load_frames("../images/player1/player1_walk", 4),
            'p1_run': self._load_frames("../images/player1/player1_run", 8),
            'p1_attack': self._load_frames("../images/player1/player1_attack", 8),
            'p2_idle': self._load_frames("../images/player2/player2_idle", 4),
            'p2_run': self._load_frames("../images/player2/player2_run", 8),
            'p2_attack': self._load_frames("../images/player2/player2_attack", 8)
        }
        
        # Item management
        self.active_items = []
        self.last_item_spawn_time = pygame.time.get_ticks()
        self.item_spawn_interval = 3000
        self.max_items = 4
        self.sound_effects = SoundEffects()

    def _load_frames(self, base_path, count):
        """Helper to preload images as Pygame surfaces."""
        frames = []
        for i in range(1, count + 1):
            frames.append(pygame.image.load(f"{base_path}{i}.png").convert_alpha())
        return frames

    def manage_items(self, screen, active_map=None):
        if active_map is None:
            active_map = self.active_map
            
        current_time = pygame.time.get_ticks()

        # Spawn logic
        if (len(self.active_items) < self.max_items and 
            current_time - self.last_item_spawn_time >= self.item_spawn_interval):
            new_item = generate_random_item(self.width, self.height, active_map)
            if new_item:
                self.active_items.append(new_item)
                self.last_item_spawn_time = current_time

        # Collision and effect logic
        for item in self.active_items[:]:
            item.render(screen)
            
            p1_hit = self.player1.check_collision(item)
            p2_hit = self.player2.check_collision(item)
            
            if p1_hit or p2_hit:
                spawn_coord = (item.x, item.y)
                
                # Apply sound effects
                sound_mapping = {
                    FreezeItem: self.sound_effects.play_freeze,
                    SpeedUpItem: self.sound_effects.play_speed_up,
                    SlowDownItem: self.sound_effects.play_slow_down,
                    MirrorItem: self.sound_effects.play_mirrored,
                    TeleportItem: self.sound_effects.play_teleport
                }
                sound_mapping.get(type(item), lambda: None)()
                    
                # Apply item effects
                if p1_hit:
                    item.use(activator=self.player1, target=self.player2)
                else:
                    item.use(activator=self.player2, target=self.player1)
                    
                self.active_items.remove(item)
                if spawn_coord in occupied_spawn_points[active_map]:
                    occupied_spawn_points[active_map][spawn_coord] = False

    def reset_players(self):
        self.player1.x, self.player1.y = self.spawn_positions[self.active_map]['player1']
        self.player2.x, self.player2.y = self.spawn_positions[self.active_map]['player2']

    def check_scoring(self, screen):
        point_scored = False
        
        if self.player1.x + self.player1.size >= self.width:
            self.player2_score += 1
            point_scored = True
            
        elif self.player2.x <= 0:
            self.player1_score += 1
            point_scored = True
            
        if point_scored:
            self.reset_players()
            self.screen_shake(screen)
            self.sound_effects.play_score_audio()
        
        if self.player1_score >= self.max_score or self.player2_score >= self.max_score:
            self.game_over = True
        
        return point_scored

    def handle_movement(self, keys, borders):
        self.player1.handle_movement("WASD", keys, self.width, self.height, borders)
        self.player2.handle_movement("arrows", keys, self.width, self.height, borders)
    
    def animate_players(self):
        # Player 1 Animation
        if self.player1.attack:
            self.player1.animate(self.animations['p1_attack'], 0.5)
        elif self.player1.is_moving:
            self.player1.animate(self.animations['p1_run'], 0.2)
        else:
            self.player1.animate(self.animations['p1_idle'], 0.1)

        # Player 2 Animation
        if self.player2.attack:
            self.player2.animate(self.animations['p2_attack'], 0.5)
        elif self.player2.is_moving:
            self.player2.animate(self.animations['p2_run'], 0.2)
        else:
            self.player2.animate(self.animations['p2_idle'], 0.1)

    def render_scores(self, screen):
        scoreboard = pygame.image.load("../images/scoreboard_sign.png").convert_alpha()
        scoreboard = pygame.transform.scale(scoreboard, (84, 95))
        screen.blit(scoreboard, (593, 0))
        
        score_font = self.get_font(25)
        player1_score_text = score_font.render(str(self.player2_score), True, (255, 0, 0))
        player2_score_text = score_font.render(str(self.player1_score), True, (0, 0, 255))
        
        screen.blit(player1_score_text, (605, 55))
        screen.blit(player2_score_text, (self.width - 635, 55))
        
    def render_platform(self, screen, map_name):
        platform_image = pygame.image.load("../assets/platform.png").convert_alpha()
        
        platforms = {
            "map1": [(266, 560), (625, 560), (1000, 560), (625, 138), (266, 138), (1000, 138)],
            "map2": [(175, 186), (175, 493), (602, 164), (602, 516), (1038, 493), (1038, 186)]
        }
        
        for pos in platforms.get(map_name, []):
            screen.blit(platform_image, pos)
            
    def render_shadow(self, screen, player):
        shadow_image = pygame.image.load("../images/shadow.png").convert_alpha()
        shadow_image = pygame.transform.scale(shadow_image, (32, 15))
        screen.blit(shadow_image, (player.x, player.y + 42))
   
    def reset_item_effects(self, event):
        if event.type in [pygame.USEREVENT + i for i in range(1, 6)]:
            self.player1.speed = 5
            self.player2.speed = 5
            self.player1.controls_reversed = False
            self.player2.controls_reversed = False

    def get_game_state(self):
        winner = None
        if self.player2_score >= self.max_score:
            winner = 'Player 1'
        elif self.player1_score >= self.max_score:
            winner = 'Player 2'
            
        return {
            'player1_score': self.player1_score,
            'player2_score': self.player2_score,
            'game_over': self.game_over,
            'winner': winner
        }

    def change_map(self, new_map):
        self.active_map = new_map
        self.player1.spawn_x, self.player1.spawn_y = self.spawn_positions[new_map]['player1']
        self.player2.spawn_x, self.player2.spawn_y = self.spawn_positions[new_map]['player2']
        self.reset_players()

    def screen_shake(self, screen, intensity=10, duration=30):
        start_time = pygame.time.get_ticks()
        original_surface = pygame.Surface.copy(screen)
        
        while pygame.time.get_ticks() - start_time < duration:
            offset_x = intensity if pygame.time.get_ticks() % 2 == 0 else -intensity
            offset_y = intensity if pygame.time.get_ticks() % 3 == 0 else -intensity
            
            screen.blit(original_surface, (offset_x, offset_y))
            pygame.display.flip()

    def render_instruction(self, screen):
        instruction_font = self.get_font(16)
        text = "GET TO THE OTHER PLAYER'S SPAWN"
        
        instruction_surface = instruction_font.render(text, True, (255, 255, 255))
        outline_surface = instruction_font.render(text, True, (0, 0, 0))
        text_rect = instruction_surface.get_rect(center=(self.width // 2, 20))

        # Outline
        for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            screen.blit(outline_surface, text_rect.move(dx, dy))

        screen.blit(instruction_surface, text_rect)