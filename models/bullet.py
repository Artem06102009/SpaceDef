import math
import arcade


class Bullet(arcade.Sprite):
    def __init__(self, start_x: float, start_y: float, end_x: float, end_y: float):
        super().__init__()
        self.texture = arcade.load_texture(":resources:/images/space_shooter/laserBlue01.png")
        self.center_x = start_x
        self.center_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.speed = 650
        angle = math.atan2(self.end_y - self.center_y, self.end_x - self.center_x)
        self.dx = math.cos(angle)
        self.dy = math.sin(angle)
        self.angle = math.degrees(-angle)
        self.scale = 0.8

    def update(self, delta_time):
        self.center_x += self.speed * delta_time * self.dx
        self.center_y += self.speed * delta_time * self.dy
