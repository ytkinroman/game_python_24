import sys
import pygame as pg
from utils import GameSettings, Colors
from simple_ui import UI, Text, UIPause, UIGamePlay, UIMainMenu
from story import StoryText
from scene import Scene
from entities import Player
from spawn_system import GhostSpawner
from environment import Environment


class Game:
    def __init__(self, fps: int) -> None:
        self.__running = True
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
        self.__running = False

    def is_game_paused(self) -> bool:
        """Возвращает True, если игра находится в состоянии паузы."""
        return self._paused

    def is_game_running(self) -> bool:
        """Возвращает True, если игра запущена."""
        return self.__running

    def update(self) -> None:
        """Обновляет игру каждый кадр."""
        scaled_delta_time = self._delta_time * self._game_speed
        self._scene.update(scaled_delta_time)

    def render(self, screen: pg.Surface) -> None:
        """Отображение графики сцены на экране."""
        self._scene.render(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        """Обработка событий, которые происходят в сцене."""
        self._scene.handle_events(event)

    def change_scene(self, scene: Scene) -> None:
        """Сменить текущую сцену."""
        self._scene = scene


class MainMenuScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self.__game = game
        self.__menu_scene_ui = UIMainMenu()

    def render(self, screen: pg.Surface) -> None:
        self.__menu_scene_ui.draw(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.__game.change_scene(StoryScene(self.__game))


class StoryScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self.__game = game
        self.__story_scene_ui = UI()

        self.__game_settings = GameSettings()
        self.__colors = Colors()

        self.__background = self.__colors.COLOR_WHITE

        self.__description_title = "* Режим истории *"
        self.__description_color = self.__colors.COLOR_GRAY
        self.__description_size = 60
        self.__description_position = (self.__game_settings.SCREEN_WIDTH // 2, self.__game_settings.SCREEN_HEIGHT * 0.05)
        self.__description = Text(self.__description_title, self.__description_size, self.__description_color, self.__description_position)

        self.__support_title = "Чтобы продолжить повествование нажмите Enter..."
        self.__support_title_ending = "История закончилась. Нажмите Enter, чтобы начать играть."
        self.__support_color = self.__colors.COLOR_GRAY
        self.__support_size = 50

        self.__support_x = self.__game_settings.SCREEN_WIDTH // 2
        self.__support_y = (self.__game_settings.SCREEN_HEIGHT - (self.__game_settings.SCREEN_HEIGHT * 0.05))  # ОТСТУП СНИЗУ НА 5%
        self.__support_position = (self.__support_x, self.__support_y)
        self.__support = Text(self.__support_title, self.__support_size, self.__support_color, self.__support_position)

        self.__story_list = ["Эта история о противостоянии добра и зла.",
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

        self.__story_texts = StoryText(self.__story_list)

        self.__story_title = self.__story_texts.get_current_text()
        self.__story_color = self.__colors.COLOR_BLACK
        self.__story_size = 55
        self.__story_x = self.__game_settings.SCREEN_WIDTH // 2
        self.__story_y = self.__game_settings.SCREEN_HEIGHT // 2
        self.__story_position = (self.__story_x, self.__story_y)
        self.__story = Text(self.__story_title, self.__story_size, self.__story_color, self.__story_position)

        self.__story_scene_ui.add_element(self.__description)
        self.__story_scene_ui.add_element(self.__story)
        self.__story_scene_ui.add_element(self.__support)

    def render(self, screen: pg.Surface) -> None:
        screen.fill(self.__background)
        self.__story_scene_ui.draw(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if self.__story_texts.is_next_text():
                    self.__story_texts.next_text()
                    self.__story.set_text(self.__story_texts.get_current_text())
                    if self.__story_texts.get_current_index() == self.__story_texts.get_texts_length() - 1:
                        self.__support.set_text(self.__support_title_ending)
                else:
                    self.__game.change_scene(GameScene(self.__game))


class GameScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self.__game_settings = GameSettings()
        self.__colors = Colors()
        self.__game = game

        self.__next_scene_delay = 6

        self.__environment_group = Environment()

        self.__players_group = pg.sprite.Group()
        self.__ghosts_group = pg.sprite.Group()
        self.__explosions_group = pg.sprite.Group()

        self.__gameplay_pause_ui = UIPause()
        self.__gameplay_ui = UIGamePlay()

        self.__player = Player(2000, 2000)
        self.__players_group.add(self.__player)

        self.__player.toggle_looking_right()
        self.__player.set_position(self.__game_settings.SCREEN_WIDTH, self.__game_settings.SCREEN_HEIGHT // 2)
        self.__player.set_target_position(self.__game_settings.SCREEN_WIDTH // 2, self.__game_settings.SCREEN_HEIGHT // 2)

        self.__points_list = [(self.__game_settings.SCREEN_WIDTH // 2, 0), (0, 0),
                              (0, self.__game_settings.SCREEN_HEIGHT // 2),
                              (self.__game_settings.SCREEN_WIDTH, self.__game_settings.SCREEN_HEIGHT // 2),
                              (self.__game_settings.SCREEN_WIDTH, self.__game_settings.SCREEN_HEIGHT),
                              (0, self.__game_settings.SCREEN_HEIGHT), (self.__game_settings.SCREEN_HEIGHT, 0)]

        self.__ghosts_spawner = GhostSpawner(1.4, self.__ghosts_group, self.__player)
        self.__ghosts_spawner.add_points(self.__points_list)

        self.__ghosts_spawner.set_active()

    def update(self, scaled_delta_time: float) -> None:
        if not self.__game.is_game_paused():
            self.__update_game_world(scaled_delta_time)
        else:
            self.__update_game_pause()

    def __update_game_world(self, scaled_delta_time: float) -> None:

        print(self.__ghosts_spawner.get_spawn_interval())

        self.__players_group.update(scaled_delta_time)
        self.__ghosts_group.update(scaled_delta_time)
        self.__explosions_group.update(scaled_delta_time)

        if self.__player.is_alive():
            self.__ghosts_spawner.update(scaled_delta_time)

            if self.__player.get_score() >= 800:
                self.__ghosts_spawner.stop_active()

                if not self.__ghosts_group.sprites():

                    self.__player.set_target_position(-500, self.__game_settings.SCREEN_HEIGHT // 2)

                    if self.__next_scene_delay > 0:
                        self.__next_scene_delay -= scaled_delta_time
                        return

                    self.__game.change_scene(EndingScene(self.__game, self.__player))

            for ghost in self.__ghosts_group:
                if ghost.is_collide_with_player():
                    ghost.die(self.__explosions_group)
                    self.__player.die(self.__explosions_group)
        else:
            self.__ghosts_spawner.stop_active()

            for ghost in self.__ghosts_group:
                ghost.move_stop()

            if self.__next_scene_delay > 0:
                self.__next_scene_delay -= scaled_delta_time
                return
            self.__game.change_scene(EndingScene(self.__game, self.__player))

    def __update_game_pause(self) -> None:
        pass

    def render(self, screen: pg.Surface) -> None:
        if not self.__game.is_game_paused():
            self.__render_game_world()
        else:
            self.__render_game_pause()

    def __render_game_world(self) -> None:
        self.__environment_group.draw(screen)
        self.__players_group.draw(screen)
        self.__ghosts_group.draw(screen)
        self.__explosions_group.draw(screen)
        self.__gameplay_ui.draw(screen)

    def __render_game_pause(self) -> None:
        self.__environment_group.draw(screen)
        self.__players_group.draw(screen)
        self.__ghosts_group.draw(screen)
        self.__explosions_group.draw(screen)
        self.__gameplay_pause_ui.draw(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.__game.toggle_pause()
            if not self.__game.is_game_paused() and self.__player.is_alive():
                if event.key == pg.K_4:
                    mouse_position = pg.mouse.get_pos()
                    self.__player.set_target_position(mouse_position[0], mouse_position[1])
                if event.key == pg.K_5:
                    mouse_position = pg.mouse.get_pos()
                    self.__player.set_position(mouse_position[0], mouse_position[1])
        elif event.type == pg.MOUSEBUTTONDOWN:
            if not self.__game.is_game_paused() and self.__player.is_alive() and event.button == 1:
                mouse_position = pg.mouse.get_pos()
                for ghost in self.__ghosts_group:
                    if ghost.is_clicked(mouse_position):
                        ghost.die(self.__explosions_group)
                        self.__player.add_score_random()
                        self.__gameplay_ui.score.set_text("{:0>4d}".format(self.__player.get_score()))


class EndingScene(Scene):
    def __init__(self, game: Game, player: Player) -> None:
        super().__init__()
        self.__game = game
        self.__player = player

        self.__final_scene_ui = UI()

        self.__game_settings = GameSettings()
        self.__colors = Colors()

        self.__background = self.__colors.COLOR_BLACK

        self.__text_title = "* Конец истории *"
        self.__text_color = self.__colors.COLOR_WHITE
        self.__text_size = 80
        self.__text_position = (self.__game_settings.SCREEN_WIDTH // 2, self.__game_settings.SCREEN_HEIGHT // 2)
        self.__text = Text(self.__text_title, self.__text_size, self.__text_color, self.__text_position)

        if self.__player.is_alive():
            self.__description_title = "Волшебник убежал, с ним остался только костюм курицы... (Хорошая концовка)"
        else:
            self.__description_title = "Волшебник, погиб оказавшийся в безвыходном положении... (Плохая концовка)"

        self.__description_color = self.__colors.COLOR_GRAY
        self.__description_size = 45
        self.__description_position = (self.__game_settings.SCREEN_WIDTH // 2, (self.__game_settings.SCREEN_HEIGHT // 2) + (self.__game_settings.SCREEN_HEIGHT * 0.07))  # ОТСТУП СНИЗУ НА 7%
        self.__description = Text(self.__description_title, self.__description_size, self.__description_color, self.__description_position)

        self.__support_title = "Чтобы выйти из игры нажмите Esc (Эскейпт)."
        self.__support_color = self.__colors.COLOR_GRAY
        self.__support_size = 40
        self.__support_position = (self.__game_settings.SCREEN_WIDTH // 2, (self.__game_settings.SCREEN_HEIGHT - (self.__game_settings.SCREEN_HEIGHT * 0.05)))  # ОТСТУП СНИЗУ НА 5%
        self.__support = Text(self.__support_title, self.__support_size, self.__support_color, self.__support_position)

        self.__replay_title = "Чтобы поиграть ещё раз нажмите Space (Пробел)."
        self.__replay_color = self.__colors.COLOR_GRAY
        self.__replay_size = 40
        self.__replay_position = (self.__game_settings.SCREEN_WIDTH // 2, (self.__game_settings.SCREEN_HEIGHT - (self.__game_settings.SCREEN_HEIGHT * 0.10)))  # ОТСТУП СНИЗУ НА 10%
        self.__replay = Text(self.__replay_title, self.__replay_size, self.__replay_color, self.__replay_position)

        self.__final_scene_ui.add_element(self.__text)
        self.__final_scene_ui.add_element(self.__description)
        self.__final_scene_ui.add_element(self.__support)
        self.__final_scene_ui.add_element(self.__replay)

    def render(self, screen: pg.Surface) -> None:
        screen.fill(self.__background)
        self.__final_scene_ui.draw(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.__game.stop()
            if event.key == pg.K_SPACE:
                self.__game.change_scene(GameScene(self.__game))


if __name__ == "__main__":
    pg.init()

    game_settings = GameSettings()
    colors = Colors()

    pg.display.set_icon(pg.image.load(game_settings.SCREEN_ICON))
    pg.display.set_caption(game_settings.SCREEN_TITLE)
    screen = pg.display.set_mode(game_settings.SCREEN_SIZE)

    clock = pg.time.Clock()
    game = Game(game_settings.GAME_FPS_MAX)

    while game.is_game_running():
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                game.stop()
            game.handle_events(event)

        game.update()
        game.render(screen)

        pg.display.flip()
        clock.tick(game_settings.GAME_FPS_MAX)

    pg.quit()
    sys.exit()
