# PARTICLE EFFECTS
def create_particle(x, y):
    particles = []
    for _ in range(10):  # Adjust number of particles
        particles.append([[x, y], [random.uniform(-2, 2), random.uniform(-2, 2)], random.randint(4, 6)])
    return particles

def draw_particles(particles, screen):
    for particle in particles:
        pygame.draw.circle(screen, (255, 255, 255), particle[0], particle[2])
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1
        if particle[2] <= 0:
            particles.remove(particle)

# SCREEN TRANSITIONS (FADING)
def fade_out(screen):
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 255, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(30)

# SCREEN SHAKE EFFECT
def screen_shake(offset, intensity):
    return random.randint(-intensity, intensity) + offset

# TIMER DISPLAY
def draw_timer(screen, start_time):
    elapsed = (pygame.time.get_ticks() - start_time) // 1000
    font = pygame.font.Font(None, 50)
    timer_surface = font.render(f"Time: {elapsed}", True, (255, 255, 255))
    screen.blit(timer_surface, (10, 10))
