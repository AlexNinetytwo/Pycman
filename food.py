import pygame

class Food:
       
    def __init__(self, game, x, y):
        self.game = game
        self.width = game.map.grid
        self.height = game.map.grid
        self.radius = 3
        self.pos = (x, y)
        self.x = x * self.width + 15
        self.y = y * self.height + 15
        self.color = (255,255,0)

    def draw(self):
        pygame.draw.circle(self.game.screen, (0,0,0), (self.x, self.y), self.radius)
        pygame.draw.circle(self.game.screen, self.color, (self.x, self.y), self.radius)