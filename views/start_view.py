import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("небо.jpg")

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        if self.background:
            arcade.draw_texture_rect(self.background,
                                     arcade.rect.XYWH(self.window.width // 2, self.window.height // 2,
                                                      self.window.width, self.window.height))

        arcade.draw_text(
            "SPACE DEFENDER",
            self.window.width // 2,
            self.window.height // 2 + 50,
            arcade.color.PINK,
            font_size=50,
            anchor_x="center",
            font_name="Arial",
            bold=True
        )
        arcade.draw_text(
            "НАЖМИТЕ ЛЮБУЮ КЛАВИШУ ДЛЯ СТАРТА",
            self.window.width // 2,
            self.window.height // 2 - 50,
            arcade.color.LIGHT_GRAY,
            font_size=20,
            anchor_x="center",
            font_name="Arial"
        )
        arcade.draw_text(
            "Управление: WASD | Мышка: Наведение | ЛКМ: Выстрел",
            self.window.width // 2,
            50,
            arcade.color.LIGHT_GRAY,
            font_size=16,
            anchor_x="center",
            font_name="Arial"
        )

    def on_key_press(self, key, modifiers):
        from views.game_view import GameView
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)
