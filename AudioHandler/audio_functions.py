import pygame


def init():
    pygame.mixer.init()


def play_sound(file_name):
    pygame.mixer.music.load("AudioHandler/AudioFiles/" + file_name)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() is True:
        continue
