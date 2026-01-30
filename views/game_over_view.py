import random
import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from database import save_score


class GameOverView(arcade.View):
    def __init__(self, killed=0, level=1):
        super().__init__()
        self.background = arcade.load_texture("небо.jpg")
        self.killed = killed
        self.level = level
        self.player_name = ""
        self.input_active = True
        self.score_saved = False
        self.error_message = ""
        self.error_timer = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.input_active = True

    def on_draw(self):
        self.clear()
        if self.background:
            arcade.draw_texture_rect(self.background,
                                     arcade.rect.XYWH(self.window.width // 2, self.window.height // 2,
                                                      self.window.width, self.window.height))
        arcade.draw_text(
            "GAME OVER",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 150,
            arcade.color.RED,
            60,
            anchor_x="center",
            font_name="Arial",
            bold=True
        )

        arcade.draw_text(
            f"Врагов уничтожено: {self.killed}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 150,
            arcade.color.WHITE,
            36,
            anchor_x="center",
            font_name="Arial"
        )

        arcade.draw_text(
            f"Уровень достигнут: {self.level}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 100,
            arcade.color.WHITE,
            36,
            anchor_x="center",
            font_name="Arial"
        )

        if self.score_saved:
            arcade.draw_text(
                f"Результат сохранен: {self.player_name}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 50,
                arcade.color.GREEN,
                32,
                anchor_x="center",
                font_name="Arial",
                bold=True
            )

            arcade.draw_text(
                "R - Новая игра | ESC - В меню",
                SCREEN_WIDTH // 2,
                150,
                arcade.color.LIGHT_GRAY,
                24,
                anchor_x="center",
                font_name="Arial"
            )
        else:
            arcade.draw_text(
                "ВВЕДИТЕ ВАШЕ ИМЯ:",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 50,
                arcade.color.YELLOW_GREEN,
                28,
                anchor_x="center",
                font_name="Arial",
                bold=True
            )
            arcade.draw_rect_filled(arcade.XYWH(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                400,
                50),
                (255, 255, 255)
            )

            border_color = arcade.color.YELLOW if self.input_active else arcade.color.GRAY
            arcade.draw_rect_outline(arcade.XYWH(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                400,
                50),
                border_color,
                3
            )

            display_name = self.player_name if self.player_name else "Введите имя..."
            text_color = arcade.color.BLACK if self.player_name else (150, 150, 150)
            arcade.draw_text(
                display_name,
                SCREEN_WIDTH // 2 - 190,
                SCREEN_HEIGHT // 2 - 10,
                text_color,
                26,
                width=380,
                align="center",
                font_name="Arial"
            )
            if self.error_message and self.error_timer > 0:
                arcade.draw_text(
                    self.error_message,
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT // 2 - 50,
                    arcade.color.RED,
                    20,
                    anchor_x="center",
                    font_name="Arial"
                )
            arcade.draw_text(
                "ENTER - Сохранить результат",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 100,
                arcade.color.LIGHT_GRAY,
                22,
                anchor_x="center",
                font_name="Arial"
            )

            arcade.draw_text(
                "ESC - Выйти без имени",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 150,
                arcade.color.LIGHT_GRAY,
                20,
                anchor_x="center",
                font_name="Arial"
            )

    def on_key_press(self, key, modifiers):
        if self.score_saved:
            if key == arcade.key.R:
                from views.game_view import GameView
                game_view = GameView()
                game_view.setup()
                self.window.show_view(game_view)
            elif key == arcade.key.ESCAPE:
                from views.start_view import StartView
                start_view = StartView()
                self.window.show_view(start_view)
            return

        if self.input_active:
            if arcade.key.A <= key <= arcade.key.Z:
                char = chr(key)
                if not modifiers & arcade.key.MOD_SHIFT:
                    char = char.lower()
                if len(self.player_name) < 20:
                    self.player_name += char
            elif arcade.key.KEY_0 <= key <= arcade.key.KEY_9:
                if len(self.player_name) < 20:
                    self.player_name += chr(key)
            elif key == arcade.key.PERIOD:
                if len(self.player_name) < 20:
                    self.player_name += "."
            elif key == arcade.key.MINUS:
                if len(self.player_name) < 20:
                    self.player_name += "-"
            elif key == arcade.key.UNDERSCORE:
                if len(self.player_name) < 20:
                    self.player_name += "_"
            elif key == arcade.key.SPACE:
                if len(self.player_name) < 20 and self.player_name and self.player_name[-1] != " ":
                    self.player_name += " "
            elif key == arcade.key.BACKSPACE:
                if self.player_name:
                    self.player_name = self.player_name[:-1]
            elif key == arcade.key.ENTER or key == arcade.key.NUM_ENTER:
                if len(self.player_name):
                    save_score(
                        player_name=self.player_name.strip(),
                        killed=self.killed,
                        level=self.level
                    )
                    print(f"Сохранено в БД: {self.player_name.strip()}")
                    self.score_saved = True
                    self.input_active = False
                else:
                    self.error_message = "Имя не может быть пустым"
                    self.error_timer = 2.0

        if key == arcade.key.ESCAPE:
            if not self.score_saved:
                if not self.player_name.strip():
                    self.player_name = "Player" + str(random.randint(1, 999))
                if len(self.player_name):
                    save_score(
                        player_name=self.player_name.strip(),
                        killed=self.killed,
                        level=self.level
                    )
                    print(f"Сохранено (ESC): {self.player_name.strip()}")
                self.score_saved = True
            from views.start_view import StartView
            start_view = StartView()
            self.window.show_view(start_view)

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.score_saved:
            input_left = SCREEN_WIDTH // 2 - 200
            input_right = SCREEN_WIDTH // 2 + 200
            input_top = SCREEN_HEIGHT // 2 + 25
            input_bottom = SCREEN_HEIGHT // 2 - 25

            if (input_left <= x <= input_right and
                    input_bottom <= y <= input_top):
                self.input_active = True
                self.error_message = ""
            else:
                self.input_active = False
