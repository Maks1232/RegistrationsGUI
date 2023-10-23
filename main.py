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

pygame.font.init()
pygame.mixer.init()

# Window creation
# WIDTH, HEIGHT = (1920, 1080)
WIDTH, HEIGHT = (1800, 900)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Registration Plates Quiz")

# Kolory
white = (255, 255, 255)
aqua = (0, 255, 255)
red = (255, 0, 0)
grey = (150, 150, 150)
dark_grey = (100, 100, 100)
green = (60, 179, 113)
black = (0, 0, 0)

# Font
font = pygame.font.Font(None, 32)
font_2 = pygame.font.Font(None, 72)


# Variables
play = False
full_list = False
full_level_list = False
active_option = "Choose voivodeship"
active_level_option = "Choose level"
mode = 1
values_list = []
score = 0

# Loading images
app_logo = pygame.image.load(os.path.join('Images', 'title_v1.png'))
registration_template = pygame.image.load(os.path.join('Images', 'registration_template.png'))
car_plates_map = pygame.image.load(os.path.join('Images', 'carplates.png'))
car_plates_map = pygame.transform.scale(car_plates_map, (0.9*WIDTH, 0.9*HEIGHT))


# Export list to the file
def export_list(voivodeship_options, file_name):
    with open(file_name, 'wb') as file:
        pickle.dump(voivodeship_options, file)


# Import list from the file
def import_list(file_name):
    with open(file_name, 'rb') as file:
        imported_list = pickle.load(file)
    return imported_list


# Pozycje pól rozwijanych
drop_down = pygame.Rect(WIDTH - (WIDTH * 0.9), 20 + app_logo.get_height(), WIDTH * 0.25, 0.04 * HEIGHT)
level_drop_down = pygame.Rect(WIDTH - (WIDTH * 0.10 + WIDTH * 0.25), 20 + app_logo.get_height(), WIDTH * 0.25,
                              0.04 * HEIGHT)

play_button = pygame.Rect(WIDTH*0.65, 0.9*HEIGHT-0.08*HEIGHT, HEIGHT*0.25, 0.04*HEIGHT)
exit_button = pygame.Rect(WIDTH*0.65, 0.9*HEIGHT-0.04*HEIGHT, HEIGHT*0.25, 0.04*HEIGHT)

registration_template_position = (0.5*WIDTH-0.5*registration_template.get_width(), 0.04*HEIGHT)

first_answer = pygame.Rect(WIDTH*0.1, 0.4*HEIGHT-0.08*HEIGHT, HEIGHT*0.5, 0.1*HEIGHT)

# Opcje pola rozwijanego
loaded_dicts = import_list('dicts.pickle3')
voivodeship_options = import_list(file_name='voivodeship_options')
level_options = ["Easy", "Medium", "Hard", "Extreme"]


def draw_element(color, element, position):
    WIN.fill(color)
    WIN.blit(element, position)


