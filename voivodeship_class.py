import random
import pickle
import pandas as pd


def import_list(file_name):
    with open(file_name, 'rb') as file:
        imported_list = pickle.load(file)
    return imported_list


def import_df(file_name):
    df = pd.read_pickle(file_name)
    return df


class Voivodeship:
    def __init__(self, voivodeship, level, mode=1):
        self.mode = mode
        self.level = level
        self.voivodeship = voivodeship
        self.merged_dicts = {}
        self.already_selected = {}
        self.loaded_dicts = import_list('dicts.pickle3')
        self.voivodeship_options = import_list(file_name='voivodeship_options')
        self.extreme_matrix = import_df(file_name='extreme_matrix.pickle')
        self.levenshtein_matrix = import_df(file_name='levenshtein_matrix.pickle')

    def random_plate(self):

        if self.voivodeship == self.voivodeship_options[-1]:
            if self.mode == 1:
                plate, county = random.choice(list(self.merged_dicts.items() - self.already_selected.items()))
            else:
                plate, county = random.choice(list(self.merged_dicts.items()))
        elif self.level == "Hard":
            if self.mode == 1:
                plate, county = random.choice(
                    list(self.loaded_dicts[self.voivodeship_options.index(self.voivodeship)].items() -
                         self.already_selected.items()))
            else:
                plate, county = random.choice(list(
                    self.loaded_dicts[self.voivodeship_options.index(self.voivodeship)].items()))
        else:
            if self.mode == 1:
                plate, county = random.choice(list(self.loaded_dicts[self.voivodeship_options.index(
                    self.voivodeship)].items() - self.already_selected.items()))
            else:
                plate, county = random.choice(list(self.loaded_dicts[self.voivodeship_options.index(
                    self.voivodeship)].items()))

        return plate, county

    def dictionary_merge(self):
        for _dict in self.loaded_dicts:
            self.merged_dicts.update(_dict)

    def get_random_question(self):

        if self.voivodeship == self.voivodeship_options[-1]:
            self.dictionary_merge()
            plate, county = self.random_plate()
        elif self.level == "Hard":
            self.dictionary_merge()
            plate, county = self.random_plate()
        else:
            plate, county = self.random_plate()

        if self.mode == 1:
            self.already_selected[plate] = county

        return plate, county

    def generate_answers(self, correct_answer):

        answers = [correct_answer]

        if self.level == "Hard":
            col = self.levenshtein_matrix[correct_answer]
        elif self.level == "Extreme":
            col = self.extreme_matrix[correct_answer]
        else:
            col = None

        if isinstance(col, pd.Series):
            col = col.to_frame()
        if self.level == 'Hard':
            col = col.sort_values(correct_answer)
        if self.level == 'Extreme':
            col = col.sort_values(correct_answer, ascending=False)

        iterator = 1

        while len(answers) < 4:
            if self.voivodeship == self.voivodeship_options[-1] and (self.level == "Medium" or self.level == 'Easy'):
                random_answer = random.choice(list(self.merged_dicts.values()))
            elif self.level == "Hard" or self.level == 'Extreme':
                random_answer = col.index[iterator]
                iterator += 1
            else:
                random_answer = random.choice(
                    list(self.loaded_dicts[self.voivodeship_options.index(self.voivodeship)].values()))

            if random_answer not in answers:
                answers.append(random_answer)

        random.shuffle(answers)
        return answers

    def ask_question(self):

        question, correct_answer = self.get_random_question()
        answers = self.generate_answers(correct_answer)

        return question, correct_answer, answers
