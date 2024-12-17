import pygame

class State:
    def __init__(self, x, y, path, size=40, is_collidable=False):
        """
        Base class for game objects
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
            size (int, optional): Size of the object (assumes square). Defaults to 40.
            color (tuple, optional): RGB color of the object. Defaults to green.
            is_collidable (bool, optional): Whether the object can collide with others. Defaults to False.
        """
        self.x = x
        self.y = y
        self.path = path
        self.image = pygame.image.load(self.path)
        self.size = size
        self.is_collidable = is_collidable
        self.speed = 0  # Default speed, can be overridden

    def update(self, dx=0, dy=0, screen_width=None, screen_height=None):
        """
        Update object's position with optional boundary checking

        Args:
            dx (float, optional): Change in x position. Defaults to 0.
            dy (float, optional): Change in y position. Defaults to 0.
            screen_width (int, optional): Screen width for boundary checking
            screen_height (int, optional): Screen height for boundary checking
        """
        self.x += dx
        self.y += dy

        # Optional boundary checking
        # if screen_width is not None:
        #     self.x = max(0, min(self.x, screen_width - self.size))
        # if screen_height is not None:
        #     self.y = max(0, min(self.y, screen_height - self.size))

    def render(self, screen):

        screen.blit(self.image, (self.x,self.y))

    def get_rect(self):

        return pygame.Rect(self.x, self.y, self.size, self.size)

    def check_collision(self, other):
        """
        Check collision with another State object
        Args:
            other (State): Another game object to check collision with
        Returns:
            bool: True if objects collide, False otherwise
        """
        if not self.is_collidable or not other.is_collidable:
            return False
        
        return self.get_rect().colliderect(other.get_rect())