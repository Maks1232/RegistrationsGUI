import sys
import time
import pandas as pd
import pygame
import os
import pickle
import numpy as np
import Levenshtein
from voivodeship_class import Voivodeship
import tkinter as tk
from tkinter import messagebox
from itertools import islice
import pygame_gui
import pygame.freetype
from pygame.locals import *
import threading

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Window creation
WIN = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
pygame.display.set_caption("Registration Plates Quiz")

# Kolory
white = (255, 255, 255)
aqua = (0, 255, 255)
red = (255, 0, 0)
grey = (150, 150, 150)
dark_grey = (100, 100, 100)
green = (60, 179, 113)
black = (0, 0, 0)
dark_blue = (66, 0, 249)
bright_blue = (175, 238, 238)

# Font
font = pygame.font.Font(None, 32)
font_2 = pygame.font.Font(None, 72)

# Variables
play = False
full_list = False
full_level_list = False
active_option = "Wybierz województwo"
active_level_option = "Wybierz poziom"
tribes = {0: 'Powtarzanie', 1: 'Bez powtórzeń'}
mode = 0
score = 0
nick_executed = False
clock = pygame.time.Clock()
UI_REFRESH_RATE = clock.tick(60) / 10000
run = True


# Loading images
app_logo = pygame.image.load(os.path.join('Images', 'title_v1.png'))
registration_template = pygame.image.load(os.path.join('Images', 'registration_template.png'))


# Export list to the file
def export_list(voivodeships, file_name):
    with open(file_name, 'wb') as file:
        pickle.dump(voivodeships, file)


# Import list from the file
def import_list(file_name):
    with open(file_name, 'rb') as file:
        imported_list = pickle.load(file)
    return imported_list


# Opcje pola rozwijanego
loaded_dicts = import_list('dicts.pickle3')
voivodeship_options = import_list(file_name='voivodeship_options')
level_options = ["Easy", "Medium", "Hard", "Extreme"]


def position_update():
    _drop_down = pygame.Rect(0.1 * WIN.get_width(),
                             20 + 1.1 * app_logo.get_height(),
                             0.25 * WIN.get_width(),
                             0.04 * WIN.get_height())

    _level_drop_down = pygame.Rect(0.9 * WIN.get_width() - _drop_down[2],
                                   20 + 1.1 * app_logo.get_height(),
                                   0.25 * WIN.get_width(),
                                   0.04 * WIN.get_height())

    _play_button = pygame.Rect(0.65 * WIN.get_width(),
                               0.82 * WIN.get_height(),
                               0.25 * WIN.get_height(),
                               0.04 * WIN.get_height())

    _exit_button = pygame.Rect(0.65 * WIN.get_width(),
                               0.86 * WIN.get_height(),
                               0.25 * WIN.get_height(),
                               0.04 * WIN.get_height())

    _first_answer = pygame.Rect(0.1 * WIN.get_width(),
                                0.32 * WIN.get_height(),
                                0.5 * WIN.get_height(),
                                0.1 * WIN.get_height())

    _mode_button = pygame.Rect(WIN.get_width() / 2 - 0.0625 * WIN.get_width(),
                               20 + 1.1 * app_logo.get_height(),
                               0.125 * WIN.get_width(),
                               0.04 * WIN.get_height())

    return _drop_down, _level_drop_down, _play_button, _exit_button, _first_answer, _mode_button


def draw_element_with_background(color, element, position):
    WIN.fill(color)
    WIN.blit(element, position)


