import pygame
import pygame.mixer

import os,time

CHANNELS = {}
MUSICS = {}

pygame.mixer.init()

class Music:
    def play_music(self, filename, volume):
        pygame.mixer.music.load(os.path.join('','sounds', filename))
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(volume)

    def play_load_music(self, volume):
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(volume)

    def load_music(self, filename):
        pygame.mixer.music.load(os.path.join('','sounds', filename))

    def stop_music(self):
        pygame.mixer.music.stop()

    def fadeout_music(self, time):
        pygame.mixer.music.fadeout(time)

    def pause_music(self):
        pygame.mixer.music.pause()

class SoundEffect:
    def play_effect(self, filename, volume, c):
        channel = pygame.mixer.find_channel(c)
        channel.stop()
        channel.set_volume(volume)
        sound = pygame.mixer.Sound(os.path.join('','sounds', filename))
        channel.play(sound)
        CHANNELS[c] = channel
