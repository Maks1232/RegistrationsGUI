if __package__:
    from .Utils import get_resource_path
    from .Constants import (
        VOIVODESHIP_OPTIONS_LIST,
        DICTS_JSON_PATH,
        EXTREME_MATRIX_CSV_PATH,
        LEVENSHTEIN_MATRIX_CSV_PATH,
        Level,
    )
else:
    from Utils import get_resource_path
    from Constants import (
        VOIVODESHIP_OPTIONS_LIST,
        DICTS_JSON_PATH,
        EXTREME_MATRIX_CSV_PATH,
        LEVENSHTEIN_MATRIX_CSV_PATH,
        Level,
    )

import random
import pandas as pd
import json


class Voivodeship:
    """
    A class used to get random registration plate index, correct city name, and four element list with obtained answers

    Attributes
    ----------
    voivodeship : str
        an attribute that determines range of available registration plates to be drawn
    level : str
        an attribute that determines difficulty level
    mode : int
        an attribute that determines game mode repetitive or non-repetitive
    already_selected : dictionary
        a dictionary with already used keys and values in particular object instance
    voivodeship_options : list
        a list of strings representing the available voivodeship options
    loaded_dicts : list
        a list of dictionaries including set of all indices and city names as keys and values
    merged_dicts: dictionary
        a dictionary including all dictionaries from loaded dictionaries merged in one
    levenshtein_matrix: DataFrame
        a matrix including Levenshtein distances between city names
    extreme_matrix: DataFrame
        a matrix including own metric similarity values
    all: int
        a value storing number of all available registration plates due to current parameter configuration

    Methods
    -------
    random_plate()
        a method being rule set for registration plate index selection
    dictionary_merge()
        a method which defines merged_dicts attribute content
    get_random_question()
        a method which returns registration plate index with repetitions or no repetitions drawn from data set in which
        content is conditioned by parameters provided in __init__ method arguments
    generate_answers(correct_answer)
        a method which returns four element, shuffled list with answers without repetitions drawn from data set in which
        content is conditioned by parameters provided in __init__ method arguments
    ask_question()
        a method which returns registration plate, belonged city name and four element list with th drawn answers
    """

    def __init__(self, voivodeship, level, mode=1):
        self.voivodeship = voivodeship
        self.level = level
        self.mode = mode
        self.already_selected = {}
        self.voivodeship_options = VOIVODESHIP_OPTIONS_LIST
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
        if not self.voivodeship == self.voivodeship_options[-1]:
            self.all = len(
                self.loaded_dicts[self.voivodeship_options.index(self.voivodeship)]
            )
        else:
            self.all = 409

    def random_plate(self):

        if self.voivodeship == self.voivodeship_options[-1]:
            if self.mode == 1:
                plate, county = random.choice(
                    list(self.merged_dicts.items() - self.already_selected.items())
                )
            else:
                plate, county = random.choice(list(self.merged_dicts.items()))

        elif self.level == Level.HARD.value:
            if self.mode == 1:
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
            if self.mode == 1:
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

        if self.voivodeship == self.voivodeship_options[-1]:
            self.dictionary_merge()
            plate, county = self.random_plate()
        else:
            plate, county = self.random_plate()

        if self.mode == 1:
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
                self.voivodeship == self.voivodeship_options[-1]
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
