from entity import Entity
import pygame
import random
import math
import time


class Ghost(Entity):
    
    DIRECTIONS = ["up","down","left","right"]
    
    def __init__(self, game):
        super().__init__(game)
        self.direction_time = random.randint(5, 100)
        self.next_direction = "right"
        self.old_pos = self.pos
        self.old_direction = ""

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

    def chase(self):
        grid_pos = self._px_cord_to_grid_cord()
        if grid_pos[0] == self.pos[0] and grid_pos[1] == self.pos[1]:
            self_x = self.pos[0]
            self_y = self.pos[1]
            possible = {"up":0,"down":0,"left":0,"right":0}
            # Get possible directions
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
            #time.sleep(1)

            # Look for shorter way to target
            if dir_amount > 1:
                min_distance = 9999
                for dir in possible:
                    if possible[dir] == 0:
                        continue
                    x = possible[dir][0]
                    y = possible[dir][1]
                    target_x = self.game.pacman.pos[0]
                    target_y = self.game.pacman.pos[1]
                    if x == target_x:
                        distance = abs(y - target_y)
                    elif y == target_y:
                        distance = abs(x - target_x)
                    else:
                        x_square = abs(x - target_x) * abs(x - target_x)
                        y_square = abs(y - target_y) * abs(y - target_y)
                        distance = math.sqrt(x_square + y_square)
                    if distance < min_distance and possible[dir] != self.old_pos:
                        min_distance = distance
                        self.direction = dir
                    #     self._show_distance((x, y), distance, (0, 255, 0))
                    # else:
                    #     self._show_distance((x, y), distance, (255, 0 ,0))
                self.old_pos = self.pos

    def _show_distance(self, pos, distance, color):
        distance = round(distance, 2)
        font = pygame.font.Font(None, 18)
        render = font.render(str(distance), True, color)
        x = pos[0] * self.width
        y = pos[1] * self.height
        self.game.screen.blit(render, (x, y))
