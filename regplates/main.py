if __package__:
    from .Constants import Color, Level, APP_LOGO_IMAGE_PATH, VOIVODESHIP_OPTIONS_LIST, RANKING_CSV_PATH
    from .Utils import get_resource_path
    from .Game import Game
else:
    from Constants import Color, Level, APP_LOGO_IMAGE_PATH, VOIVODESHIP_OPTIONS_LIST, RANKING_CSV_PATH
    from Utils import get_resource_path
    from Game import Game

from itertools import islice
import pandas as pd
from enum import Enum
import pygame
import pygame_gui

"""
Configuration file with pygame initialization, color definitions, image imports and variable set

Functions
----------
load_df(file)
    a function used to read excel file and put it into DataFrame collection sorted by last column (score points) 
    descending
position_update()
    a function used to make start window elements resizable
draw_rect(position, text, button_color)
    a function used to draw rectangular with frame and filled out with the text in specific position
write_text(text, location)
    a function used to write and blit the text in specific position
draw_list(position, options, active_list, active_choice)
    a function used to draw dropdown list in specific position
render_dataframe(df)
    a function which render DataFrame collection content to be displayed in GUI
nick_input()
    a function used to initialization elements needed for getting user name function control   
get_user_name()
    a function used to manage getting user name view
handle_drop_down_event(_drop_down, _options, _event, _full_list_flag, _active_option)
    a function used to spot and execute dropdown list handling
"""


def position_update(WIN, app_logo):
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

    _mode_button = pygame.Rect(WIN.get_width() / 2 - 0.0625 * WIN.get_width(),
                               20 + 1.1 * app_logo.get_height(),
                               0.125 * WIN.get_width(),
                               0.04 * WIN.get_height())

    return _drop_down, _level_drop_down, _play_button, _exit_button, _mode_button


