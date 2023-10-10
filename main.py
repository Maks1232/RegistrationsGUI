import pandas as pd
import pygame
import os
import pickle
import numpy as np
import Levenshtein
from voivodeship_class import Voivodeship

pygame.font.init()
pygame.mixer.init()

# Window creation
WIDTH, HEIGHT = (1920, 1080)
# WIDTH, HEIGHT = (1800, 900)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Registration Plates Quiz")

# Kolory
active_color = (0, 255, 255)
background_color = (255, 255, 255)
button_color = (150, 150, 150)
active_button_color = (100, 100, 100)
text_color = (255, 255, 255)
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
values_list = []
score = 0

# Loading images
app_logo = pygame.image.load(os.path.join('Images', 'title_v1.png'))
registration_template = pygame.image.load(os.path.join('Images', 'registration_template.png'))
car_plates_map = pygame.image.load(os.path.join('Images', 'carplates.png'))


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
voivodeship_options = import_list(file_name='voivodeship_options')
level_options = ["Easy", "Hard"]


def draw_element(color, element, position):
    WIN.fill(color)
    WIN.blit(element, position)


def draw_rect(position, text):
    pygame.draw.rect(WIN, button_color, position)
    pygame.draw.rect(WIN, text_color, position, 2)
    write_text(text,
               (position[0] + position[2] // 2, position[1] + position[3]// 2))


def write_text(text, location):
    text_surface = font.render(text, True, text_color)
    text_location = text_surface.get_rect(center=location)
    WIN.blit(text_surface, text_location)


def draw_list(position, options, active_list, active_choice):
    draw_rect(position, active_choice)

    if active_list:

        for i, option in enumerate(options):
            y = position[1] + (i + 1) * position.height
            pygame.draw.rect(WIN, button_color, (position[0], y, position.width, position.height))
            pygame.draw.rect(WIN, text_color, (position[0], y, position.width, position.height), 2)
            write_text(option, (position[0] + position.width // 2, y + position.height // 2))


def game(play, score):
    entity = Voivodeship(voivodeship=active_option, level=active_level_option)
    score_surface = font_2.render("Score: " + str(score), True, black)
    registration, county, answers = entity.ask_question()
    registration_surface = font_2.render(registration, True, black)
    registration_position = (0.5 * WIDTH - 0.5 * registration_surface.get_width()
                             + 0.27 * registration_surface.get_width(),
                             0.04 * HEIGHT + 0.5 * registration_template.get_height() -
                             0.42 * registration_surface.get_height())

    while play:

        draw_element((175, 238, 238), registration_template, registration_template_position)
        score_position = (WIDTH - 2 * score_surface.get_width(), registration_position.__getitem__(1))
        WIN.blit(registration_surface, registration_position)
        WIN.blit(score_surface, score_position)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                play = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    play = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    play = False
                for i in range(2):
                    for j in range(2):
                        if i == 1:
                            x = first_answer.x
                        else:
                            x = WIDTH - first_answer.x - first_answer.width

                        y = first_answer.y + j * first_answer.y

                        square_option = pygame.Rect(x, y, first_answer.width, first_answer.height)

                        if square_option.collidepoint(event.pos):
                            if answers[2 * i + j] == county:
                                score += 1
                                play = not play
                                game(True, score)
                            else:
                                score = 0
                                play = not play
                                game(True, score)

        for i in range(2):
            for j in range(2):
                if i == 1:
                    x = first_answer.x
                else:
                    x = WIDTH - first_answer.x - first_answer.width
                y = first_answer.y + j * first_answer.y

                draw_rect((x, y, first_answer.width, first_answer.height), answers[2 * i + j])

        draw_rect(exit_button, "Exit")
        pygame.display.flip()


clock = pygame.time.Clock()
run = True

while run:

    clock.tick(60)
    draw_element(background_color, app_logo, (0.5*WIDTH-0.5*app_logo.get_width(), 0.02*HEIGHT))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # response = pygame.messagebox.askyesno("Potwierdzenie zamknięcia", "Czy na pewno chcesz zamknąć program?")
            # if response:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if drop_down.collidepoint(event.pos):
                full_list = not full_list
                full_level_list = False
            elif exit_button.collidepoint(event.pos):
                run = False
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
                play = True
                game(play, score)

    draw_rect(play_button, "Play!")
    draw_rect(exit_button, "Exit")
    draw_list(drop_down, voivodeship_options, active_list=full_list, active_choice=active_option)
    draw_list(level_drop_down, level_options, active_list=full_level_list, active_choice=active_level_option)

    pygame.display.flip()


# loaded_dicts = import_list('dicts.pickle2')
#
# for voivodeship in range(len(loaded_dicts)):
#     for key, value in loaded_dicts[voivodeship].items():
#         values_list.append(value)
#
# levenshtein_matrix = np.zeros((len(values_list), len(values_list)))
#
# for num, element in enumerate(values_list):
#     for num_2, _element in enumerate(values_list):
#         levenshtein_matrix[num][num_2] = Levenshtein.distance(element, _element)
#
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
# print(df)
# df.to_csv("aaaa.csv", index=False)
