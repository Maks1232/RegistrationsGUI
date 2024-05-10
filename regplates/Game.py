from __future__ import annotations

from .Constants import VOIVODESHIPS_ALL, VOIVODESHIPS_ALL_T, Level, Voivodeship
from .Questions import Questions


class Game:
    def __init__(
        self,
        level: Level,
        voivodeship: Voivodeship | VOIVODESHIPS_ALL_T,
        repeating: bool,
    ):
        self.isRunning: bool = True
        self.level: Level = level
        self.voivodeship: Voivodeship | VOIVODESHIPS_ALL_T = voivodeship
        self.repeating_mode: bool = repeating

        if voivodeship == VOIVODESHIPS_ALL and self.level == Level.EASY:
            raise ValueError(
                "Dla obszaru wszystkich województw rozgrywka zaczyna się od poziomu medium "
            )

        self.multiplier: int = self._get_multiplier()
        self.score: int = 0
        self.score_percentage: int = 100
        self.questions = Questions(
            voivodeship=self.voivodeship
            if self.voivodeship == VOIVODESHIPS_ALL
            else self.voivodeship.value,
            level=self.level.value,
            repeating_mode=self.repeating_mode,
        )
        self.all_questions_num: int = self.questions.all
        self.questions_count: int = 0
        self.questions_left_count: int = self.all_questions_num
        self.next()

    def register_answer(self, id: int) -> None:
        if self.current_question[2][id] == self.current_question[1]:
            self.score += self.multiplier
        self.score_percentage = round(
            100 * self.score / (self.multiplier * self.questions_count)
        )
        self.next()

    def next(self) -> None:
        if self.questions_left_count == 0 and not self.repeating_mode:
            self._end_game()
            return
        self.current_question = self.questions.ask_question()
        self.questions_count += 1
        self.questions_left_count -= 1

    def _get_multiplier(self) -> int:
        if self.level == Level.EXTREME:
            x = 4
        elif self.level == Level.HARD:
            x = 3
        elif self.level == Level.MEDIUM:
            x = 2
        elif self.level == Level.EASY:
            x = 1

        if self.voivodeship == VOIVODESHIPS_ALL:
            x += 1

        return x

    def get_score_text(self) -> str:
        if not self.repeating_mode:
            return f"{self.score_percentage}%"
        else:
            return self.score

    def _end_game(self) -> None:
        self.isRunning = False
