import math
import arcade
from models.direction import Direction
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class Player(arcade.Sprite):
    def __init__(self, x: float, y: float, speed: float):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.speed = speed
        self.scale = 0.8
        self.forward_texture = arcade.load_texture("playerShip1_blue_покой_прямо.png")
        self.back_texture = arcade.load_texture("playerShip1_blue_вниз.png")
        self.right_texture = arcade.load_texture("playerShip1_blue_вправо.png")
        self.left_texture = arcade.load_texture("playerShip1_blue_влево.png")
        self.texture = self.forward_texture
        self.direction = Direction.RIGHT
        self.is_moving = False
        self.move_state = "forward"
        self.last_dx = 0
        self.last_dy = 0
        self.health = 100
        self.max_health = 100

    def update_animation(self, delta_time: float = 1 / 60):
        if self.move_state == "right":
            self.texture = self.right_texture
        elif self.move_state == "left":
            self.texture = self.left_texture
        elif self.move_state == "backward":
            self.texture = self.back_texture
        else:
            self.texture = self.forward_texture

    def update(self, delta_time, keys):
        dx, dy = 0, 0
        w_press = arcade.key.W in keys
        s_press = arcade.key.S in keys
        a_press = arcade.key.A in keys
        d_press = arcade.key.D in keys
        if w_press: dy = 1
        if s_press: dy = -1
        if a_press: dx = -1
        if d_press: dx = 1
        self.last_dx = dx
        self.last_dy = dy
        if dx != 0 and dy != 0:
            dx *= 1 / math.sqrt(2)
            dy *= 1 / math.sqrt(2)
        self.center_x += self.speed * delta_time * dx
        self.center_y += self.speed * delta_time * dy
        margin = 30
        self.center_x = max(margin, min(self.center_x, SCREEN_WIDTH - margin))
        self.center_y = max(margin, min(self.center_y, SCREEN_HEIGHT - margin))
        self.is_moving = dx != 0 or dy != 0
        if d_press and not a_press:
            self.move_state = "right"
            self.direction = Direction.RIGHT
        elif a_press and not d_press:
            self.move_state = "left"
            self.direction = Direction.LEFT
        elif w_press and not s_press:
            self.move_state = "forward"
        elif s_press and not w_press:
            self.move_state = "backward"
        else:
            self.move_state = "forward"
            if dx < 0:
                self.direction = Direction.LEFT
            elif dx > 0:
                self.direction = Direction.RIGHT
