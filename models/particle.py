import random
import arcade

class Particle:
    def __init__(self, x: float, y: float, color=None):
        self.x = x
        self.y = y
        self.size = random.uniform(2, 6)
        if color:
            self.color = color
        else:
            self.color = random.choice([
                (255, 255, 100), (255, 200, 50), (255, 100, 100),
                (100, 200, 255), (255, 150, 255)
            ])
        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(-3, 3)
        self.lifetime = random.uniform(0.5, 1.5)
        self.alpha = 255

    def update(self, delta_time):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= delta_time
        self.alpha = int(255 * (self.lifetime / 1.5))
        return self.lifetime > 0

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.size, (*self.color, self.alpha))
