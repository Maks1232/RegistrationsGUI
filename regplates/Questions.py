from __future__ import annotations

import json
import random

import pandas as pd

from .Constants import (
    DICTS_JSON_PATH,
    EXTREME_MATRIX_CSV_PATH,
    LEVENSHTEIN_MATRIX_CSV_PATH,
    VOIVODESHIPS_ALL,
    Level,
    Voivodeship,
)
from .Utils import get_resource_path


class Questions:
    def __init__(self, voivodeship, level, repeating_mode=True):
        self.voivodeship = voivodeship
        self.level = level
        self.repeating_mode = repeating_mode
        self.already_selected = {}
        self.voivodeship_options = [
            *[voivodeship.value for voivodeship in Voivodeship],
            VOIVODESHIPS_ALL,
        ]
        with open(get_resource_path(DICTS_JSON_PATH), encoding="utf8") as dicts_file:
            self.loaded_dicts = json.load(dicts_file)
        self.merged_dicts = self.dictionary_merge()
        self.levenshtein_matrix = pd.read_csv(
            get_resource_path(LEVENSHTEIN_MATRIX_CSV_PATH),
            index_col=0,
            encoding="utf-8",
        )
        self.extreme_matrix = pd.read_csv(
            get_resource_path(EXTREME_MATRIX_CSV_PATH), index_col=0, encoding="utf-8"
        )
        if not self.voivodeship == VOIVODESHIPS_ALL:
            self.all = len(
                self.loaded_dicts[self.voivodeship_options.index(self.voivodeship)]
            )
        else:
            self.all = 409

    def random_plate(self):
        if self.voivodeship == VOIVODESHIPS_ALL:
            if not self.repeating_mode:
                plate, county = random.choice(
                    list(self.merged_dicts.items() - self.already_selected.items())
                )
            else:
                plate, county = random.choice(list(self.merged_dicts.items()))

        elif self.level == Level.HARD.value:
            if not self.repeating_mode:
                plate, county = random.choice(
                    list(
                        self.loaded_dicts[
                            self.voivodeship_options.index(self.voivodeship)
                        ].items()
                        - self.already_selected.items()
                    )
                )
            else:
                plate, county = random.choice(
                    list(
                        self.loaded_dicts[
                            self.voivodeship_options.index(self.voivodeship)
                        ].items()
                    )
                )
        else:
            if not self.repeating_mode:
                plate, county = random.choice(
                    list(
                        self.loaded_dicts[
                            self.voivodeship_options.index(self.voivodeship)
                        ].items()
                        - self.already_selected.items()
                    )
                )
            else:
                plate, county = random.choice(
                    list(
                        self.loaded_dicts[
                            self.voivodeship_options.index(self.voivodeship)
                        ].items()
                    )
                )

        return plate, county

    def dictionary_merge(self):
        merged = {}
        for _dict in self.loaded_dicts:
            merged.update(_dict)
        return merged

    def get_random_question(self):
        if self.voivodeship == VOIVODESHIPS_ALL:
            self.dictionary_merge()
            plate, county = self.random_plate()
        else:
            plate, county = self.random_plate()

        if not self.repeating_mode:
            self.already_selected[plate] = county

        return plate, county

    def generate_answers(self, correct_answer):
        answers = [correct_answer]

        if self.level == Level.HARD.value:
            col = self.levenshtein_matrix[correct_answer]
            if isinstance(col, pd.Series):
                col = col.to_frame()
            col = col.sort_values(correct_answer)
        elif self.level == Level.EXTREME.value:
            col = self.extreme_matrix[correct_answer]
            if isinstance(col, pd.Series):
                col = col.to_frame()
            col = col.sort_values(correct_answer, ascending=False)
        else:
            col = None

        iterator = 0

        while len(answers) < 4:
            if (
                self.voivodeship == VOIVODESHIPS_ALL
                and self.level == Level.MEDIUM.value
            ):
                random_answer = random.choice(list(self.merged_dicts.values()))
            elif self.level == Level.HARD.value or self.level == Level.EXTREME.value:
                random_answer = col.index[iterator]
                iterator += 1
            else:
                random_answer = random.choice(
                    list(
                        self.loaded_dicts[
                            self.voivodeship_options.index(self.voivodeship)
                        ].values()
                    )
                )

            if random_answer not in answers:
                answers.append(random_answer)

        random.shuffle(answers)

        return answers

    def ask_question(self):
        question, correct_answer = self.get_random_question()
        answers = self.generate_answers(correct_answer)

        return question, correct_answer, answers
