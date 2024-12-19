
import pygame
import sys
import random
from player import Player
from items import *
from sound_effects import SoundEffects

class GameLogic:
    def __init__(self, width, height, get_font):
        """
        Initialize game logic with screen dimensions and font function
        
        Args:
            width (int): Screen width
            height (int): Screen height
            get_font (function): Function to load fonts
        """
        self.width = width
        self.height = height
        self.get_font = get_font
        
        # Scoring and game state
        self.player1_score = 0
        self.player2_score = 0
        self.max_score = 5  # Win condition
        self.game_over = False
        
        # Create players
        self.player1 = Player(path="../Images/player1/player1_idle1.png", x=20, y=300)
        self.player2 = Player(path="../Images/player2/player2_idle1.png", x=1200, y=300)
        self.player2.image = pygame.transform.flip(self.player2.image, True, False)
        
        # Set opponents
        self.player1.opponent = self.player2
        self.player2.opponent = self.player1
        
        # Animation lists
        self.idle1 = ["../Images/player1/player1_idle1.png", "../Images/player1/player1_idle2.png", "../Images/player1/player1_idle3.png", "../Images/player1/player1_idle4.png"]
        self.walk1 = ["../Images/player1/player1_walk1.png", "../Images/player1/player1_walk2.png", "../Images/player1/player1_walk3.png", "../Images/player1/player1_walk4.png"]
        self.idle2 = ["../Images/player2/player2_idle1.png", "../Images/player2/player2_idle2.png", "../Images/player2/player2_idle3.png", "../Images/player2/player2_idle4.png"]
        self.run1 = ["../Images/player1/player1_run1.png", "../Images/player1/player1_run2.png", "../Images/player1/player1_run3.png", "../Images/player1/player1_run4.png", "../Images/player1/player1_run5.png", "../Images/player1/player1_run6.png", "../Images/player1/player1_run7.png", "../Images/player1/player1_run8.png"]
        self.run2 = ["../Images/player2/player2_run1.png", "../Images/player2/player2_run2.png", "../Images/player2/player2_run3.png", "../Images/player2/player2_run4.png", "../Images/player2/player2_run5.png", "../Images/player2/player2_run6.png", "../Images/player2/player2_run7.png", "../Images/player2/player2_run8.png"]
        self.attack1 = ["../Images/player1/player1_attack1.png", "../Images/player1/player1_attack2.png", "../Images/player1/player1_attack3.png", "../Images/player1/player1_attack4.png", "../Images/player1/player1_attack5.png", "../Images/player1/player1_attack6.png", "../Images/player1/player1_attack7.png", "../Images/player1/player1_attack8.png"]
        self.attack2 = ["../Images/player2/player2_attack1.png", "../Images/player2/player2_attack2.png", "../Images/player2/player2_attack3.png", "../Images/player2/player2_attack4.png", "../Images/player2/player2_attack5.png", "../Images/player2/player2_attack6.png", "../Images/player2/player2_attack7.png", "../Images/player2/player2_attack8.png"]
        
        # Item management
        self.active_items = []
        self.last_item_spawn_time = pygame.time.get_ticks()
        self.item_spawn_interval = 3000  # 3 seconds between item spawn attempts
        self.max_items = 4
        self.sound_effects = SoundEffects()

    def manage_items(self, screen):
        current_time = pygame.time.get_ticks()

        # Check if it's time to spawn a new item
        if (len(self.active_items) < self.max_items and 
            current_time - self.last_item_spawn_time >= self.item_spawn_interval):
            # Generate a new item
            new_item = generate_random_item(self.width, self.height)
            if new_item:
                self.active_items.append(new_item)
                # Update last spawn time
                self.last_item_spawn_time = current_time

        # Render and check item collisions
        for item in self.active_items[:]:
            item.render(screen)
            if self.player1.check_collision(item) or self.player2.check_collision(item):
                # Mark the spawn point as available again
                occupied_spawn_points[(item.x, item.y)] = False
                
                # Play the appropriate sound based on item type
                if isinstance(item, FreezeItem):
                    self.sound_effects.play_freeze()
                elif isinstance(item, SpeedUpItem):
                    self.sound_effects.play_speed_up()
                elif isinstance(item, SlowDownItem):
                    self.sound_effects.play_slow_down()
                elif isinstance(item, MirrorItem):
                    self.sound_effects.play_mirrored()
                elif isinstance(item, TeleportItem):
                    self.sound_effects.play_teleport()
                    
                # Apply the item effect
                if self.player1.check_collision(item):
                    item.use(self.player1, self.player2)
                else:
                    item.use(self.player2, self.player1)
                self.active_items.remove(item)

   
   
   
    def reset_players(self):
        """Reset players to their initial positions"""
        self.player1.x = 20
        self.player1.y = 300
        self.player2.x = 1200
        self.player2.y = 300

    def check_scoring(self):
        """
        Check if players have scored and update scores
        
        Returns:
            bool: True if a point was scored, False otherwise
        """
        point_scored = False
        
        if self.player1.x + self.player1.size >= self.width:
            # Player 1 reaches right side, Player 2 scores
            self.player2_score += 1
            point_scored = True
            self.reset_players()
        
        if self.player2.x <= 0:
            # Player 2 reaches left side, Player 1 scores
            self.player1_score += 1
            point_scored = True
            self.reset_players()
        
        # Check for game over
        if self.player1_score >= self.max_score or self.player2_score >= self.max_score:
            self.game_over = True
        
        return point_scored

    def handle_movement(self, keys, borders):
        """
        Handle player movement based on key presses
        
        Args:
            keys (pygame.key.ScancodeWrapper): Pressed keys
        """
        self.player1.handle_movement("WASD", keys, self.width, self.height, borders)
        self.player2.handle_movement("arrows", keys, self.width, self.height, borders)

    #animatetion here
    
    def animate_players(self):
        """Animate players with idle animations"""
        if self.player1.is_moving == True and self.player1.attack == True:
            self.player1.animate(self.attack1, 0.5)
        elif self.player1.is_moving == True:
            self.player1.animate(self.run1, .2)
        elif self.player1.is_moving == False and self.player1.attack == True:
            self.player1.animate(self.attack1, 0.5)
        else:
            self.player1.animate(self.idle1, .1)

        if self.player2.is_moving == True and self.player2.attack == True:
            self.player2.animate(self.attack2, 0.5)
        elif self.player2.is_moving == True:
            self.player2.animate(self.run2, .2)
        elif self.player2.is_moving == False and self.player2.attack == True:
            self.player2.animate(self.attack2, 0.5)
        else:
            self.player2.animate(self.idle2, .1)



    def render_scores(self, screen):
        """
        Render player scores on the screen
        
        Args:
            screen (pygame.Surface): Game screen to render scores
        """
        # Render scores
        scoreboard = pygame.image.load("../Images/scoreboard_sign.png")
        scoreboard = pygame.transform.scale(scoreboard,(84,95))
        screen.blit(scoreboard, (593,0))
        score_font = self.get_font(25)
        player1_score_text = score_font.render(f"{self.player2_score}", True, (255, 255, 255))
        player2_score_text = score_font.render(f"{self.player1_score}", True, (255, 255, 255))
        screen.blit(player1_score_text, (605, 55))
        screen.blit(player2_score_text, (self.width - 635, 55))

   
   
   
    def reset_item_effects(self, event):
        """
        Reset item effects when specific events occur
        
        Args:
            event (pygame.event.Event): Pygame event
        """
        if event.type == pygame.USEREVENT:
            self.player1.speed = 5
            self.player2.speed = 5
        
        if event.type in [pygame.USEREVENT + i for i in range(1, 6)]:
            self.player1.speed = 5
            self.player2.speed = 5
            self.player1.controls_reversed = False
            self.player2.controls_reversed = False

    def get_game_state(self):
        """
        Get the current game state
        
        Returns:
            dict: Game state information
        """
        return {
            'player1_score': self.player1_score,
            'player2_score': self.player2_score,
            'game_over': self.game_over,
            'winner': 'Player 1' if self.player2_score >= self.max_score else 'Player 2' if self.player1_score >= self.max_score else None
        }