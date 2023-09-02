from entity import Entity
import pygame
import random
import math
from spritsheet import Spritesheet
import time


class Ghost(Entity):

    
    DIRECTIONS = ["up","down","left","right"]
    
    def __init__(self, game, name):
        super().__init__(game)
        self.name = name
        self.direction_time = random.randint(5, 100)
        self.next_direction = "right"
        self.old_pos = self.pos
        self.old_direction = ""
        self.spritesheet = Spritesheet("images/spritesheet1.png")
        self.frame = 0
        self.mode = self.chase
        self.time = round(time.perf_counter())

    def killed(self):
        pygame.draw.rect(self.game.screen, (0,0,0), (self.x, self.y, self.width, self.height))

    def recalc_pos(self):
        self.x = self.pos[0] * self.width
        self.y = self.pos[1] * self.height
        
    def draw(self):
        #pygame.draw.rect(self.game.screen, self.color, (self.x, self.y, self.width, self.height))
        self.animation()
        self.game.screen.blit(self.image, (self.x, self.y))

    def clear_draw(self):
        pygame.draw.rect(self.game.screen, (0,0,0), (self.x, self.y, self.width, self.height))

    def control(self):
        if self.direction_time == 0 or self.moving == False:
          self.next_direction = random.choice(Ghost.DIRECTIONS)
          self.direction_time = random.randint(5, 100)
        else:
            self.direction_time -= 1

    def animation(self):
        frame = f'frame_{self.frame}'
        self.animation_tick += 1
        if self.animation_tick == 10:
            self.animation_tick = 0
            self.frame = 0 if self.frame else 1
        if self.mode == self.chase:
            self.image = self.spritesheet.parse_sprite(self.name, self.direction, frame)
        elif self.mode == self.frightened:
            self.image = self.spritesheet.parse_sprite("frightened", "all_directions", frame)


    def frightened(self):
        self.speed = 1
        grid_pos = self._px_cord_to_grid_cord()
        if grid_pos[0] == self.pos[0] and grid_pos[1] == self.pos[1]:
            possible, dir_amount = self.choose_direction()
            if dir_amount > 1:
                max_distance = 0
                for dir in possible:
                    if possible[dir] == 0:
                        continue
                    x = possible[dir][0]
                    y = possible[dir][1]
                    distance = self.get_distance(x ,y)
                    if distance > max_distance and possible[dir] != self.old_pos:
                        max_distance = distance
                        self.direction = dir
                self.old_pos = self.pos
        if round(time.perf_counter()) > self.time + 10:
            if self.x % 2: self.x += 1
            if self.y % 2: self.y += 1
            self.speed = 2
            self.mode = self.chase
            self.recalc_pos()

    def chase(self):
        grid_pos = self._px_cord_to_grid_cord()
        if self.pos == grid_pos:
            possible, dir_amount = self.choose_direction()
            if dir_amount > 1:
                min_distance = 9999
                for dir in possible:
                    if possible[dir] == 0:
                        continue
                    x = possible[dir][0]
                    y = possible[dir][1]
                    distance = self.get_distance(x ,y)
                    if distance < min_distance and possible[dir] != self.old_pos:
                        min_distance = distance
                        self.direction = dir
                self.old_pos = self.pos

    def choose_direction(self):
        self_x = self.pos[0]
        self_y = self.pos[1]
        possible = {"up":0,"down":0,"left":0,"right":0}
        def get_relative_cords(cords, x_or_y_as_index, offset):
            changed = cords[x_or_y_as_index] + offset
            new_cords = (cords[0], changed) if x_or_y_as_index else (changed, cords[1])
            return new_cords
        cords = (self_x, self_y)
        offset = -1
        i = 0
        dir_amount = 0
        for dir in possible:
            x_or_y = i < 2
            neighbor = get_relative_cords(cords, x_or_y, offset)
            if neighbor in self.game.map.way:
                possible[dir] = neighbor
                dir_amount += 1
            offset *= -1
            i += 1
        return possible, dir_amount
    
    def get_distance(self, x, y):
        target_x = self.game.pacman.pos[0]
        target_y = self.game.pacman.pos[1]
        x_square = abs(x - target_x) * abs(x - target_x)
        y_square = abs(y - target_y) * abs(y - target_y)
        distance = math.sqrt(x_square + y_square)
        return distance
    
    def turn_direction(self):
        self.old_pos = self.pos
        match self.direction:
            case "up":
                self.direction = "down"
            case "down":
                self.direction = "up"
            case "left":
                self.direction = "right"
            case "right":
                self.direction = "left"

    def _show_distance(self, pos, distance, color):
        distance = round(distance, 2)
        font = pygame.font.Font(None, 18)
        render = font.render(str(distance), True, color)
        x = pos[0] * self.width
        y = pos[1] * self.height
        self.game.screen.blit(render, (x, y))

    

