import math
import random
import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from models.player import Player
from models.bullet import Bullet
from models.enemy import Enemy, BossEnemy, EnemyBullet
from models.particle import Particle


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None
        self.keys_pressed = set()
        self.player_list = None
        self.bullets_list = None
        self.enemies_list = None
        self.enemy_bullets_list = None
        self.particles = []
        self.player = None
        self.shoot_sound = None
        self.explosion_sound = None
        self.hit_sound = None

        self.physics_engine = None

        self.level = 1
        self.score = 0
        self.enemies_killed = 0
        self.enemies_killed_this_level = 0
        self.enemies_to_next_level = 8
        self.level_up_message = ""
        self.level_up_timer = 0

        self.spawn_timer = 0
        self.enemy_shoot_timer = 0
        self.max_enemies_on_screen = 15

    def setup(self):
        self.background = arcade.load_texture("небо.jpg")
        self.keys_pressed = set()
        self.player_list = arcade.SpriteList()
        self.bullets_list = arcade.SpriteList()
        self.enemies_list = arcade.SpriteList()
        self.enemy_bullets_list = arcade.SpriteList()
        self.particles = []

        self.level = 1
        self.score = 0
        self.enemies_killed = 0
        self.enemies_killed_this_level = 0
        self.enemies_to_next_level = 8
        self.level_up_message = ""

        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 300)
        self.player_list.append(self.player)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.enemies_list
        )

        self.shoot_sound = arcade.load_sound("z_uk-aska-z_uk.mp3")
        self.explosion_sound = arcade.load_sound(":resources:/sounds/explosion2.wav")
        self.hit_sound = arcade.load_sound(":resources:/sounds/hit3.wav")
        self.world_camera = arcade.camera.Camera2D()
        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.world_camera.view_data,
            max_amplitude=2.0,
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )

        for _ in range(5):
            enemy = Enemy(self.level)
            self.enemies_list.append(enemy)

    def on_draw(self):
        self.clear()
        self.camera_shake.update_camera()
        self.world_camera.use()
        self.camera_shake.readjust_camera()

        if self.background:
            arcade.draw_texture_rect(self.background,
                                     arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                                      SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player_list.draw()
        self.bullets_list.draw()
        self.enemies_list.draw()
        self.enemy_bullets_list.draw()
        for particle in self.particles:
            particle.draw()
        self.draw_ui()

    def draw_ui(self):
        health_width = 300
        health_height = 20
        health_x = 20
        health_y = SCREEN_HEIGHT - 40
        arcade.draw_rect_filled(
            arcade.rect.XYWH(health_x + health_width // 2,
                             health_y,
                             health_width, health_height),
            (50, 50, 50)
        )

        health_percent = self.player.health / self.player.max_health
        arcade.draw_rect_filled(
            arcade.rect.XYWH(health_x + health_width * health_percent // 2,
                             health_y,
                             health_width * health_percent, health_height),
            arcade.color.RED if health_percent < 0.3 else
            arcade.color.YELLOW if health_percent < 0.6 else
            arcade.color.GREEN
        )

        arcade.draw_text(
            f"HP: {int(self.player.health)}/{self.player.max_health}",
            health_x + health_width + 10,
            health_y - 6,
            arcade.color.WHITE,
            16
        )

        arcade.draw_text(
            f"Уровень: {self.level}",
            SCREEN_WIDTH - 240,
            SCREEN_HEIGHT - 40,
            arcade.color.CYAN,
            24,
            font_name="Arial",
            bold=True
        )

        arcade.draw_text(
            f"Врагов: {self.enemies_killed_this_level}/{self.enemies_to_next_level}",
            SCREEN_WIDTH - 240,
            SCREEN_HEIGHT - 80,
            arcade.color.YELLOW,
            20,
            font_name="Arial"
        )

        arcade.draw_text(
            "Управление: WASD | Мышка: Наведение | ЛКМ: Выстрел",
            SCREEN_WIDTH // 2,
            25,
            arcade.color.LIGHT_GRAY,
            16,
            anchor_x="center",
            font_name="Arial"
        )

        if self.player.health < 30:
            arcade.draw_text(
                "LOW HEALTH!",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                arcade.color.RED,
                36,
                anchor_x="center",
                font_name="Arial",
                bold=True
            )

        if self.level_up_message and self.level_up_timer > 0:
            arcade.draw_text(
                self.level_up_message,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 100,
                arcade.color.GREEN,
                48,
                anchor_x="center",
                font_name="Arial",
                bold=True
            )

            if "БОСС" in self.level_up_message:
                arcade.draw_text(
                    "УНИЧТОЖЬТЕ БОССА!",
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT // 2 + 40,
                    arcade.color.ORANGE,
                    36,
                    anchor_x="center",
                    font_name="Arial",
                    bold=True
                )

    def on_update(self, delta_time):
        self.camera_shake.update(delta_time)
        self.player_list.update(delta_time, self.keys_pressed)
        self.player_list.update_animation(delta_time)
        self.physics_engine.update()
        self.bullets_list.update(delta_time)
        self.enemies_list.update(delta_time)
        self.enemy_bullets_list.update(delta_time)

        self.particles = [p for p in self.particles if p.update(delta_time)]

        bullets_to_remove = []
        for bullet in self.bullets_list:
            if (bullet.center_x < -50 or bullet.center_x > SCREEN_WIDTH + 50 or
                    bullet.center_y < -50 or bullet.center_y > SCREEN_HEIGHT + 50):
                bullets_to_remove.append(bullet)
        for bullet in bullets_to_remove:
            bullet.remove_from_sprite_lists()

        enemy_bullets_to_remove = []
        for bullet in self.enemy_bullets_list:
            if (bullet.center_x < -50 or bullet.center_x > SCREEN_WIDTH + 50 or
                    bullet.center_y < -50 or bullet.center_y > SCREEN_HEIGHT + 50):
                enemy_bullets_to_remove.append(bullet)
        for bullet in enemy_bullets_to_remove:
            bullet.remove_from_sprite_lists()

        if self.level_up_timer > 0:
            self.level_up_timer -= delta_time

        self.spawn_timer += delta_time
        spawn = max(0.3, 1.0 - (self.level - 1) * 0.15)

        if self.enemies_killed_this_level < self.enemies_to_next_level:
            if self.spawn_timer > spawn:
                self.spawn_timer = 0
                if len(self.enemies_list) < self.max_enemies_on_screen:
                    enemy = Enemy(self.level)
                    self.enemies_list.append(enemy)
                    self.physics_engine = arcade.PhysicsEngineSimple(
                        self.player, self.enemies_list
                    )

        self.enemy_shoot_timer += delta_time
        shoot_rate = max(0.3, 1.0 - (self.level - 1) * 0.1)
        if self.enemy_shoot_timer > shoot_rate:
            self.enemy_shoot_timer = 0
            for enemy in self.enemies_list:
                if random.random() < 0.4 + (self.level - 1) * 0.08:
                    bullet = EnemyBullet(enemy.center_x, enemy.center_y - 30, self.level)
                    self.enemy_bullets_list.append(bullet)

        self.check_collisions()

        if self.player.health <= 0:
            self.player.health = 0
            from views.game_over_view import GameOverView
            game_over_view = GameOverView(
                killed=self.enemies_killed,
                level=self.level
            )
            self.window.show_view(game_over_view)

    def check_collisions(self):
        for bullet in self.bullets_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemies_list)
            for enemy in hit_list:
                enemy.health -= 25 + (self.level - 1) * 2
                bullet.remove_from_sprite_lists()

                for _ in range(5):
                    self.particles.append(Particle(bullet.center_x, bullet.center_y))

                if enemy.health <= 0:
                    self.camera_shake.start()

                    for _ in range(20):
                        self.particles.append(Particle(enemy.center_x, enemy.center_y))

                    enemy.remove_from_sprite_lists()
                    self.enemies_killed += 1
                    self.enemies_killed_this_level += 1
                    self.score += enemy.points

                    arcade.play_sound(self.explosion_sound)

                    if self.enemies_killed_this_level >= self.enemies_to_next_level:
                        self.level_up()

                    self.physics_engine = arcade.PhysicsEngineSimple(
                        self.player, self.enemies_list
                    )
                else:
                    arcade.play_sound(self.hit_sound)

        for bullet in self.enemy_bullets_list:
            if arcade.check_for_collision(bullet, self.player):
                self.player.health -= bullet.damage
                bullet.remove_from_sprite_lists()

                for _ in range(10):
                    self.particles.append(Particle(bullet.center_x, bullet.center_y, (255, 100, 100)))

                arcade.play_sound(self.hit_sound)

        player_hits = arcade.check_for_collision_with_list(self.player, self.enemies_list)
        for enemy in player_hits:
            damage = 10 + (self.level - 1) * 3
            self.player.health -= damage
            enemy.health = 0

            self.camera_shake.start()

            for _ in range(25):
                self.particles.append(Particle(enemy.center_x, enemy.center_y))

            arcade.play_sound(self.explosion_sound)

            if enemy.health <= 0:
                enemy.remove_from_sprite_lists()
                self.enemies_killed += 1
                self.enemies_killed_this_level += 1
                self.score += enemy.points

                if self.enemies_killed_this_level >= self.enemies_to_next_level:
                    self.level_up()

                self.physics_engine = arcade.PhysicsEngineSimple(
                    self.player, self.enemies_list
                )

    def level_up(self):
        for enemy in self.enemies_list:
            enemy.remove_from_sprite_lists()

        self.level += 1
        self.enemies_killed_this_level = 0

        if self.level % 5 == 0:
            boss = BossEnemy(self.level)
            self.enemies_list.append(boss)
            self.enemies_to_next_level = 1
            self.level_up_message = f"УРОВЕНЬ {self.level} - БОСС!"
        else:
            self.enemies_to_next_level = 8 + self.level * 2
            self.level_up_message = f"УРОВЕНЬ {self.level}!"

        self.level_up_timer = 3.0
        self.player.health = min(self.player.max_health, self.player.health + 30)

        if self.level % 5 != 0:
            for _ in range(8):
                enemy = Enemy(self.level)
                self.enemies_list.append(enemy)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.enemies_list
        )

    def on_key_press(self, key, modifiers):
        if key:
            self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            bullet = Bullet(
                self.player.center_x,
                self.player.center_y, x, y)
            self.bullets_list.append(bullet)
            arcade.play_sound(self.shoot_sound)

            self.camera_shake.start()
