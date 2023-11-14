import pygame
import sys
import os
from AnswerRect import *
from Voivodeship import *
from tkinter import messagebox

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

reg_template = pygame.image.load(os.path.join('Images', 'registration_template.png'))


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


def multiplier(voivodeship, level, voivodeship_base):

    level_base = ["Easy", "Medium", "Hard", "Extreme"]

    multipliers = {
        (voivodeship_base[-1], level_base[-1]): (2, 3),
        (voivodeship_base[-1], level_base[-2]): (2, 2),
        (voivodeship_base[-1], level_base[0]): (0, 1),
        (not voivodeship_base[-1], level_base[-1]): (1, 2),
        (not voivodeship_base[-1], level_base[-2]): (0, 1)
    }

    a, b = multipliers.get((voivodeship, level), (1, 0))

    return a + b


class Game:
    def __init__(self, screen, active_option, active_level_option, mode, nickname):
        self.nickname = nickname
        self.active_option = active_option
        self.active_level_option = active_level_option
        self.mode = mode
        self._play = True
        self._score = 0
        self.screen = screen
        self.manager = pygame_gui.UIManager((screen.get_width(), screen.get_height()))
        self.voivodeship = Voivodeship(voivodeship=self.active_option, level=self.active_level_option, mode=self.mode)
        self.questions_left = self.voivodeship.all
        self.registration, self.county, self.answers = self.voivodeship.ask_question()
        self.answer_blocks = [
            AnswerRect(0.1 * screen.get_width(),
                       0.47 * screen.get_height(),
                       0.5 * screen.get_height(),
                       0.1 * screen.get_height(),
                       self.answers[0], self.manager),
            AnswerRect(0.9 * screen.get_width() - 0.5 * screen.get_height(),
                       0.47 * screen.get_height(),
                       0.5 * screen.get_height(),
                       0.1 * screen.get_height(),
                       self.answers[1], self.manager),
            AnswerRect(0.1 * screen.get_width(),
                       0.67 * screen.get_height(),
                       0.5 * screen.get_height(),
                       0.1 * screen.get_height(),
                       self.answers[2], self.manager),
            AnswerRect(0.9 * screen.get_width() - 0.5 * screen.get_height(),
                       0.67 * screen.get_height(),
                       0.5 * screen.get_height(),
                       0.1 * screen.get_height(),
                       self.answers[3], self.manager),
        ]
        self.multiplier = multiplier(self.active_option, self.active_level_option, self.voivodeship.voivodeship_options)
        self.score_percentage = round(100 * self._score / (self.multiplier * self.voivodeship.all))

        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(0.9 * self.screen.get_width() - 0.25 * self.screen.get_height(),
                                      0.86 * self.screen.get_height(),
                                      0.25 * self.screen.get_height(),
                                      0.04 * self.screen.get_height()),
            text='Wyjdź',
            manager=self.manager
        )
        self.update_question_info()
        self.update_score_info()
        self.run()

    def run(self):
        clock = pygame.time.Clock()

        while self._play:
            time_delta = clock.tick(60) / 1000.0

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self._play = self.exit_execute()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._play = self.exit_execute()
                if event.type == pygame.VIDEORESIZE:
                    pass
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.exit_button:
                            self._play = self.exit_execute()
                        else:
                            self.handle_answer_click(event.ui_element)

                        self.next_question()
                        self.update_answer_blocks()

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.draw_elements()

            self.manager.draw_ui(self.screen)

            pygame.display.flip()

    def next_question(self):
        try:
            self.registration, self.county, self.answers = self.voivodeship.ask_question()
        except IndexError as e:
            print(e)
            self.notification()
            self.update_question_info()
            self.update_score_info()
            save_score(self.nickname, self.active_level_option, self.active_option, self.score_percentage)
            self._play = False

    def update_answer_blocks(self):
        for i, answer_block in enumerate(self.answer_blocks):
            self.answer_blocks[i].update_text(self.answers[i])

    def draw_elements(self):
        self.screen.fill(bright_blue)

        font = pygame.font.Font(None, 72)
        reg_surface = font.render(self.registration, True, black)
        font = pygame.font.Font(None, 40)
        user_information = font.render("Wybierz nazwę miejscowości, której odpowiada wyświetlany "
                                       "powyżej indeks rejestracyjny:", True, dark_blue)

        self.screen.blit(reg_template, (0.5 * self.screen.get_width() - 0.5 * reg_template.get_width(),
                                        0.04 * self.screen.get_height()))
        self.screen.blit(reg_surface, (0.5 * self.screen.get_width() + 0.12085 * reg_template.get_width() -
                                       0.5 * reg_surface.get_width(), 0.04 * self.screen.get_height() +
                                       0.5 * reg_template.get_height() - 0.42 * reg_surface.get_height()))
        self.screen.blit(user_information, (0.5 * self.screen.get_width() - 0.5 * user_information.get_width(),
                                            0.04 * self.screen.get_height() + 2 * reg_template.get_height()))

        for block in self.answer_blocks:
            block.button.update(0)

        self.exit_button.update(0)
        self.update_question_info()
        self.update_score_info()

    def update_question_info(self):
        if self.mode == 1:
            font = pygame.font.Font(None, 48)
            text = font.render(f"Pozostało: {self.questions_left}", True, black)
            self.screen.blit(text, (0.1 * self.screen.get_width(),
                                    0.04 * self.screen.get_height() + 0.5 * text.get_height()))

    def update_score_info(self):

        font = pygame.font.Font(None, 48)
        if self.mode == 1:
            self.score_percentage = round(100 * self._score / (self.multiplier * self.voivodeship.all))
            text = font.render(f"Twój wynik: {self.score_percentage}%", True, black)
        else:
            text = font.render(f"Twój wynik: {self._score }", True, black)

        self.screen.blit(text, (0.9 * self.screen.get_width() - text.get_width(),
                                0.04 * self.screen.get_height() + 0.5 * text.get_height()))

    def handle_answer_click(self, clicked_block):
        for block in self.answer_blocks:
            if block.button == clicked_block and block.text == self.county:
                self._score += self.multiplier
        self.questions_left += -1

    @staticmethod
    def exit_execute():
        if messagebox.askquestion("Potwierdzenie", "Czy na pewno chcesz wyjść do menu?") == "no":
            return True

    @staticmethod
    def notification():
        messagebox.askquestion("Potwierdzenie", "Czy na pewno chcesz wyjść do menu?")