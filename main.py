import sys
import os
import pygame as pg
from colors import Colors
from game_settings import GameSettings
from simple_ui import UI, Text
from story import StoryText
from scene import Scene
from entities import Player, Ghost
from spawn_system import Spawner, GhostSpawner


class Game:
    def __init__(self, fps: int) -> None:
        self._running = True
        self._paused = False

        self._fps = fps
        self._game_speed = 1.0
        self._delta_time = round(1 / self._fps, 3)

        self._scene = MainMenuScene(self)

    def toggle_pause(self) -> None:
        """Переключение состояния паузы."""
        self._paused = not self._paused

    def stop(self) -> None:
        """Останавливает игру."""
        self._running = False

    def is_game_paused(self) -> bool:
        """Возвращает True, если игра находится в состоянии паузы."""
        return self._paused

    def is_game_running(self) -> bool:
        """Возвращает True, если игра запущена."""
        return self._running

    def update(self) -> None:
        """Обновляет игру каждый кадр."""
        scaled_delta_time = self._delta_time * self._game_speed
        self._scene.update(scaled_delta_time)

    def render(self, screen: pg.Surface) -> None:
        """Отображение графики игры на экране."""
        self._scene.render(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        """Обработка событий, которые происходят в игре."""
        self._scene.handle_events(event)

    def change_scene(self, scene: Scene) -> None:
        """Изменение текущей сцены в игре."""
        self._scene = scene


class MainMenuScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self._game = game
        self._menu_scene_ui = UI()

        self._background = colors.color_white

        self._welcome_text_title = "Добро пожаловать в игру!"
        self._welcome_text_color = colors.color_black
        self._welcome_text_size = 70
        self._welcome_text_position = (game_settings.screen_width // 2, game_settings.screen_height // 2)
        self._welcome_text = Text(self._welcome_text_title, self._welcome_text_size, self._welcome_text_color, self._welcome_text_position)

        self._supporting_text_title = "Чтобы начать игру нажмите Space (Пробел)."
        self._supporting_text_color = colors.color_gray
        self._supporting_text_size = 45
        self._supporting_text_position_x = game_settings.screen_width / 2
        self._supporting_text_position_y = (game_settings.screen_height - (game_settings.screen_height * 0.05))  # ОТСТУП СНИЗУ НА 5%
        self._supporting_text_position = (self._supporting_text_position_x, self._supporting_text_position_y)
        self._supporting_text = Text(self._supporting_text_title, self._supporting_text_size, self._supporting_text_color, self._supporting_text_position)

        self._menu_scene_ui.add_element(self._welcome_text)
        self._menu_scene_ui.add_element(self._supporting_text)

    def render(self, screen: pg.Surface) -> None:
        screen.fill(self._background)
        self._menu_scene_ui.draw(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
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

        self._supporting_text_title = "Чтобы продолжить повествование нажмите Enter..."
        self._supporting_text_title_story_ending = "История закончилась. Нажмите Enter, чтобы начать играть."
        self._supporting_text_color = colors.color_gray
        self._supporting_text_size = 50
        self._supporting_text_position_x = game_settings.screen_width / 2
        self._supporting_text_position_y = (game_settings.screen_height - (game_settings.screen_height * 0.05))  # ОТСТУП СНИЗУ НА 5%
        self._supporting_text_position = (self._supporting_text_position_x, self._supporting_text_position_y)
        self._supporting_text = Text(self._supporting_text_title, self._supporting_text_size, self._supporting_text_color, self._supporting_text_position)

        self._story_list = ["Эта история о противостоянии добра и зла.",
                           "Вы - величайший маг, обитатель мирной деревни \"Гринвич\".",
                           "Всё случилось во время праздника костюмов...",
                           "На вашу деревню напал злодей - некому ранее неизвестный колдун.",
                           "Он призвал духов стихий, чтобы уничтожить ваш любимый дом.",
                           "В панике вы бросились бежать со всех ног...",
                           "Оставив позади всех и всё, что у вас было.",
                           "...",
                           "Даже не успели снять праздничный костюм...",
                           "...",
                           "Всё оказалось не так просто...",
                           "Кажется, вы попали в засаду..."]
        self._story_texts = StoryText(self._story_list)

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

        self._gameplay_scene_ui = UI()
        self._gameplay_pause_scene_ui = UI()

        self._score_text_title = "0"
        self._score_text_color = colors.color_black
        self._score_text_size = 70
        self._score_text_position = (game_settings.screen_width - (game_settings.screen_width * 0.1), (game_settings.screen_height * 0.05))
        self._score_text = Text(self._score_text_title, self._score_text_size, self._score_text_color, self._score_text_position)

        self._help_text_title = "Не дайте Духам приблизится!"
        self._help_text_color = colors.color_white
        self._help_text_size = 50
        self._help_text_position = (game_settings.screen_width // 2, game_settings.screen_height - (game_settings.screen_height * 0.05))
        self._help_text = Text(self._help_text_title, self._help_text_size, self._help_text_color, self._help_text_position)

        self._gameplay_scene_ui.add_element(self._score_text)
        self._gameplay_scene_ui.add_element(self._help_text)

        self._pause_text_title = "Пауза"
        self._pause_text_color = colors.color_black
        self._pause_text_size = 140
        self._pause_text_position = (game_settings.screen_width * 0.15, game_settings.screen_height * 0.07)
        self._pause_text = Text(self._pause_text_title, self._pause_text_size, self._pause_text_color, self._pause_text_position)

        self.pause_transparent_surface = pg.Surface((game_settings.screen_width, game_settings.screen_height))
        self.pause_transparent_surface.fill(colors.color_white)
        self.pause_transparent_surface.set_alpha(128)

        self._gameplay_pause_scene_ui.add_element(self._pause_text)

        self._background = pg.image.load(os.path.join("images", "game_background.png"))

        self._explosions_group = pg.sprite.Group()
        self._players_group = pg.sprite.Group()
        self._ghosts_group = pg.sprite.Group()

        self._player = Player(2000, 2000)
        self._players_group.add(self._player)
        self._player.toggle_looking_right()
        self._player.set_position(game_settings.screen_width, (game_settings.screen_height // 2))
        self._player.set_target_position((game_settings.screen_width // 2), (game_settings.screen_height // 2))

        self.spawner = Spawner()
        points_list = [(game_settings.screen_width // 2, 0), (0, game_settings.screen_height / 2), (game_settings.screen_width, game_settings.screen_height / 2),
                       (0, 0), (game_settings.screen_width, game_settings.screen_height), (0, game_settings.screen_height), (game_settings.screen_height, 0)]
        self.spawner.add_points(points_list)
        self.ghosts_spawner = GhostSpawner(1.8, self._ghosts_group, self.spawner, self._player)
        self.ghosts_spawner.toggle_active()

    def render(self, screen: pg.Surface) -> None:
        if not self._game.is_game_paused():
            self.__render_game_world()
        else:
            self.__render_game_pause()

    def __render_game_world(self) -> None:
        screen.blit(self._background, (0, 0))
        self._ghosts_group.draw(screen)
        self._players_group.draw(screen)
        self._explosions_group.draw(screen)
        self._gameplay_scene_ui.draw(screen)

    def __render_game_pause(self) -> None:
        screen.blit(self._background, (0, 0))
        self._ghosts_group.draw(screen)
        self._players_group.draw(screen)
        screen.blit(self.pause_transparent_surface, (0, 0))
        self._gameplay_pause_scene_ui.draw(screen)

    def update(self, scaled_delta_time: float) -> None:
        if not self._game.is_game_paused():
            self.__update_game_world(scaled_delta_time)
        else:
            self.__update_game_pause()

    def __update_game_world(self, scaled_delta_time: float) -> None:
        if self._player.get_score() >= 200 and self.ghosts_spawner.is_active():
            self.ghosts_spawner.toggle_active()
            if not self._ghosts_group.sprites():
                self._player.set_delay(5)
                self._player.set_target_position(0, game_settings.screen_width // 2)
                self._player.set_delay(5)
                self._game.change_scene(FinalScene(self._game))

        self.ghosts_spawner.update(scaled_delta_time)

        for phantom in self._ghosts_group:
            if phantom.collide_with_player(self._player):
                self.ghosts_spawner.toggle_active()
                self._player.die(self._explosions_group)
                for g in self._ghosts_group:
                    g.move_stop()

        self._players_group.update(scaled_delta_time)
        self._ghosts_group.update(scaled_delta_time)
        self._explosions_group.update(scaled_delta_time)

    def __update_game_pause(self) -> None:
        pass

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self._game.toggle_pause()
            if not self._game.is_game_paused():
                if event.key == pg.K_1:
                    self._game.change_scene(FinalScene(self._game))
                elif event.key == pg.K_t:
                    mouse_position = pg.mouse.get_pos()
                    self._player.set_target_position(mouse_position[0], mouse_position[1])
                elif event.key == pg.K_d:
                    self._player.die(self._explosions_group)
        elif event.type == pg.MOUSEBUTTONDOWN:
            if not game.is_game_paused() and event.button == 1 and self._player.is_alive():
                mouse_position = pg.mouse.get_pos()
                for ghost in self._ghosts_group:
                    if ghost.is_clicked(mouse_position):
                        ghost.die(self._explosions_group)
                        self._player.add_score(50)
                        self._score_text.set_text(str(self._player.get_score()))

# class EndingScene


class FinalScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self.__game = game
        self.__game_settings = GameSettings()
        self.__final_scene_ui = UI()

        self.__background = colors.color_black

        self.__text_title = "* Конец *"
        self.__text_color = colors.color_white
        self.__text_size = 95
        self.__text_position = (self.__game_settings.screen_width // 2, self.__game_settings.screen_height // 2)
        self.__text = Text(self.__text_title, self.__text_size, self.__text_color, self.__text_position)

        self.__support_text_title = "Чтобы выйти из игры нажмите Esc (Эскейпт)."
        self.__support_text_color = colors.color_white
        self.__support_text_size = 40
        self.__support_text_position = (self.__game_settings.screen_width // 2, (self.__game_settings.screen_height - (self.__game_settings.screen_height * 0.05)))  # ОТСТУП СНИЗУ НА 5%
        self.__support_text = Text(self.__support_text_title, self.__support_text_size, self.__support_text_color, self.__support_text_position)

        self.__final_scene_ui.add_element(self.__text)
        self.__final_scene_ui.add_element(self.__support_text)

    def render(self, screen: pg.Surface) -> None:
        screen.fill(self.__background)
        self.__final_scene_ui.draw(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.__game.stop()


if __name__ == "__main__":
    pg.init()

    game_settings = GameSettings()
    colors = Colors()

    pg.display.set_icon(pg.image.load(game_settings.screen_icon))
    pg.display.set_caption(game_settings.screen_title)
    screen = pg.display.set_mode(game_settings.screen_size)

    clock = pg.time.Clock()
    game = Game(game_settings.game_fps_max)

    while game.is_game_running():
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                game.stop()
            game.handle_events(event)

        game.update()
        game.render(screen)

        pg.display.flip()
        clock.tick(game_settings.game_fps_max)

    pg.quit()
    sys.exit()
