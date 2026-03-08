import pygame

class State:
    """
    Base class for physical game objects (Players, Items, Walls).
    """
    def __init__(self, x, y, path, size=40, is_collidable=False):
        """
        Args:
            x (float): Initial x position
            y (float): Initial y position
            path (str): File path to the image asset
            size (int, optional): Size of the object (assumes square). Defaults to 40.
            is_collidable (bool, optional): Whether the object can collide with others. Defaults to False.
        """
        self.x = x
        self.y = y
        self.path = path
        
        # .convert_alpha() significantly speeds up rendering for images with transparency
        self.image = pygame.image.load(self.path).convert_alpha()
        
        self.size = size
        self.is_collidable = is_collidable
        self.speed = 0

    def update(self, dx=0, dy=0, screen_width=None, screen_height=None):
        """
        Update object's position with optional boundary checking.

        Args:
            dx (float, optional): Change in x position. Defaults to 0.
            dy (float, optional): Change in y position. Defaults to 0.
            screen_width (int, optional): Screen width for boundary checking.
            screen_height (int, optional): Screen height for boundary checking.
        """
        self.x += dx
        self.y += dy

        # Optional boundary checking
        if screen_width is not None:
            self.x = max(0, min(self.x, screen_width - self.size))
        if screen_height is not None:
            self.y = max(0, min(self.y, screen_height - self.size))

    def render(self, screen):
        """Draws the state object onto the provided screen."""
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        """Returns the pygame.Rect bounding box for collisions."""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def check_collision(self, other):
        """
        Check collision with another State object.
        
        Args:
            other (State): Another game object to check collision with.
        Returns:
            bool: True if objects collide, False otherwise.
        """
        if not self.is_collidable or not getattr(other, 'is_collidable', False):
            return False
        
        return self.get_rect().colliderect(other.get_rect())