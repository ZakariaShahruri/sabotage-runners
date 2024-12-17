import pygame

class Player:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.image = pygame.image.load('images/Unarmed_Walk_full.png')
        self.image = pygame.transform.scale(self.image, (113, 200))
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def handle_movement(self, keys, screen_width, screen_height):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed

        # Keep player within screen bounds
        self.x = max(0, min(self.x, screen_width - self.size))
        self.y = max(0, min(self.y, screen_height - self.size))

    # def draw(self, surface):
    #     pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))







        