import pygame
import random
from PIL import Image

class Map:
    
    def __init__(self, game):
        self.window_size = game.window_size
        self.grid = int(game.window_size[0] / 25)
        self.screen = game.screen
        self.color = (0,0,0)
        self.way = []

    def draw_grid(self):
        for x in range(0, self.window_size[0], self.grid):
            pygame.draw.line(self.screen, self.color, (x, 0),(x, self.window_size[1]))
        for y in range(0, self.window_size[1], self.grid):
            pygame.draw.line(self.screen, self.color, (0, y),(self.window_size[0], y))

    def extract_white_pixel_coords(self, image_path):

        image = Image.open(image_path)

        # convert the image into an L-mode-image (8-Bit-greyscale)
        image = image.convert("L")
        for y in range(image.height):
            for x in range(image.width):
                pixel = image.getpixel((x, y))
                if pixel == 255:
                    self.way.append((x, y))

        self.mirrow()

    def draw(self):
        for i in range(len(self.way)):
          x = self.way[i][0] * self.grid
          y = self.way[i][1] * self.grid
          pygame.draw.rect(self.screen,self.color,(x,y,self.grid,self.grid))

    def mirrow(self):
        mirrowed_cords = []
        for cords in self.way:
            x = cords[0]
            y = cords[1]
            y = 24 - y
            new_cords = (x,y)     
            mirrowed_cords.append(new_cords)
            x = 24 - x
            new_cords = (x,y)                    
            mirrowed_cords.append(new_cords)
            y = cords[1]
            new_cords = (x,y)                   
            mirrowed_cords.append(new_cords)
        for cords in mirrowed_cords:
            if cords not in self.way:
                self.way.append(cords)
