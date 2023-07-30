import pygame
import sys
from pacman import Pacman
from map import Map
from food import Food
from ghost import Ghost


class Game:
    
    def __init__(self, window_size:tuple = (800,800)):
        pygame.init()
        self.window_size = window_size
        self.screen = pygame.display.set_mode(self.window_size)
        self.screen.fill((0,0,64))
        self.clock = pygame.time.Clock()
        # World
        self.map = Map(self)
        self.map.extract_white_pixel_coords("C:\programming\pythongames\pacman\levels\lvl2.png")
        self.map.draw()
        self.foods = []
        self.stroke_food()
        # Pacman
        self.pacman = Pacman(self)     
        # Enemies
        self.enemies = []
        for i in range(3):
            self.enemies.append(Ghost(self))
        
    def update(self):
        if self.pacman.alive:
            pygame.display.update()
            self.clock.tick(60)
            # World
            self.draw_food()
            # Pacman
            self.pacman.move()
            self.pacman.draw()
            self.pacman.animation()
            self.pacman.eat_food()
            # Enemies
            for enemy in self.enemies:
                enemy.move()
                enemy.draw()
        elif self.pacman.heath > 0:
            self.pacman.heath -= 1
            self.pacman.alive = True
            for enemy in self.enemies:
                enemy.restart()
            self.pacman.restart()


        
    def check(self):

        for enemy in self.enemies:
            enemy.control()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            else:
                self.pacman.control(event)

        self.pacman.touch_enemy()
                

    def stroke_food(self):
        for place in self.map.way:
            self.foods.append(Food(self, place[0], place[1]))

    def draw_food(self):
        for food in self.foods:
            food.draw()
            