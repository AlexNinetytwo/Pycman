import pygame
from random import randint
from spritsheet import Spritesheet

class SuperFood:
    
    def __init__(self, game, name):
        self.is_super = True
        self.name = name
        self.game = game
        self.width = game.map.grid
        self.height = game.map.grid
        self.radius = 3
        self.pos = (0, 0)
        while self.pos not in self.game.map.way:
            self.generate_pos()
        self.x = self.pos[0] * self.width
        self.y = self.pos[1] * self.height
        self.spritesheet = Spritesheet("images/spritesheet1.png")

    def __del__(self):
        pygame.draw.rect(self.game.screen, (0,0,0), (self.x, self.y, self.width, self.height))
    
    def generate_pos(self):
        x = randint(0, self.game.map.tiles)
        y = randint(0, self.game.map.tiles)
        self.pos = (x ,y)

    def draw(self):
        self.image = self.spritesheet.parse_sprite("food", self.name, "frame_0")
        self.game.screen.blit(self.image, (self.x, self.y))