def draw_rect(position, text, button_color, WIN):
    pygame.draw.rect(WIN, button_color, position)  # draw rectangular
    pygame.draw.rect(WIN, Color.WHITE.value, position, 2)  # draw the frame
    write_text(text.value if isinstance(text, Enum) else text, (position[0] + position[2] // 2, position[1] + position[3] // 2), WIN)


def write_text(text, location, WIN):
    font = pygame.font.Font(None, 32)
    text_surface = font.render(text, True, Color.WHITE.value)
    text_location = text_surface.get_rect(center=location)
    WIN.blit(text_surface, text_location)


def draw_list(position, options, active_list, active_choice, WIN):
    draw_rect(position, active_choice, Color.ACTIVE_GREEN.value if active_list else Color.GREEN.value, WIN)

    if active_list:
        for i, option in enumerate(options):
            y = position[1] + (i + 1) * position.height

            pygame.draw.rect(WIN, Color.DARK_GREY.value, (position[0], y, position.width, position.height))

            pygame.draw.rect(WIN, Color.WHITE.value, (position[0], y, position.width, position.height), 2)
            write_text(option.value if isinstance(option, Enum) else option, (position[0] + position.width // 2, y + position.height // 2), WIN)


def render_dataframe(df, WIN):

    font = pygame.font.Font(None, 32)
    font_2 = pygame.font.Font(None, 72)

    _x, _y = WIN.get_width() / 10, WIN.get_height() / 2.8
    cell_width, cell_height = WIN.get_width() / 5, WIN.get_height() / 30

    text = font_2.render("Ranking:", True, Color.DARK_BLUE.value)
    WIN.blit(text, (20, 20 + WIN.get_height() / 3.9))

    for col in df.columns[1:]:
        text = font.render(col, True, Color.BLACK.value)
        WIN.blit(text, (_x - WIN.get_width() / 300, 20 + _y))
        _x += cell_width

    _y += 2 * cell_height

    for num, (_, row) in enumerate(islice(df.iterrows(), 10), start=1):
        _x = 20
        for value in row:
            if isinstance(value, int) and value is not row.iloc[-1]:
                text = font.render(str(num), True, Color.BLACK.value)
            else:
                text = font.render(str(value), True, Color.BLACK.value)

            if _x == 20:
                WIN.blit(text, (_x, _y))
            else:
                WIN.blit(text, (_x - WIN.get_width() / 9, _y))
            _x += cell_width
        _y += cell_height


def nick_input(WIN):
    _manager = pygame_gui.UIManager((WIN.get_width(), WIN.get_height()))
    _frame = (WIN.get_width() / 2, WIN.get_height() / 20)
    _text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
        (WIN.get_width() / 2 - _frame[0] / 2, WIN.get_height() / 2 - _frame[1] / 2), _frame),
        manager=_manager, object_id='#main_text_entry')

    return _manager, _frame, _text_input


def get_user_name(clock, WIN):

    font = pygame.font.Font(None, 32)
    text = font.render("Wprowadź nazwę użytkownika i wciśnij klawisz ENTER:", True, Color.DARK_BLUE.value)
    _run = True

    manager, frame, text_input = nick_input(WIN)
    text_input.focus()

    while _run:

        for _event in pygame.event.get():
            if _event.type == pygame.VIDEORESIZE:
                manager, frame, text_input = nick_input(WIN)
                text_input.focus()
            elif _event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and _event.ui_object_id == '#main_text_entry':
                _run = False
                return _event.text

            manager.process_events(_event)

        manager.update(clock.tick(60) / 10000)

        WIN.fill("white")
        WIN.blit(text, (WIN.get_width() / 2 - text.get_width() / 2,
                        text_input.get_starting_height() + 5 * text.get_height()))

        manager.draw_ui(WIN)
        pygame.display.update()


def handle_drop_down_event(_drop_down, _options, _full_list_flag, _active_option, event):
    if _full_list_flag:
        for _i, _option in enumerate(_options):
            _y = _drop_down.y + (_i + 1) * _drop_down.height
            square_option = pygame.Rect(_drop_down.x, _y, _drop_down.width, _drop_down.height)

            if square_option.collidepoint(event.pos):
                _active_option = _option
                _full_list_flag = False
    return _active_option.value if isinstance(_active_option, Enum) else _active_option, _full_list_flag


def main_function():
    pygame.init()
    pygame.font.init()
    try:
        pygame.mixer.init()
    except pygame.error as e:
        print(str(e))
    WIN = pygame.display.set_mode((1400, 800), pygame.RESIZABLE)
    pygame.display.set_caption("Registration Plates Quiz")   

    clock = pygame.time.Clock()

    run = True
    full_list = False
    nick_executed = False
    full_level_list = False
    nickname = "Unknown"
    active_option = "Wybierz województwo"
    active_level_option = "Wybierz poziom"
    tribes = {0: 'Powtarzanie', 1: 'Bez powtórzeń'}
    mode = 0

    # Drop down options
    voivodeship_options = VOIVODESHIP_OPTIONS_LIST
    # Loading images
    app_logo = pygame.image.load(get_resource_path(APP_LOGO_IMAGE_PATH))

    while run:

        drop_down, level_drop_down, play_button, exit_button, mode_button = position_update(WIN, app_logo)
        WIN.fill(Color.WHITE.value)
        WIN.blit(app_logo, (0.5 * WIN.get_width() - 0.5 * app_logo.get_width(), 0.02 * WIN.get_height()))

        ranking_df = pd.read_csv(get_resource_path(RANKING_CSV_PATH))
        ranking_df.sort_values(by=ranking_df.columns[-1], ascending=False, inplace=True)
        render_dataframe(ranking_df,WIN)

        for event in pygame.event.get():
            if not nick_executed:
                nickname = get_user_name(clock,WIN)
                nick_executed = True
            if event.type == pygame.QUIT:
                run = Game.exit_execute()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = Game.exit_execute()
            elif event.type == pygame.VIDEORESIZE:
                WIN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if drop_down.collidepoint(event.pos):
                    full_list = not full_list
                    full_level_list = False
                elif exit_button.collidepoint(event.pos):
                    run = Game.exit_execute()
                elif level_drop_down.collidepoint(event.pos):
                    full_level_list = not full_level_list
                    full_list = False
                elif mode_button.collidepoint(event.pos):
                    mode = not mode
                elif full_list:
                    active_option, full_list = handle_drop_down_event(drop_down, voivodeship_options, full_list,
                                                                      active_option, event)
                elif full_level_list:
                    active_level_option, full_level_list = handle_drop_down_event(level_drop_down, Level,
                                                                                  full_level_list, active_level_option, event)
                if play_button.collidepoint(event.pos):
                    if not active_option == "Wybierz województwo" and not active_level_option == "Wybierz poziom":
                        if active_option == voivodeship_options[-1] and active_level_option == Level.EASY.value:
                            Game.config_notification()
                        else:
                            game_instance = Game(WIN, active_option, active_level_option, mode, nickname)

        draw_rect(mode_button, tribes[mode], Color.DARK_GREY.value if mode != 0 else Color.GREY.value, WIN)
        draw_list(drop_down, voivodeship_options, active_list=full_list, active_choice=active_option, WIN=WIN)
        draw_list(level_drop_down, Level, active_list=full_level_list, active_choice=active_level_option, WIN=WIN)
        draw_rect(exit_button, "Wyjdź", Color.GREY.value, WIN)
        draw_rect(play_button, "Zagraj!",
                  Color.GREEN.value if active_option != 'Wybierz województwo' and active_level_option != 'Wybierz poziom' else Color.GREY.value, WIN)

        pygame.display.flip()


if __name__ == "__main__":
    main_function()
