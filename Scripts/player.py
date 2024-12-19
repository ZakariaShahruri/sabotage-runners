import pygame
from state import State

class Player(State):
    def __init__(self, x, y, path, size=30, speed=5):
        super().__init__(x, y, path, size, is_collidable=True)
        self.speed = speed
        self.path = path
        self.image = pygame.image.load(self.path)
        self.image = pygame.transform.scale(self.image, (32, 48))
        self.facing_right = True
        self.attack = False
        self.hittable = True
        
        
        # New attributes for item interactions
        self.spawn_x = x
        self.spawn_y = y
        self.is_shielded = False
        self.controls_reversed = False
        self.opponent = None  # Will be set in main game loop
        self.current_frame = 0
        self.getting_hit = False

    def knockback(self, other_player, knockback_force=50):
        """Apply knockback to another player."""
        if self.attack:
            if self.facing_right:
                other_player.x += knockback_force  # Push to the right
            else:
                other_player.x -= knockback_force

    def handle_movement(self, controls, keys, screen_width, screen_height, walls):
        # Reset movement
        dx = 0
        dy = 0

        # Check movement keys, taking into account potential control reversal
        if controls == "WASD":
            # If controls are reversed, swap the keys
            if self.controls_reversed:
                if keys[pygame.K_d]:
                    dx = -self.speed
                if keys[pygame.K_a]:
                    dx = self.speed
                if keys[pygame.K_s]:
                    dy = -self.speed
                if keys[pygame.K_w]:
                    dy = self.speed
            else:
                if keys[pygame.K_a]:
                    dx = -self.speed
                    self.is_moving = True
                if keys[pygame.K_d]:
                    dx = self.speed
                    self.is_moving = True
                if keys[pygame.K_w]:
                    dy = -self.speed
                    self.is_moving = True
                if keys[pygame.K_s]:
                    dy = self.speed
                    self.is_moving = True
                if not keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d]:
                    self.is_moving = False

        elif controls == "arrows":
            # If controls are reversed, swap the keys
            if self.controls_reversed:
                if keys[pygame.K_RIGHT]:
                    dx = -self.speed
                if keys[pygame.K_LEFT]:
                    dx = self.speed
                if keys[pygame.K_DOWN]:
                    dy = -self.speed
                if keys[pygame.K_UP]:
                    dy = self.speed
            else:
                if keys[pygame.K_LEFT]:
                    dx = -self.speed
                    self.is_moving = True
                if keys[pygame.K_RIGHT]:
                    dx = self.speed
                    self.is_moving = True
                if keys[pygame.K_UP]:
                    dy = -self.speed
                    self.is_moving = True
                if keys[pygame.K_DOWN]:
                    dy = self.speed
                    self.is_moving = True
                if not keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT]:
                    self.is_moving = False

        # Update position with boundary checking
        self.update(dx, dy, screen_width, screen_height)
        
        for wall in walls:
            if self.check_collision(wall):
                self.update(-dx, -dy, screen_width, screen_height)
                break
    
    def animate(self, action, speed):
            self.current_frame += speed
            self.current_frame %= len(action)
            if self.current_frame >= len(action):
                self.current_frame = 0
                
            if self.facing_right == True:
                self.image = pygame.image.load(action[int(self.current_frame)])
                self.image = pygame.transform.scale(self.image, (32, 48))
            elif self.facing_right == False:
                self.image = pygame.image.load(action[int(self.current_frame)])
                self.image = pygame.transform.flip(self.image, True, False)
                self.image = pygame.transform.scale(self.image, (32, 48))