def draw_rect(position, text, button_color):
    pygame.draw.rect(WIN, button_color, position)
    pygame.draw.rect(WIN, white, position, 2)
    write_text(text,
               (position[0] + position[2] // 2, position[1] + position[3]// 2))


def write_text(text, location):
    text_surface = font.render(text, True, white)
    text_location = text_surface.get_rect(center=location)
    WIN.blit(text_surface, text_location)


def draw_list(position, options, active_list, active_choice):
    draw_rect(position, active_choice, grey)

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


def multiplicator(voivodeship, level, voivodeship_base, level_base):

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
    elif voivodeship == voivodeship_base[-1] and level == level_base[0] or not voivodeship == voivodeship_base[-1] and level == level_base[-2]:
        b = 1

    return a + b


def game(_play, _score):

    score_multiplicator = multiplicator(active_option, active_level_option, voivodeship_options, level_options)
    if not active_option == 'Wszystkie':
        plates_left = len(loaded_dicts[voivodeship_options.index(active_option)])
    else:
        plates_left = 409

    entity = Voivodeship(voivodeship=active_option, level=active_level_option, mode=mode)
    registration, county, answers = entity.ask_question()

    while _play:

        score_surface = font_2.render("Score: " + str(_score), True, black)
        left_surface = font_2.render("Plates left: " + str(plates_left), True, black)
        registration_surface = font_2.render(registration, True, black)

        registration_position = (0.5 * WIDTH - 0.5 * registration_surface.get_width()
                                 + 0.27 * registration_surface.get_width(),
                                 0.04 * HEIGHT + 0.5 * registration_template.get_height() -
                                 0.42 * registration_surface.get_height())

        draw_element((175, 238, 238), registration_template, registration_template_position)
        score_position = (WIDTH - 2 * score_surface.get_width(), registration_position.__getitem__(1))
        left_position = (score_surface.get_width(), registration_position.__getitem__(1))

        WIN.blit(registration_surface, registration_position)
        WIN.blit(score_surface, score_position)
        WIN.blit(left_surface, left_position)

        for _event in pygame.event.get():

            if _event.type == pygame.QUIT:
                _play = exit_execute(_play, stage=1)
            elif _event.type == pygame.KEYDOWN:
                if _event.key == pygame.K_ESCAPE:
                    _play = exit_execute(_play, stage=1)
            elif _event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(_event.pos):
                    _play = exit_execute(_play, stage=1)
                for i in range(2):
                    for j in range(2):
                        if i == 1:
                            x = first_answer.x
                        else:
                            x = WIDTH - first_answer.x - first_answer.width

                        y = first_answer.y + j * first_answer.y

                        _square_option = pygame.Rect(x, y, first_answer.width, first_answer.height)

                        if _square_option.collidepoint(_event.pos):
                            if answers[2 * i + j] == county:
                                _score += score_multiplicator
                                plates_left -= 1
                                try:
                                    registration, county, answers = entity.ask_question()
                                except Exception:
                                    show_message("Brawo!", "Wszystkie tablice zostały odgadnięte!")
                                    _play = False
                            else:
                                plates_left -= 1
                                if mode == 0:
                                    _score = 0
                                try:
                                    registration, county, answers = entity.ask_question()
                                except Exception:
                                    show_message("Brawo!", "Wszystkie tablice zostały odgadnięte!")
                                    _play = False
        for i in range(2):
            for j in range(2):
                if i == 1:
                    x = first_answer.x
                else:
                    x = WIDTH - first_answer.x - first_answer.width
                y = first_answer.y + j * first_answer.y

                draw_rect((x, y, first_answer.width, first_answer.height), answers[2 * i + j], grey)

        draw_rect(exit_button, "Exit", grey)
        pygame.display.flip()


clock = pygame.time.Clock()
run = True

while run:

    clock.tick(60)
    draw_element(white, app_logo, (0.5 * WIDTH - 0.5 * app_logo.get_width(), 0.02 * HEIGHT))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = exit_execute(run)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = exit_execute(run)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if drop_down.collidepoint(event.pos):
                full_list = not full_list
                full_level_list = False
            elif exit_button.collidepoint(event.pos):
                run = exit_execute(run)
            elif level_drop_down.collidepoint(event.pos):
                full_level_list = not full_level_list
                full_list = False
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
                if not active_option == "Choose voivodeship" and not active_level_option == "Choose level":
                    game(True, score)

    if active_option != 'Choose voivodeship' and active_level_option != 'Choose level':
        draw_rect(play_button, "Play!", green)
    else:
        draw_rect(play_button, "Play!", grey)

    draw_rect(exit_button, "Exit", grey)
    draw_list(drop_down, voivodeship_options, active_list=full_list, active_choice=active_option)
    draw_list(level_drop_down, level_options, active_list=full_level_list, active_choice=active_level_option)

    pygame.display.flip()
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

