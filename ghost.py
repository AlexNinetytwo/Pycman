from entity import Entity
import pygame
import random


class Ghost(Entity):
    
    DIRECTIONS = ["up","down","left","right"]
    
    def __init__(self, game):
        super().__init__(game)
        self.direction_time = random.randint(5, 100)

    def recalc_pos(self):
        self.x = self.pos[0] * self.width
        self.y = self.pos[1] * self.height
        
    def draw(self):
        pygame.draw.rect(self.game.screen, self.color, (self.x, self.y, self.width, self.height))

    def clear_draw(self):
        pygame.draw.rect(self.game.screen, (0,0,0), (self.x, self.y, self.width, self.height))

    def control(self):
        if self.direction_time == 0 or self.moving == False:
          self.next_direction = random.choice(Ghost.DIRECTIONS)
          self.direction_time = random.randint(5, 100)
        else:
            self.direction_time -= 1

    def animation(self):
        pass