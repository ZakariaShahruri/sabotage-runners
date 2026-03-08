import pygame
from state import State

class Player(State):
    def __init__(self, x, y, path, size=30, speed=5):
        super().__init__(x, y, path, size, is_collidable=True)
        self.speed = speed
        
        # Load and scale initial image
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 48))
        
        # State attributes
        self.facing_right = True
        self.attack = False
        self.hittable = True
        self.getting_hit = False
        self.is_shielded = False
        self.controls_reversed = False
        
        self.spawn_x = x
        self.spawn_y = y
        self.opponent = None
        self.current_frame = 0.0
        
        # Timers
        self.attack_start_time = 0
        self.hit_cooldown_start = 0

    def knockback(self, other_player, knockback_force=150):
        """Apply knockback to another player if attacking."""
        if self.attack:
            direction = 1 if self.facing_right else -1
            other_player.x += knockback_force * direction
    
    def handle_movement(self, controls, keys, screen_width, screen_height, borders):
        """Calculates and applies movement based on input mappings."""
        dx, dy = 0, 0
        
        # Define base mappings
        if controls == "WASD":
            mapping = {
                pygame.K_a: (-self.speed, 0),
                pygame.K_d: (self.speed, 0),
                pygame.K_w: (0, -self.speed),
                pygame.K_s: (0, self.speed)
            }
        elif controls == "arrows":
            mapping = {
                pygame.K_LEFT: (-self.speed, 0),
                pygame.K_RIGHT: (self.speed, 0),
                pygame.K_UP: (0, -self.speed),
                pygame.K_DOWN: (0, self.speed)
            }
        else:
            mapping = {}

        # Reverse controls if affected by an item
        if self.controls_reversed:
            mapping = {key: (-vec[0], -vec[1]) for key, vec in mapping.items()}

        # Calculate intent
        for key, (move_x, move_y) in mapping.items():
            if keys[key]:
                dx += move_x
                dy += move_y

        self.is_moving = (dx != 0 or dy != 0)

        # Apply movement and handle border collisions
        self.update(dx, dy, screen_width, screen_height)
        
        for border_block in borders:
            if self.check_collision(border_block):
                # Revert movement if colliding
                self.update(-dx, -dy, screen_width, screen_height)
                break
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y + 4, self.size - 3, self.size * 1.4)

    def animate(self, animation_frames, speed):
        """
        Loops through pre-loaded animation surfaces.
        :param animation_frames: List of pre-loaded pygame.Surface objects.
        :param speed: Float determining animation speed.
        """
        if not animation_frames:
            return

        self.current_frame += speed
        if self.current_frame >= len(animation_frames):
            self.current_frame = 0
            
        frame_surface = animation_frames[int(self.current_frame)]
        
        if not self.facing_right:
            frame_surface = pygame.transform.flip(frame_surface, True, False)
            
        self.image = pygame.transform.scale(frame_surface, (32, 48))