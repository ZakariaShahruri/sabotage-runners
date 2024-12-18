import os
import sys
import pygame
from player import Player
from items import generate_random_item
from button import Button

# Set working directory to main.py's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#getting fonts
def get_font(size):
    return pygame.font.Font("../fonts/font.ttf", size)

# Screen dimensions
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)


#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (170, 170, 170)
BLUE = (0, 122, 204)

def game_loop():
    # Initialization of pygame
    pygame.init()

    # Screen setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Sabotage Runners")
    
    # set the background image
    background = pygame.image.load("../Images/background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Create players
    player1 = Player(path="../Images/player1/player1_idle1.png", x=20, y=300)
    player2 = Player(path="../Images/player2/player2_idle1.png", x=1200, y=300)
    
    
    # Set opponents
    player1.opponent = player2
    player2.opponent = player1
    
    #adding animation lists
    idle1 = ["../Images/player1/player1_idle1.png", "../Images/player1/player1_idle2.png"]
    walk = ["../Images/player1/player1_walk1.png", "../Images/player1/player1_walk2.png", "../Images/player1/player1_walk3.png", "../Images/player1/player1_walk4.png", ]
    idle2 = ["../Images/player2/player2_idle1.png", "../Images/player2/player2_idle2.png"]
    

    # Item management
    active_items = []  # List to store items
    item_spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(item_spawn_event, 3000)  # Set a timer to spawn items every 3 seconds

    # The game loop
    running = True
    clock = pygame.time.Clock()
    

    while running:
        
        # Get pressed keys
        keys = pygame.key.get_pressed()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Spawn new items every 3 seconds
            if len(active_items) < 4:
                if event.type == item_spawn_event:
                    active_items.append(generate_random_item(WIDTH, HEIGHT))

            # Reset item effects
            if event.type == pygame.USEREVENT:
                player1.speed = 10
                player2.speed = 10
            if event.type in [pygame.USEREVENT + i for i in range(1, 6)]:
                player1.speed = 10
                player2.speed = 10
                player1.is_shielded = False
                player2.is_shielded = False
                player1.controls_reversed = False
                player2.controls_reversed = False

        

        # Clear the screen and draw the background
        screen.blit(background, (0, 0))

        # Handle player movement
        player1.handle_movement("WASD", keys, WIDTH, HEIGHT)
        player2.handle_movement("arrows", keys, WIDTH, HEIGHT)
        
        player1.animate(idle1, 0.06)
        player2.animate(idle2,0.06)

        
        # Render and check item collisions
        for item in active_items[:]:  # Use a copy of the list to safely remove items
            item.render(screen)
            if player1.check_collision(item):
                item.use(player1, player2)
                active_items.remove(item)
            elif player2.check_collision(item):
                item.use(player2, player1)
                active_items.remove(item)

        # Render players
        player1.render(screen)
        player2.render(screen)

        # Update display
        pygame.display.flip()

        # Limit FPS to 60
        clock.tick(60)

    # Close pygame
    pygame.quit()
    sys.exit()

def menu():
    # Initialize Pygame
    pygame.init()

    # Screen setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sabotage Runners")
    menu_cover = pygame.image.load("../Images/menucover.png")
    

        
    play_button = Button(image=pygame.image.load("../Images/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    option_button = Button(image=pygame.image.load("../Images/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    quit_button = Button(image=pygame.image.load("../Images/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

    # Menu loop
    running = True
    while running:
        screen.blit(menu_cover, (0, 0))
        
        menu_text = get_font(70).render("Sabotage Runners", True, "#FFD300")
        menu_rect = menu_text.get_rect(center=(640, 100))
        
        screen.blit(menu_text, menu_rect)
        
        menu_mouse_pos = pygame.mouse.get_pos()

        for button in [play_button, option_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    game_loop()
                if option_button.checkForInput(menu_mouse_pos):
                    pass
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
            

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    menu()
