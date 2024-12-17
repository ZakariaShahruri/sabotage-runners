import pygame

pygame.init()
pygame.mixer.init()

# Path to music files
menu_music = "../audios/menu_music.mp3"
main_music = "../audios/main_music.mp3"
one_vs_one_music = "../audios/one_vs_one_music.mp3"
end_screen_music = "../audios/end_screen_music.mp3"

# Music Manager Class
class MusicManager:
    @staticmethod
    def play_music(music_file):
        """Load and play background music in a loop."""
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)  # -1 means infinite loop

    @staticmethod
    def stop_music():
        """Stop the currently playing background music."""
        pygame.mixer.music.stop()

# Example Usage
if __name__ == "__main__":
    try:
        print("Playing menu music...")
        MusicManager.play_music(menu_music)

        input("Press Enter to switch to main music...")
        MusicManager.play_music(main_music)

        input("Press Enter to switch to one-vs-one music...")
        MusicManager.play_music(one_vs_one_music)

        input("Press Enter to end screen music...")
        MusicManager.play_music(end_screen_music)

        print("Exiting music test...")
    finally:
        pygame.mixer.music.stop()
        pygame.quit()
