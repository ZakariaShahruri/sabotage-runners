import pygame
from state import State

class Player(State):
    def __init__(self, x, y, path, size=40, speed=10):
        super().__init__(x, y, path, size, is_collidable=True)
        self.speed = speed
        self.path = path
        self.image = pygame.image.load(self.path)
        self.image = pygame.transform.scale(self.image, (52, 91))
        
        # New attributes for item interactions
        self.spawn_x = x
        self.spawn_y = y
        self.is_shielded = False
        self.controls_reversed = False
        self.opponent = None  # Will be set in main game loop
        self.current_frame = 0

    def handle_movement(self, controls, keys, screen_width, screen_height):
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
                if keys[pygame.K_d]:
                    dx = self.speed
                if keys[pygame.K_w]:
                    dy = -self.speed
                if keys[pygame.K_s]:
                    dy = self.speed

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
                if keys[pygame.K_RIGHT]:
                    dx = self.speed
                if keys[pygame.K_UP]:
                    dy = -self.speed
                if keys[pygame.K_DOWN]:
                    dy = self.speed

        # Update position with boundary checking
        self.update(dx, dy, screen_width, screen_height)
        
    
    def animate(self, action, speed):
        self.image = pygame.image.load(action[int(self.current_frame)])
        self.image = pygame.transform.scale(self.image, (52, 91))
        self.current_frame += speed
        if self.current_frame >= len(action):
            self.current_frame = 0