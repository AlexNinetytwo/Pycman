import pygame

class Hud:
    
    def __init__(self, game):
        self.game = game
        self.pos = (700,100)
        self.text = f"Heath: {self.game.pacman.heath}"
        self.color = (255,255,0)
        self.font = pygame.font.Font(None, 12)
        self.text_surface = self.font.render(self.text, True, self.color)