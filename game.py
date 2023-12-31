import pygame
import sys
from pacman import Pacman
from map import Map
from food import Food
from ghost import Ghost
from hud import Hud
from superFood import SuperFood
from pinkGhost import PinkGhost


class Game:
    
    def __init__(self, window_size:tuple = (800,800)):
        pygame.init()
        self.window_size = window_size
        self.screen = pygame.display.set_mode(self.window_size)
        self.color = (0,0,64)
        self.clock = pygame.time.Clock()
        self.level = 1
        self.fill_game(f"levels/lvl{self.level}.png")
         
    def fill_game(self, lvl):
        self.screen.fill(self.color)
        self.map = Map(self)
        self.map.extract_white_pixel_coords(lvl)
        self.map.draw()
        self.food = [Food(self, place[0], place[1]) for place in self.map.way]
        self.food_amount = len(self.food)
        self.food += [SuperFood(self, "cherry") for i in range(4)]
        # Pacman
        self.pacman = Pacman(self)
        # Hud
        self.hud = Hud(self)
        # Enemies
        self.enemies = [Ghost(self, "red_ghost") for i in range(3)]
        self.enemies.append(PinkGhost(self, "pink_ghost"))
        self.enemies.append(PinkGhost(self, "pink_ghost"))

    def update(self):
        # Debug
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
            self.hud.update()
            for enemy in self.enemies:
                enemy.restart()
            self.pacman.restart()

    def check(self):

        for enemy in self.enemies:
            enemy.mode()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            else:
                self.pacman.control(event)

        self.pacman.touch_enemy()

        if self.pacman.points == self.food_amount:
            self.level += 1
            self.fill_game(f"levels/lvl{self.level}.png")


    def draw_food(self):
        for food in self.food:
            food.draw()

            