import math
import random
import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class Enemy(arcade.Sprite):
    def __init__(self, level=1):
        super().__init__()
        enemy_textures = [
            ":resources:/images/space_shooter/playerShip1_green.png",
            ":resources:/images/space_shooter/playerShip1_orange.png",
            ":resources:/images/space_shooter/playerShip2_orange.png",
            ":resources:/images/space_shooter/playerShip3_orange.png"
        ]
        self.texture = arcade.load_texture(random.choice(enemy_textures))
        self.center_x = random.randint(50, SCREEN_WIDTH - 50)
        self.center_y = SCREEN_HEIGHT + 30
        self.speed = random.uniform(150, 300) * (1 + (level - 1) * 0.2)
        self.scale = random.uniform(0.5, 0.8)
        self.direction = random.choice([-1, 1])
        self.health = 30 + (level - 1) * 10
        self.points = random.randint(10, 25) + level * 2

    def update(self, delta_time):
        self.center_y -= self.speed * delta_time
        self.center_x += self.direction * 50 * delta_time
        if self.center_x < 50:
            self.center_x = 50
            self.direction = 1
        elif self.center_x > SCREEN_WIDTH - 50:
            self.center_x = SCREEN_WIDTH - 50
            self.direction = -1
        if self.center_y < -50:
            self.remove_from_sprite_lists()


class BossEnemy(Enemy):
    def __init__(self, level=1):
        super().__init__(level)
        self.texture = arcade.load_texture(":resources:/images/space_shooter/playerShip3_orange.png")
        self.scale = 1.5
        self.speed = 80 + (level - 1) * 10
        self.health = 200 + (level - 1) * 50
        self.points = 500
        self.shoot = 0

    def update(self, delta_time):
        self.center_y -= self.speed * delta_time * 0.3
        self.center_x += math.sin(self.shoot) * 100 * delta_time
        self.shoot += delta_time * 2
        if self.center_y < -50:
            self.remove_from_sprite_lists()


class EnemyBullet(arcade.Sprite):
    def __init__(self, x: float, y: float, level=1):
        super().__init__()
        self.texture = arcade.load_texture(":resources:/images/space_shooter/laserRed01.png")
        self.center_x = x
        self.center_y = y
        self.speed = 400 + (level - 1) * 20
        self.scale = 0.7
        self.damage = 10 + (level - 1) * 2

    def update(self, delta_time):
        self.center_y -= self.speed * delta_time
