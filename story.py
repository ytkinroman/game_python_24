class StoryText:
    def __init__(self, texts: list[str]) -> None:
        self._texts = texts
        self._current_index = 0

    def get_current_text(self) -> str:
        return self._texts[self._current_index]

    def is_next_text(self) -> bool:
        return self._current_index < len(self._texts) - 1

    def next_text(self) -> None:
        self._current_index += 1

    def get_current_index(self) -> int:
        return self._current_index

    def get_texts_length(self) -> int:
        return len(self._texts)
