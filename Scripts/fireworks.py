import random
import pygame

pygame.init()
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Fireworks!')
fps = 60
timer = pygame.time.Clock()

# Fireworks related variables
fireworks = []
counter = 0
new_fireworks = True
colors = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0),
    (128, 0, 128), (0, 255, 255), (255, 20, 147), (75, 0, 130),
    (255, 105, 180), (255, 255, 255), (255, 140, 0), (173, 216, 230),
    (144, 238, 144), (255, 182, 193)
]
projectiles = []
directions = [
    (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1),
    (2, 1), (1, 2), (-2, 1), (-1, 2), (-2, -1), (-1, -2), (2, -1), (1, -2)
]


def draw_fireworks(firework_list, projectile_list, frame_counter):
    remove_fireworks = []

    for i in range(len(firework_list)):
        firework = firework_list[i]
        x, y, explode_y, delay, color, speed = firework

        if delay < frame_counter and y > explode_y:
            pygame.draw.rect(screen, color, [x, y, 10, 10], 0, 3)
            firework[1] -= speed  # Move upward
        elif y <= explode_y:
            for direction in directions:
                dx, dy = direction
                projectile_list.append([x, y, dx * 3, dy * 3, color, 60])  # Add projectiles
            remove_fireworks.append(i)

    for index in reversed(remove_fireworks):
        firework_list.pop(index)

    remove_projectiles = []
    for i in range(len(projectile_list)):
        projectile = projectile_list[i]
        px, py, dx, dy, color, lifetime = projectile

        # Gradual fade effect for the color
        faded_color = (
            max(0, color[0] - (60 - lifetime) * 4),
            max(0, color[1] - (60 - lifetime) * 4),
            max(0, color[2] - (60 - lifetime) * 4),
        )

        pygame.draw.circle(screen, faded_color, (int(px), int(py)), 3)
        projectile[5] -= 1  # Decrease lifetime
        projectile[0] += dx  # Update x position
        projectile[1] += dy  # Update y position
        projectile[3] += 0.1  # Simulate gravity

        if lifetime <= 0 or not (0 <= px <= WIDTH and 0 <= py <= HEIGHT):
            remove_projectiles.append(i)

    for index in reversed(remove_projectiles):
        projectile_list.pop(index)

    return firework_list, projectile_list


run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    counter += 1

    if new_fireworks:
        for _ in range(30):
            fireworks.append([
                random.randint(10, WIDTH - 10), HEIGHT, random.randint(100, HEIGHT // 2),
                random.randint(0, 300), random.choice(colors), random.randint(6, 11)
            ])
        new_fireworks = False

    fireworks, projectiles = draw_fireworks(fireworks, projectiles, counter)

    if len(fireworks) == 0 and len(projectiles) == 0:
        counter = 0
        new_fireworks = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
