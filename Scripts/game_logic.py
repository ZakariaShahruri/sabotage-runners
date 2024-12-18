import os
import pygame
import sys
import random
from player import Player
from items import generate_random_item

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
        
        # Set opponents
        self.player1.opponent = self.player2
        self.player2.opponent = self.player1
        
        # Animation lists
        self.idle1 = ["../Images/player1/player1_idle1.png", "../Images/player1/player1_idle2.png", "../Images/player1/player1_idle3.png", "../Images/player1/player1_idle4.png"]
        self.walk1 = ["../Images/player1/player1_walk1.png", "../Images/player1/player1_walk2.png", "../Images/player1/player1_walk3.png", "../Images/player1/player1_walk4.png"]
        self.idle2 = ["../Images/player2/player2_idle1.png", "../Images/player2/player2_idle2.png", "../Images/player2/player2_idle3.png", "../Images/player2/player2_idle4.png"]
        self.run1 = ["../Images/player1/player1_run1.png", "../Images/player1/player1_run2.png", "../Images/player1/player1_run3.png", "../Images/player1/player1_run4.png", "../Images/player1/player1_run5.png", "../Images/player1/player1_run6.png", "../Images/player1/player1_run7.png", "../Images/player1/player1_run8.png"]
        self.run2 = ["../Images/player2/player2_run1.png", "../Images/player2/player2_run2.png", "../Images/player2/player2_run3.png", "../Images/player2/player2_run4.png", "../Images/player2/player2_run5.png", "../Images/player2/player2_run6.png", "../Images/player2/player2_run7.png", "../Images/player2/player2_run8.png"]
        
        # Item management
        self.active_items = []
        self.last_item_spawn_time = pygame.time.get_ticks()
        self.item_spawn_interval = 3000  # 3 seconds between item spawn attempts
        self.max_items = 4

    def manage_items(self, screen):
        """
        Carefully manage item spawning and collision
        
        Args:
            screen (pygame.Surface): Game screen to render items
        """
        current_time = pygame.time.get_ticks()
        
        # Check if it's time to spawn a new item
        if (len(self.active_items) < self.max_items and 
            current_time - self.last_item_spawn_time >= self.item_spawn_interval):
            
            # Generate a new item
            new_item = generate_random_item(self.width, self.height)
            self.active_items.append(new_item)
            
            # Update last spawn time
            self.last_item_spawn_time = current_time

        # Render and check item collisions
        for item in self.active_items[:]:
            item.render(screen)
            if self.player1.check_collision(item):
                item.use(self.player1, self.player2)
                self.active_items.remove(item)
            elif self.player2.check_collision(item):
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

    def handle_movement(self, keys, walls):
        """
        Handle player movement based on key presses
        
        Args:
            keys (pygame.key.ScancodeWrapper): Pressed keys
        """
        self.player1.handle_movement("WASD", keys, self.width, self.height, walls)
        self.player2.handle_movement("arrows", keys, self.width, self.height, walls)

    #animatetion here
    
    def animate_players(self):
        """Animate players with idle animations"""
        if self.player1.is_moving == False:
            self.player1.animate(self.idle1, 0.1)
        else:
            self.player1.animate(self.run1, .2)


        if self.player2.is_moving == False:
            self.player2.animate(self.idle2, 0.1)
        else:
            self.player2.animate(self.run2, .2)


    def render_scores(self, screen):
        """
        Render player scores on the screen
        
        Args:
            screen (pygame.Surface): Game screen to render scores
        """
        # Render scores
        score_font = self.get_font(36)
        player1_score_text = score_font.render(f"Player 1: {self.player2_score}", True, (255, 255, 255))
        player2_score_text = score_font.render(f"Player 2: {self.player1_score}", True, (255, 255, 255))
        screen.blit(player1_score_text, (20, 20))
        screen.blit(player2_score_text, (self.width - 400, 20))

    def reset_item_effects(self, event):
        """
        Reset item effects when specific events occur
        
        Args:
            event (pygame.event.Event): Pygame event
        """
        if event.type == pygame.USEREVENT:
            self.player1.speed = 10
            self.player2.speed = 10
        
        if event.type in [pygame.USEREVENT + i for i in range(1, 6)]:
            self.player1.speed = 10
            self.player2.speed = 10
            self.player1.is_shielded = False
            self.player2.is_shielded = False
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
            'winner': 'Player 1' if self.player1_score >= self.max_score else 'Player 2' if self.player2_score >= self.max_score else None
        }