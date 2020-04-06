import pygame
from pygame.locals import *

class Musique:

    def __init__(self):
        pygame.mixer.init()
        self.joue = False
        self.musique = pygame.mixer.Sound("song18.wav")

    def commencer(self):
        self.joue = True
        self.musique.play(-1)

    def arreter(self):
        self.musique.stop()
        self.joue = False

    def switch(self):
        if self.joue:
            self.arreter()
        else:
            self.commencer()
