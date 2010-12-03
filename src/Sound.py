import pygame
import pygame.mixer

import os,time

CHANNELS = {}
MUSICS = {}

pygame.mixer.init()

class Music:
    def play_music(self, filename):
        pygame.mixer.music.load(os.path.join('','sounds', filename))
        #m_channel = pygame.mixer.Channel(1)
        #m_channel.set_volume(0.6)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(1)
        #m_channel.play(sound)
        #CHANNELS[0] = m_channel
        #print 'playing 1= ',m_channel
    def stop_music(self):
        pygame.mixer.music.stop()

class SoundEffect:
    def play_effect(self, filename):
        channel = pygame.mixer.find_channel(True)
        channel.stop()
        channel.set_volume(1.0)
        sound = pygame.mixer.Sound(os.path.join('','sounds', filename))
        channel.play(sound)
        CHANNELS[1] = channel
        print 'playing 2= ',channel