def draw_rect(position, text, button_color):
    pygame.draw.rect(WIN, button_color, position)  # draw rectangular
    pygame.draw.rect(WIN, white, position, 2)  # draw the frame
    write_text(text,
               (position[0] + position[2] // 2, position[1] + position[3] // 2))


def write_text(text, location):
    text_surface = font.render(text, True, white)
    text_location = text_surface.get_rect(center=location)
    WIN.blit(text_surface, text_location)


def draw_list(position, options, active_list, active_choice):
    draw_rect(position, active_choice, green)

    if active_list:

        for i, option in enumerate(options):
            y = position[1] + (i + 1) * position.height
            pygame.draw.rect(WIN, grey, (position[0], y, position.width, position.height))
            pygame.draw.rect(WIN, white, (position[0], y, position.width, position.height), 2)
            write_text(option, (position[0] + position.width // 2, y + position.height // 2))


def show_message(title, message):
    messagebox.showinfo(title, message)


def exit_execute(_run, stage=0):
    if stage == 0:
        _result = messagebox.askquestion("Potwierdzenie", "Czy na pewno chcesz wyjść z aplikacji?")
    else:
        _result = messagebox.askquestion("Potwierdzenie", "Czy na pewno chcesz wyjść do menu?")

    if _result == "yes":
        _run = False

    return _run


def multiplier(voivodeship, level, voivodeship_base, level_base):
    a = 1
    b = 0

    if voivodeship == voivodeship_base[-1] and level == level_base[-1]:
        a = 2
        b = 3
    elif voivodeship == voivodeship_base[-1] and level == level_base[-2]:
        a = 2
        b = 2
    elif not voivodeship == voivodeship_base[-1] and level == level_base[-1]:
        a = 1
        b = 2
    elif (voivodeship == voivodeship_base[-1] and level == level_base[0] or
          not voivodeship == voivodeship_base[-1] and level == level_base[-2]):
        b = 1

    return a + b


def load_df(name):
    df = pd.read_excel(name)
    return df


def save_score(nick, level, voivodeship, points):
    df = load_df("test.xlsx")

    updater = pd.DataFrame(columns=["Nazwa", "Poziom", "Województwo", "Skuteczność[%]"])
    updater.at[0, 'Nazwa'] = nick
    updater.at[0, 'Poziom'] = level
    updater.at[0, 'Województwo'] = voivodeship
    updater.at[0, 'Skuteczność[%]'] = points

    df = pd.concat([updater, df], ignore_index=True)

    df.to_excel("test.xlsx", columns=["Nazwa", "Poziom", "Województwo", "Skuteczność[%]"])


# Funkcja do renderowania DataFrame
def render_dataframe(df):
    _x, _y = WIN.get_width() / 10, WIN.get_height() / 2.3
    cell_width, cell_height = WIN.get_width() / 5, WIN.get_height() / 30

    text = font_2.render("Ranking ostatnich rozgrywek:", True, dark_blue)
    WIN.blit(text, (20, 20 + WIN.get_height() / 3.4))

    for col in df.columns[1:]:
        text = font.render(col, True, black)
        WIN.blit(text, (_x - WIN.get_width() / 300, 20 + _y))
        _x += cell_width

    _y += 2 * cell_height

    for _, row in islice(df.iterrows(), 8):
        _x = 20
        for value in row:
            if isinstance(value, int) and value is not row.iloc[-1]:
                text = font.render(str(value + 1), True, black)
            else:
                text = font.render(str(value), True, black)
            if _x == 20:
                WIN.blit(text, (_x, _y))
            else:
                WIN.blit(text, (_x - WIN.get_width() / 9, _y))
            _x += cell_width
        _y += cell_height


def nick_input():
    _manager = pygame_gui.UIManager((WIN.get_width(), WIN.get_height()))
    _frame = (WIN.get_width() / 2, WIN.get_height() / 20)
    _text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
        (WIN.get_width() / 2 - _frame[0] / 2, WIN.get_height() / 2 - _frame[1] / 2), _frame),
        manager=_manager, object_id='#main_text_entry')

    return _manager, _frame, _text_input


def get_user_name():
    text = font.render("Wprowadź nazwę użytkownika i wciśnij klawisz ENTER:", True, dark_blue)
    _run = True

    manager, frame, text_input = nick_input()

    while _run:

        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                manager, frame, text_input = nick_input()
            elif (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                    event.ui_object_id == '#main_text_entry'):
                _run = False
                return event.text

            manager.process_events(event)

        manager.update(UI_REFRESH_RATE)

        WIN.fill("white")
        WIN.blit(text, (WIN.get_width() / 2 - text.get_width() / 2,
                        text_input.get_starting_height() + 5 * text.get_height()))

        manager.draw_ui(WIN)
        pygame.display.update()


def game(_play, _score):

    score_multiplier = multiplier(active_option, active_level_option, voivodeship_options, level_options)
    entity = Voivodeship(voivodeship=active_option, level=active_level_option, mode=mode)
    registration, county, answers = entity.ask_question()
    position_update()

    if not active_option == voivodeship_options[-1]:
        plates_left = len(loaded_dicts[voivodeship_options.index(active_option)])
    else:
        plates_left = 409

    while _play:

        if not active_option == voivodeship_options[-1]:
            score_perc = str(
                round(100 * _score / (score_multiplier * len(loaded_dicts[voivodeship_options.index(active_option)]))))
        else:
            score_perc = str(round(100 * _score / (score_multiplier * 409)))

        if mode == 1:
            score_surface = font_2.render("Poprawnie: " + score_perc + '%', True, black)
        else:
            score_surface = font_2.render("Poprawnie: " + str(_score), True, black)

        # bravo = font_2.render("Brawo!", True, green)
        registration_surface = font_2.render(registration, True, black)

        registration_template_position = (0.5 * WIN.get_width() - 0.5 * registration_template.get_width(),
                                          0.04 * WIN.get_height())
        registration_position = (0.5 * WIN.get_width() - 0.215 * registration_surface.get_width(),
                                 0.04 * WIN.get_height() + 0.5 * registration_template.get_height() -
                                 0.42 * registration_surface.get_height())

        draw_element_with_background(bright_blue, registration_template, registration_template_position)
        score_position = (0.9 * WIN.get_width() - score_surface.get_width(), registration_position.__getitem__(1))
        left_position = (0.1 * WIN.get_width(), registration_position.__getitem__(1))

        if mode == 1:
            left_surface = font_2.render("Pozostało: " + str(plates_left), True, black)
            WIN.blit(left_surface, left_position)

        WIN.blit(registration_surface, registration_position)
        WIN.blit(score_surface, score_position)

        for _event in pygame.event.get():

            if _event.type == pygame.QUIT:
                _play = exit_execute(_play, stage=1)
            elif _event.type == pygame.KEYDOWN:
                if _event.key == pygame.K_ESCAPE:
                    _play = exit_execute(_play, stage=1)
            elif _event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(_event.pos):
                    _play = exit_execute(_play, stage=1)

                for _i in range(2):
                    _x = first_answer.x if _i == 1 else WIN.get_width() - first_answer.x - first_answer.width
                    for _j in range(2):
                        _y = first_answer.y + _j * first_answer.y

                        _square_option = pygame.Rect(_x, _y, first_answer.width, first_answer.height)

                        if _square_option.collidepoint(_event.pos):
                            if answers[2 * _i + _j] == county:
                                _score += score_multiplier
                                plates_left -= 1
                                try:
                                    registration, county, answers = entity.ask_question()
                                except IndexError as e:
                                    print(e)
                                    show_message("Brawo!", "Wszystkie tablice zostały odgadnięte!")
                                    save_score(nickname, active_level_option, active_option, score_perc)
                                    _play = False
                            else:
                                plates_left -= 1
                                if mode == 0:
                                    _score = 0
                                try:
                                    registration, county, answers = entity.ask_question()
                                except IndexError as e:
                                    print(e)
                                    show_message("Brawo!", "Wszystkie tablice zostały odgadnięte!")
                                    save_score(nickname, active_level_option, active_option, score_perc)
                                    _play = False

        for _i in range(2):
            _x = first_answer.x if _i == 1 else WIN.get_width() - first_answer.x - first_answer.width
            for _j in range(2):
                _y = first_answer.y + _j * first_answer.y
                draw_rect((_x, _y, first_answer.width, first_answer.height), answers[2 * _i + _j], grey)

        draw_rect(exit_button, "Wyjdź", grey)
        pygame.display.flip()


while run:

    clock.tick(60)
    draw_element_with_background(white, app_logo, (0.5 * WIN.get_width() - 0.5 * app_logo.get_width(),
                                                   0.02 * WIN.get_height()))
    drop_down, level_drop_down, play_button, exit_button, first_answer, mode_button = position_update()
    render_dataframe(load_df("test.xlsx"))

    for event in pygame.event.get():
        if not nick_executed:
            nickname = get_user_name()
            nick_executed = True
        if event.type == pygame.QUIT:
            run = exit_execute(run)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = exit_execute(run)
        elif event.type == VIDEORESIZE:
            WIN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if drop_down.collidepoint(event.pos):
                full_list = not full_list
                full_level_list = False
            elif exit_button.collidepoint(event.pos):
                run = exit_execute(run)
            elif level_drop_down.collidepoint(event.pos):
                full_level_list = not full_level_list
                full_list = False
            elif mode_button.collidepoint(event.pos):
                mode = not mode
            elif full_list:
                for i, option in enumerate(voivodeship_options):
                    y = drop_down.y + (i + 1) * drop_down.height

                    square_option = pygame.Rect(drop_down.x, y, drop_down.width,
                                                drop_down.height)

                    if square_option.collidepoint(event.pos):
                        active_option = option
                        full_list = False
            elif full_level_list:
                for i, option in enumerate(level_options):
                    y = level_drop_down.y + (i + 1) * level_drop_down.height

                    square_option = pygame.Rect(level_drop_down.x, y, level_drop_down.width,
                                                level_drop_down.height)

                    if square_option.collidepoint(event.pos):
                        active_level_option = option
                        full_level_list = False

            if play_button.collidepoint(event.pos):
                if not active_option == "Wybierz województwo" and not active_level_option == "Wybierz poziom":
                    game(True, score)

    if active_option != 'Wybierz województwo' and active_level_option != 'Wybierz poziom':
        draw_rect(play_button, "Zagraj!", green)
    else:
        draw_rect(play_button, "Zagraj!", grey)

    if mode == 0:
        draw_rect(mode_button, tribes[mode], grey)
    else:
        draw_rect(mode_button, tribes[mode], dark_grey)

    draw_rect(exit_button, "Wyjdź", grey)
    draw_list(drop_down, voivodeship_options, active_list=full_list, active_choice=active_option)
    draw_list(level_drop_down, level_options, active_list=full_level_list, active_choice=active_level_option)

    pygame.display.flip()

# print("aaaaaa: " + nick)
#
# export_list(values_list, 'values_409_list.pickle')

# with open('lista_indeksow_poprawiona.txt', 'r') as file:
#     # Odczytaj zawartość pliku
#     lista_indeksow = [linia.strip() for linia in file.readlines()]
#
# with open('lista_powiatow_poprawiona.txt', 'r') as file:
#     # Odczytaj zawartość pliku
#     values_list = [linia.strip() for linia in file.readlines()]
#
# print(lista_indeksow)
# print(values_list)
#


# #zapis stringów do pliku w kolumnach
# with open('lista_indeksow_poprawiona.txt', 'w') as file:
#     file.writelines('\n'.join(key_list))
#
# #zapis stringów do pliku w kolumnach
# with open('lista_powiatow_poprawiona.txt', 'w') as file:
#     file.writelines('\n'.join(values_list))

# dicts_pickle_2 = import_list('dicts.pickle2')
# for dict in dicts_pickle_2:
#     if 'BS' in dict:
#         dict['BS'] = 'Suwałki(miasto)'
#     if 'BSU' in dict:
#         dict['BS'] = 'Suwałki(powiat)'
#     if 'DX' in dict:
#         dict['DX'] = 'Wrocław(miasto 2)'
#     if 'ED' in dict:
#         dict['ED'] = 'Łódź(miasto 2)'
#     if 'ESK' in dict:
#         dict['ESK'] = 'Skierniewice(powiat)'
#     if 'ES' in dict:
#         dict['ES'] = 'Skierniewice(miasto)'
#     if 'GWO' in dict:
#         dict['GWO'] = 'Wejherowo(powiat 2)'
#     if 'GWE' in dict:
#         dict['GWE'] = 'Wejherowo(powiat)'
#     if 'KBC' in dict:
#         dict['KBC'] = 'Bochnia(powiat)'
#     if 'KBA' in dict:
#         dict['KBA'] = 'Bochnia(powiat 2)'
#     if 'KK' in dict:
#         dict['KK'] = 'Kraków(miasto 2)'
#     if 'PY' in dict:
#         dict['PY'] = 'Poznań(miasto 2)'
#     if 'ZZ' in dict:
#         dict['ZZ'] = 'Szczecin(miasto 2)'
#     if 'ZS' in dict:
#         dict['ZS'] = 'Szczecin(miasto)'
# export_list(dicts_pickle_2, 'dicts.pickle3')
# yyy = {}
# xxx = import_list('dicts.pickle3')
# for dict_ in xxx:
#     yyy.update(dict_)
# export_list(yyy, 'testy.pickle')


# loaded_dicts = import_list('dicts.pickle3')
# key_list = []
#
# for voivodeship in range(len(loaded_dicts)):
#     for key, value in loaded_dicts[voivodeship].items():
#         values_list.append(value)
#         key_list.append(key)
#
# export_list(key_list, '409_indices.pickle')
# export_list(values_list, '409_values.pickle')
#
#
# _matrix = np.zeros((len(values_list), len(values_list)))
#
# # import_list('409_values.pickle')
#
# for num, element in enumerate(values_list):
#     for num_2, _element in enumerate(values_list):
#
#         for i in range(3):
#             if element[:i] == _element[:i]:
#                 _matrix[num][num_2] += i
# #
# df = pd.DataFrame(_matrix, columns=values_list, index=values_list)
# # df.to_csv('extreme.csv')
# df.to_pickle('extreme_matrix.pickle')
#


#
# levenshtein_matrix = np.zeros((len(values_list), len(values_list)))
#
# for num, element in enumerate(values_list):
#     for num_2, _element in enumerate(values_list):
#         levenshtein_matrix[num][num_2] = Levenshtein.distance(element, _element)
#
# df = pd.DataFrame(levenshtein_matrix, columns=values_list, index=values_list)

# df.to_pickle('levenshtein_matrix.pickle')


# print(levenshtein_matrix)

# print(loaded_dicts['Podlaskie'])
# print(voivodeship_options[0])
# print(voivodeship_options.index('Podlaskie'))
#
# print(Voivodeship.get_random_question())
# df = pd.DataFrame(levenshtein_matrix)
# for i in range(409):
#     for j in range(409):
#         if j>i:
#             df.iat[i, j] = ''
