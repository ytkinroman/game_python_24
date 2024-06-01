class StoryText:
    def __init__(self, texts: list[str]) -> None:
        self._texts = texts
        self._current_index = 0

    def get_current_text(self) -> str:
        """Возвращает текущий текст по текущему индексу."""
        return self._texts[self._current_index]

    def is_next_text(self) -> bool:
        """Проверяет, есть ли следующий текст в списке."""
        return self._current_index < len(self._texts) - 1

    def next_text(self) -> None:
        """Переходит к следующему тексту, увеличивая текущий индекс на единицу."""
        self._current_index += 1

    def get_current_index(self) -> int:
        """Возвращает текущий индекс."""
        return self._current_index

    def get_texts_length(self) -> int:
        """Возвращает количество текстов в списке."""
        return len(self._texts)
