from utils import GameSettings


class GameManager:
    def __init__(self, game, group, player, spawner) -> None:
        self._game_settings = GameSettings()

        self._game = game
        self._player = player
        self._spawner = spawner
        self._group = group

        self._state = "intro"

        self._start_delay = 0
        self._start_delay_timer = 2

        self._gameplay_delay = 0
        self._gameplay_delay_timer = 5

        self._end_delay = 0
        self._end_delay_timer = 3

        self._next_delay = 0
        self._next_delay_timer = 6

    def update(self, scaled_delta_time: float) -> None:
        if self._state == "intro":
            self.update_intro(scaled_delta_time)
        elif self._state == "gameplay":
            self.update_gameplay(scaled_delta_time)
        elif self._state == "final":
            self.update_final()
        elif self._state == "end":
            self.update_end(scaled_delta_time)
        elif self._state == "next":
            self.update_next(scaled_delta_time)
        elif self._state == "bed":
            self.update_bed(scaled_delta_time)

    def update_intro(self, scaled_delta_time: float) -> None:
        if self._start_delay_timer > 0:
            self._start_delay += scaled_delta_time
            print(self._start_delay)

            if self._start_delay >= self._start_delay_timer:
                print("ES!")
                self._state = "gameplay"
                self._player.set_target_position(self._game_settings.SCREEN_WIDTH // 2, self._game_settings.SCREEN_HEIGHT // 2)

    def update_gameplay(self, scaled_delta_time: float) -> None:
        if self._gameplay_delay_timer > 0:
            self._gameplay_delay += scaled_delta_time
            print(self._gameplay_delay)

            if self._gameplay_delay >= self._gameplay_delay_timer:
                print("ES!")
                self._spawner.set_active()
                self._state = "final"

    def update_final(self) -> None:
        if self._player.is_alive():
            if self._player.get_score() >= 600:
                self._spawner.stop_active()
                if not self._group.sprites():
                    self._state = "end"
        else:
            self._game.toggle_ending()
            self._state = "end"

    def update_end(self, scaled_delta_time: float) -> None:
        if self._end_delay_timer > 0:
            self._end_delay += scaled_delta_time
            print(self._end_delay)

            if self._end_delay >= self._end_delay_timer:
                print("ES!")
                self._player.set_target_position(-150, self._game_settings.SCREEN_HEIGHT // 2)
                self._spawner.stop_active()
                self._state = "next"

    def update_next(self, scaled_delta_time: float) -> None:
        if self._next_delay_timer > 0:
            self._next_delay += scaled_delta_time
            print(self._next_delay)

            if self._next_delay >= self._next_delay_timer:
                self._game.change_scene("end")

    def update_bed(self, scaled_delta_time: float) -> None:
        if self._next_delay_timer > 0:
            self._next_delay += scaled_delta_time
            print(self._next_delay)

            if self._next_delay >= self._next_delay_timer:
                self._game.change_scene("end")
