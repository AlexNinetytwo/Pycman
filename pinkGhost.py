from ghost import Ghost
import math

class PinkGhost(Ghost):

    def get_distance(self, x, y):
        target_x, target_y = self.get_target_tile()
        x_square = abs(x - target_x) * abs(x - target_x)
        y_square = abs(y - target_y) * abs(y - target_y)
        distance = math.sqrt(x_square + y_square)
        return distance
    
    def get_target_tile(self):
        pacman = self.game.pacman
        target_x = pacman.pos[0]
        target_y = pacman.pos[1]
        match pacman.direction:
            case "up":
                target_y = pacman.pos[1] - 4
            case "down":
                target_y = pacman.pos[1] + 4
            case "left":
                target_x = pacman.pos[0] - 4
            case "right":
                target_x = pacman.pos[0] + 4
        
        return target_x, target_y