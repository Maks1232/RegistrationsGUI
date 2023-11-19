from itertools import islice
import pygame.freetype
from pygame.locals import *
from config import *


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


def draw_rect(position, text, button_color):
    pygame.draw.rect(WIN, button_color, position)  # draw rectangular
    pygame.draw.rect(WIN, white, position, 2)  # draw the frame
    write_text(text, (position[0] + position[2] // 2, position[1] + position[3] // 2))


def write_text(text, location):
    font = pygame.font.Font(None, 32)
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


def render_dataframe(df):

    font = pygame.font.Font(None, 32)
    font_2 = pygame.font.Font(None, 72)

    _x, _y = WIN.get_width() / 10, WIN.get_height() / 2.8
    cell_width, cell_height = WIN.get_width() / 5, WIN.get_height() / 30

    text = font_2.render("Ranking:", True, dark_blue)
    WIN.blit(text, (20, 20 + WIN.get_height() / 3.9))

    for col in df.columns[1:]:
        text = font.render(col, True, black)
        WIN.blit(text, (_x - WIN.get_width() / 300, 20 + _y))
        _x += cell_width

    _y += 2 * cell_height

    for num, (_, row) in enumerate(islice(df.iterrows(), 10), start=1):
        _x = 20
        for value in row:
            if isinstance(value, int) and value is not row.iloc[-1]:
                text = font.render(str(num), True, black)
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

    font = pygame.font.Font(None, 32)

    text = font.render("Wprowadź nazwę użytkownika i wciśnij klawisz ENTER:", True, dark_blue)
    _run = True

    manager, frame, text_input = nick_input()
    text_input.focus()

    while _run:

        for _event in pygame.event.get():
            if _event.type == VIDEORESIZE:
                manager, frame, text_input = nick_input()
                text_input.focus()
            elif _event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and _event.ui_object_id == '#main_text_entry':
                _run = False
                return _event.text

            manager.process_events(_event)

        manager.update(UI_REFRESH_RATE)

        WIN.fill("white")
        WIN.blit(text, (WIN.get_width() / 2 - text.get_width() / 2,
                        text_input.get_starting_height() + 5 * text.get_height()))

        manager.draw_ui(WIN)
        pygame.display.update()


def handle_drop_down_event(_drop_down, _options, _event, _full_list_flag, _active_option):
    if _full_list_flag:
        for _i, _option in enumerate(_options):
            _y = _drop_down.y + (_i + 1) * _drop_down.height
            square_option = pygame.Rect(_drop_down.x, _y, _drop_down.width, _drop_down.height)

            if square_option.collidepoint(event.pos):
                _active_option = _option
                _full_list_flag = False
    return _active_option, _full_list_flag


if __name__ == "__main__":

    while run:

        WIN.fill(white)
        WIN.blit(app_logo, (0.5 * WIN.get_width() - 0.5 * app_logo.get_width(), 0.02 * WIN.get_height()))
        drop_down, level_drop_down, play_button, exit_button, first_answer, mode_button = position_update()

        render_dataframe(load_df("ranking.xlsx"))

        for event in pygame.event.get():
            if not nick_executed:
                nickname = get_user_name()
                nick_executed = True
            if event.type == pygame.QUIT:
                run = Game.exit_execute()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = Game.exit_execute()
            elif event.type == VIDEORESIZE:
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
                    active_option, full_list = handle_drop_down_event(drop_down, voivodeship_options, event, full_list,
                                                                      active_option)
                elif full_level_list:
                    active_level_option, full_level_list = handle_drop_down_event(level_drop_down, level_options, event,
                                                                                  full_level_list, active_level_option)
                if play_button.collidepoint(event.pos):
                    if not active_option == "Wybierz województwo" and not active_level_option == "Wybierz poziom":
                        if active_option == voivodeship_options[-1] and active_level_option == level_options[0]:
                            Game.config_notification()
                        else:
                            game_instance = Game(WIN, active_option, active_level_option, mode, nickname)
                            game_instance.run()

        draw_rect(mode_button, tribes[mode], dark_grey if mode != 0 else grey)
        draw_list(drop_down, voivodeship_options, active_list=full_list, active_choice=active_option)
        draw_list(level_drop_down, level_options, active_list=full_level_list, active_choice=active_level_option)
        draw_rect(exit_button, "Wyjdź", grey)
        draw_rect(play_button, "Zagraj!",
                  green if active_option != 'Wybierz województwo' and active_level_option != 'Wybierz poziom' else grey)

        pygame.display.flip()
