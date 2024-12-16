import pygame
pygame.init()
pygame.mixer.init()

# Path to music files
menu_music = "../audios/menu_music.mp3"
main_music = "../audios/main_music.mp3"
one_vs_one_music = "../audios/one_vs_one_music"

# Play menu music at startup of program in a loop
pygame.mixer.music.load(menu_music)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.delay(100)    