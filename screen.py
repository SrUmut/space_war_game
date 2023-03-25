import pygame


class Screen():
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.surf = pygame.display.set_mode((self.width, self.height))
