import pygame
from state import State

class Player(State):
    def __init__(self, x, y, size=40, color=(0, 255, 0), speed=5):
        super().__init__(x, y, size, color, is_collidable=True)
        self.speed = speed

    def handle_movement(self, controls, keys, screen_width, screen_height):
        # Reset movement
        dx = 0
        dy = 0

        # Check movement keys
        if controls == "WASD":
            if keys[pygame.K_a]:
                dx = -self.speed
            if keys[pygame.K_d]:
                dx = self.speed
            if keys[pygame.K_w]:
                dy = -self.speed
            if keys[pygame.K_s]:
                dy = self.speed

        elif controls == "arrows":
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







        