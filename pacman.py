import pygame
from pygame.locals import *
from entity import Entity
import math
import time


class Pacman(Entity):

    def __init__(self, game):
        super().__init__(game)
        self.color = (255,255,0)
        self.points = 0
        self.radius = 15
        self.eating_sound = pygame.mixer.Sound("sounds/pacman_chomp.wav")
        self.eating_sound.set_volume(0.2)
        self.x = self.pos[0] * self.width + self.radius
        self.y = self.pos[1] * self.height + self.radius
        self.openes = 0
        self.heath = 3
        self.super = False
        
    def draw(self):
        pygame.draw.circle(self.game.screen, self.color, (self.x,self.y), 15.0)  

    def recalc_pos(self):
        self.x = self.pos[0] * self.width + self.radius
        self.y = self.pos[1] * self.height + self.radius

    def clear_draw(self):
        pygame.draw.circle(self.game.screen, (0,0,0), (self.x,self.y), 15.0)

    def control(self, event):
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                self.next_direction = "down"
            if event.key == K_UP:
                self.next_direction = "up"
            if event.key == K_LEFT:
                self.next_direction = "left"
            if event.key == K_RIGHT:
                self.next_direction = "right"

    def animation(self):
        if self.moving:
            self.animation_tick += 2
        if self.animation_tick > 30:
            self.animation_tick = 0
        elif self.animation_tick > 15:
            self.openes = 30 - self.animation_tick
        else:
            self.openes = self.animation_tick / 2
            
        points = [(self.x, self.y), (self.x + 15, self.y + self.openes), (self.x + 15, self.y - self.openes)]
        points = self.__rotate_mouth(points)
        pygame.draw.polygon(self.game.screen, (0,0,0), points)

    def __rotate_mouth(self, points):
        rotated_points = []
        for x, y in points:
            rel_x = x - self.x
            rel_y = y - self.y
            match self.direction:
                case "up":
                    angle = -90
                case "down":
                    angle = 90
                case "left":
                    angle = 180
                case _:
                    angle = 0
            new_x = rel_x * math.cos(math.radians(angle)) - rel_y * math.sin(math.radians(angle))
            new_y = rel_x * math.sin(math.radians(angle)) + rel_y * math.cos(math.radians(angle))
            rotated_x = new_x + self.x
            rotated_y = new_y + self.y
            rotated_points.append((rotated_x, rotated_y))
        return rotated_points

    def eat_food(self):
        for food in self.game.food:
            if food.pos == self.pos:
                self.eating_sound.play()
                self.points += 1
                self.super = True if food.is_super else False
                if self.super:
                    for enemy in self.game.enemies:
                        enemy.mode = enemy.frightened
                        enemy.time = round(time.perf_counter())
                        enemy.turn_direction()
                self.game.food.remove(food)
                self.game.hud.update()   
                

    def touch_enemy(self):
        for enemy in self.game.enemies:
            if self.pos == enemy.pos:
                if enemy.mode == enemy.chase:
                    # self.alive = False
                    pass
                elif enemy.mode == enemy.frightened:
                    # enemy.killed()
                    # self.game.enemies.remove(enemy)
                    # del enemy
                    pass
