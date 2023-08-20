import pygame

class Hud:
    
    def __init__(self, game):
        self.game = game
        self.pos = (600,25)
        self.text = f"Score: {self.game.pacman.points} Heath: {self.game.pacman.heath}"
        self.color = (255,255,0)
        self.font = pygame.font.Font(None, 24)
        self.text_surface = self.font.render(self.text, True, self.color)
        self.game.screen.blit(self.text_surface, self.pos)

    def update(self):
        pygame.draw.rect(self.game.screen, self.game.color, (self.pos[0], self.pos[1], self.text_surface.get_width(), self.text_surface.get_height()))
        self.text = f"Score: {self.game.pacman.points} Heath: {self.game.pacman.heath}"
        self.text_surface = self.font.render(self.text, True, self.color)
        self.game.screen.blit(self.text_surface, self.pos)