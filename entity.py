import random
from abc import ABC, abstractmethod


class Entity(ABC):
    
    def __init__(self, game):
        self.game = game
        self.alive = True
        self.direction = ""
        self.next_direction = ""
        self.moving = False
        self.color = (255,255,255)
        self.speed = 2
        self.width = game.map.grid
        self.height = game.map.grid
        self.radius = 0
        self.pos = random.choice(game.map.way)
        self.x = self.pos[0] * self.width
        self.y = self.pos[1] * self.height
        self.animation_tick = 0

    @abstractmethod
    def draw(self):
        pass

    def recalc_pos(self):
        self.x = self.pos[0] * self.width
        self.y = self.pos[1] * self.height

    @abstractmethod
    def control(self):
        pass
    
    @abstractmethod
    def clear_draw(self):
        pass

    @abstractmethod
    def animation(self):
        pass

    def restart(self):
        self.clear_draw()
        self.pos = random.choice(self.game.map.way)
        self.recalc_pos()
       
    def _px_cord_to_grid_cord(self) -> tuple:
        offset = self.radius
        tiles = self.width
        grid_x = (self.x - offset) / tiles
        grid_y = (self.y - offset) / tiles
        grid_x = round(grid_x, 2)
        grid_y = round(grid_y, 2)
        return (grid_x, grid_y)
    
    def move(self):
      self.clear_draw()
      grid_pos = self._px_cord_to_grid_cord()
      self.pos = (round(grid_pos[0]), round(grid_pos[1]))

      if self.next_direction != "":

        if self.next_direction == "right":       
            if not self._collision((self.pos[0]+1, grid_pos[1])):
                self.direction = self.next_direction
                self.next_direction = ""    

        elif self.next_direction == "left":    
            if not self._collision((self.pos[0]-1, grid_pos[1])):
                self.direction = self.next_direction
                self.next_direction = ""

        elif self.next_direction == "down":         
            if not self._collision((grid_pos[0], self.pos[1]+1)):
                self.direction = self.next_direction
                self.next_direction = ""

        elif self.next_direction == "up":         
            if not self._collision((grid_pos[0], self.pos[1]-1)):
                self.direction = self.next_direction
                self.next_direction = ""

      if self.direction == "right":
            if not self._collision((self.pos[0]+1, grid_pos[1])):            
                self.x += self.speed
                self.moving = True      
            elif grid_pos[0] < self.pos[0]:
                print(f'right: grid: {grid_pos[0]} pos: {self.pos[0]}')
                self.x += self.speed
                self.moving = True
            elif self._change_side(self.pos[0]+1):
                self.x += self.speed
                self.moving = True
            else:
                self.moving = False
      
      elif self.direction == "left":
            if not self._collision((self.pos[0]-1, grid_pos[1])):             
                    self.x -= self.speed
                    self.moving = True           
            elif grid_pos[0] > self.pos[0]:
                self.x -= self.speed
                self.moving = True
            elif self._change_side(self.pos[0]-1):
                self.x -= self.speed
                self.moving = True
            else:
                self.moving = False
      
      elif self.direction == "down":
            if not self._collision((grid_pos[0], self.pos[1]+1)):             
                self.y += self.speed
                self.moving = True           
            elif grid_pos[1] < self.pos[1]:
                self.y += self.speed
                self.moving = True
            else:
                self.moving = False
      
      elif self.direction == "up":
            if not self._collision((grid_pos[0], self.pos[1]-1)):             
                self.y -= self.speed
                self.moving = True           
            elif grid_pos[1] > self.pos[1]:
                self.y -= self.speed
                self.moving = True
            else:
                self.moving = False
        
    def _collision(self, cords):
        if cords in self.game.map.way:
            return False
        return True
    
    def _change_side(self, next_x):
        grid_width = self.game.map.tiles
        if next_x == grid_width:
            self.x = 0
            grid_pos = self._px_cord_to_grid_cord()
            self.old_pos = (round(grid_pos[0]), round(grid_pos[1])) # So the ghosts don't turn
            return True
        elif next_x == -1:
            self.x = self.game.window_size[0]
            grid_pos = self._px_cord_to_grid_cord()
            self.old_pos = (round(grid_pos[0]), round(grid_pos[1])) # So the ghosts don't turn
            return True
        return False