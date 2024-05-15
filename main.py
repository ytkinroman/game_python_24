import sys
import pygame as pg
from colors import Colors
from game_settings import GameSettings
from simple_ui import UI, Text
from scene import Scene
from story import StoryText


class Game:
    def __init__(self, fps: int) -> None:
        self._is_paused = False
        self._fps = fps
        self._game_speed = 1.0
        self._delta_time = round(1 / self._fps, 3)
        self._scene = MainMenuScene(self)

    def toggle_pause(self) -> None:
        self._is_paused = not self._is_paused

    def is_game_paused(self) -> bool:
        return self._is_paused

    def set_game_speed(self, speed) -> None:
        self._game_speed = speed

    def update(self) -> None:
        scaled_delta_time = self._delta_time * self._game_speed
        self._scene.update(scaled_delta_time)

    def render(self, screen: pg.Surface) -> None:
        """Отрисовка действующей сцены."""
        self._scene.render(screen)

    def handle_event(self, event: pg.event.Event) -> None:
        """Обработка событий действующей сцены."""
        self._scene.handle_events(event)

    def change_scene(self, scene: Scene):
        """Поменять действующую сцену."""
        self._scene = scene


class MainMenuScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self._game = game
        self._menu_scene__ui = UI()

        self._background = colors.color_white

        self._welcome_text_title = "Добро пожаловать в игру!"
        self._welcome_text_color = colors.color_black
        self._welcome_text_size = 70
        self._welcome_text_position_x = game_settings.screen_width / 2
        self._welcome_text_position_y = game_settings.screen_height / 2
        self._welcome_text_position = (self._welcome_text_position_x, self._welcome_text_position_y)
        self._welcome_text = Text(self._welcome_text_title, self._welcome_text_size, self._welcome_text_color, self._welcome_text_position)

        self._supporting_text_title = "Чтобы начать игру нажмите Enter..."
        self._supporting_text_color = colors.color_gray
        self._supporting_text_size = 45
        self._supporting_text_position_x = game_settings.screen_width / 2
        self._supporting_text_position_y = (game_settings.screen_height - (game_settings.screen_height * 0.05))
        self._supporting_text_position = (self._supporting_text_position_x, self._supporting_text_position_y)
        self._supporting_text = Text(self._supporting_text_title, self._supporting_text_size, self._supporting_text_color, self._supporting_text_position)

        self._menu_scene__ui.add_element(self._welcome_text)
        self._menu_scene__ui.add_element(self._supporting_text)

    def render(self, screen: pg.Surface) -> None:
        screen.fill(self._background)
        self._menu_scene__ui.draw(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self._game.change_scene(StoryScene(self._game))


class StoryScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self._game = game
        self._story_scene_ui = UI()

        self._background = colors.color_white

        self._welcome_text_title = "* Режим истории *"
        self._welcome_text_color = colors.color_gray
        self._welcome_text_size = 60
        self._welcome_text_position_x = game_settings.screen_width / 2
        self._welcome_text_position_y = game_settings.screen_height * 0.05
        self._welcome_text_position = (self._welcome_text_position_x, self._welcome_text_position_y)
        self._welcome_text = Text(self._welcome_text_title, self._welcome_text_size, self._welcome_text_color, self._welcome_text_position)

        self._supporting_text_title = "Продолжить повествование нажмите Enter..."
        self._supporting_text_title_story_ending = "История закончилась. Нажмите Enter, чтобы начать играть..."
        self._supporting_text_color = colors.color_gray
        self._supporting_text_size = 50
        self._supporting_text_position_x = game_settings.screen_width / 2
        self._supporting_text_position_y = (game_settings.screen_height - (game_settings.screen_height * 0.05))
        self._supporting_text_position = (self._supporting_text_position_x, self._supporting_text_position_y)
        self._supporting_text = Text(self._supporting_text_title, self._supporting_text_size, self._supporting_text_color, self._supporting_text_position)

        self._story_texts = StoryText(["Эта история о противостоянии добра и зла.",
                              "Вы - величайший маг, обитатель мирной деревни \"Гринвич\".",
                              "Всё случилось во время праздника костюмов...",
                              "На вашу деревню напал злодей - некому ранее неизвестный колдун.",
                              "Он призвал духов стихий, чтобы уничтожить ваш любимый дом.",
                              "В панике вы бросились бежать со всех ног...",
                              "Оставив позади всех и всё, что у вас было.",
                              "Даже не успели снять праздничный костюм...",
                              "...",
                              "Кажется, вы попали в засаду..."])

        self._story_text_title = self._story_texts.get_current_text()
        self._story_text_color = colors.color_black
        self._story_text_size = 55
        self._story_text_position_x = game_settings.screen_width / 2
        self._story_text_position_y = game_settings.screen_height / 2
        self._story_text_position = (self._story_text_position_x, self._story_text_position_y)
        self._story_text = Text(self._story_text_title, self._story_text_size, self._story_text_color, self._story_text_position)

        self._story_scene_ui.add_element(self._welcome_text)
        self._story_scene_ui.add_element(self._story_text)
        self._story_scene_ui.add_element(self._supporting_text)

    def render(self, screen: pg.Surface) -> None:
        screen.fill(self._background)
        self._story_scene_ui.draw(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if self._story_texts.is_next_text():
                    self._story_texts.next_text()
                    self._story_text.set_text(self._story_texts.get_current_text())
                    if self._story_texts.get_current_index() == self._story_texts.get_texts_length() - 1:
                        self._supporting_text.set_text(self._supporting_text_title_story_ending)
                else:
                    self._game.change_scene(GameScene(self._game))


class GameScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self._game = game
        self._background = colors.color_green

    def render(self, screen: pg.Surface) -> None:
        screen.fill(self._background)

    def update(self, scaled_delta_time: float) -> None:
        if not self._game.is_game_paused():
            self._update_game_world(scaled_delta_time)
        else:
            self._update_paused_state()

    def _update_game_world(self, scaled_delta_time: float) -> None:
        pass

    def _update_paused_state(self) -> None:
        pass

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self._game.toggle_pause()
            elif event.key == pg.K_1:
                self._game.change_scene(EndScene(self._game))


class EndScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self._game = game
        self._background = colors.color_black

    def render(self, screen: pg.Surface) -> None:
        screen.fill(self._background)

    def update(self, delta_time: float) -> None:
        pass

    def handle_events(self, event: pg.event.Event) -> None:
        pass


if __name__ == "__main__":
    pg.init()

    game_settings = GameSettings()
    colors = Colors()

    pg.display.set_icon(pg.image.load(game_settings.screen_icon))
    pg.display.set_caption(game_settings.screen_title)
    screen = pg.display.set_mode(game_settings.screen_size)

    clock = pg.time.Clock()
    game = Game(game_settings.game_fps_max)

    running = True
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
            game.handle_event(event)

        game.update()
        game.render(screen)

        pg.display.flip()
        clock.tick(game_settings.game_fps_max)

    pg.quit()
    sys.exit()
