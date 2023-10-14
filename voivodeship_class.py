import csv
import random
import colorama as colorama
import pickle

import numpy as np
import pandas as pd


def import_list(file_name):
    with open(file_name, 'rb') as file:
        imported_list = pickle.load(file)
    return imported_list


def import_df(file_name):
    df = pd.read_pickle(file_name)
    return df


class Voivodeship:
    def __init__(self, voivodeship, level):
        self.voivodeship = voivodeship
        self.level = level
        self.merged_dicts = {}
        self.voivodeship_options = import_list(file_name='voivodeship_options')
        self.levenshtein_matrix = import_df(file_name='levenshtein_matrix.pickle')
        self.loaded_dicts = import_list('dicts.pickle3')

    def get_random_question(self):

        # wybierzlosowy klucz i wartość (mapowanie z przekazywanej zmiennej tekstowej na indeks listy w słowniku)
        if self.voivodeship == self.voivodeship_options[-1]:
            for _dict in self.loaded_dicts:
                self.merged_dicts.update(_dict)
            id, county = random.choice(list(self.merged_dicts.items()))
        elif self.level == "Hard":
            for _dict in self.loaded_dicts:
                self.merged_dicts.update(_dict)
            id, county = random.choice(
                list(self.loaded_dicts[self.voivodeship_options.index(self.voivodeship)].items()))
        else:
            id, county = random.choice(list(self.loaded_dicts[self.voivodeship_options.index(self.voivodeship)].items()))

        return id, county

    def generate_answers(self, correct_answer):

        # generujemy listę odpowiedzi, w tym poprawnej odpowiedzi
        answers = [correct_answer]

        if self.level == 'Hard':
            col = self.levenshtein_matrix[correct_answer]
            if isinstance(col, pd.Series):
                col = col.to_frame()
                col = col.sort_values(correct_answer)
                print(col)
            else:
                col = col.sort_values(correct_answer)
            iterator = 1

        while len(answers) < 4:
            # wybieramy losową wartość ze słownika, ale tylko jeśli nie jest już na liście
            if self.voivodeship == self.voivodeship_options[-1] and (self.level == "Medium" or self.level == 'Easy'):
                random_answer = random.choice(list(self.merged_dicts.values()))
            elif self.level == "Hard":
                random_answer = col.index[iterator]
                iterator += 1
            elif self.level == "Unicum":
                random_answer = col.index[iterator]
                iterator += 1
            else:
                random_answer = random.choice(
                    list(self.loaded_dicts[self.voivodeship_options.index(self.voivodeship)].values()))

            if random_answer not in answers:
                answers.append(random_answer)

        # losowo przemieszczamy poprawną odpowiedź
        random.shuffle(answers)
        return answers

    def ask_question(self):

        question, correct_answer = self.get_random_question()
        answers = self.generate_answers(correct_answer)

        return question, correct_answer, answers
