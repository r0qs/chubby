import pygame
import pygame.mixer

import os,time

CHANNELS = {}
MUSICS = {}

pygame.mixer.init()

class Music:
    def play_music(self, filename):
        pygame.mixer.music.load(os.path.join('','sounds', filename))
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(1)

    def stop_music(self):
        pygame.mixer.music.stop()

class SoundEffect:
    def play_effect(self, filename, c):
        channel = pygame.mixer.find_channel(c)
        channel.stop()
        channel.set_volume(1.0)
        sound = pygame.mixer.Sound(os.path.join('','sounds', filename))
        channel.play(sound)
        CHANNELS[c] = channel
