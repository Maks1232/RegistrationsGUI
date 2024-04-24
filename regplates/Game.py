import os
from regplates.AnswerRect import AnswerRect
from regplates.Voivodeship import Voivodeship
from tkinter import messagebox
import pygame
import regplates
import pygame_gui
import pandas as pd

# Colors
white = (255, 255, 255)
aqua = (0, 255, 255)
red = (255, 0, 0)
grey = (150, 150, 150)
dark_grey = (100, 100, 100)
green = (60, 179, 113)
black = (0, 0, 0)
dark_blue = (66, 0, 249)
bright_blue = (175, 238, 238)

dir_name = os.path.realpath("..")
reg_template = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(regplates.__file__)),'Images', 'registration_template.png'))


class Game:
    """
    A class used to manage game session view including interactive answer blocks handling and information displaying

    Attributes
    ----------
    screen : object
        a PyGame object representing application window
    active_option : str
        an attribute which store active voivodeship name selected by user
    active_level_option : str
        an attribute which store active difficulty level selected by user
    mode : int
        an attribute that determines game mode repetitive or non-repetitive
    nickname : str
        a string representing username
    _play : bool
        an attribute for program loop control
    _score: int
        a value representing current number of collected game points
    manager: object
        a pygame_gui.UIManager object for help answer block control
    voivodeship: object
        a custom voivodeship class object instance enabling game session handling
    registration: str
        a registration plate index obtained with voivodeship class mechanisms
    county: str
        a city name belonged to registration plate index obtained with voivodeship class mechanisms
    answers: list
        a list of obtained with voivodeship class mechanisms answers conditioned by registration attribute value
    questions_left: int
        a number of remaining registration plate indices to be drawn in current game session
    answer_blocks: object
        a view element used for represent interactive rectangular to show city name and spot the click action
    multiplier: int
        a number to be recognized as score multiplier conditioned by arguments sent during game class object instance
        creation
    score_percentage: int
        a _score expressed as value in percentage format
    exit_button: object
        a view element used for represent interactive rectangular to make exit action available
    Methods
    -------
    run()
        a method to make game session algorithm automated
    multiplier()
        a method used to calculate appropriate score multiplier conditioned by arguments sent during game class object
        instance creation
    save_score(file)
        a method for doing score save to the Excel file
    next_question()
        a method triggering next question display
    update_answer_blocks()
        a method used for update answer block content after next_question method triggered
    draw_elements(delta)
        a method used for drawing each game session view element on the screen
    update_question_info(delta)
        a method used for update number of displayed left registration plate indices value in non-repetitive mode
    update_score_info(delta)
        a method used for update number of displayed score value in game session
    handle_answer_click(clicked_block)
        a method used for handle spotted answer block click
    reset()
        a method used for spot and handle reset procedure need
    exit_execute()
        a method used for spot and handle exit procedure if needed
    notification()
        a method used for spot and display user notification if needed
    config_notification()
        a method used for spot and display user notification different than previous if needed
    Raises
    -------
    IndexError
        If method returns that exception it is a signal that the registration plate indices pool is empty

    """
    def __init__(self, screen, active_option, active_level_option, mode, nickname):
        self.screen = screen
        self.active_option = active_option
        self.active_level_option = active_level_option
        self.mode = mode
        self.nickname = nickname
        self._play = True
        self._score = 0
        self.manager = pygame_gui.UIManager((screen.get_width(), screen.get_height()))
        self.voivodeship = Voivodeship(voivodeship=self.active_option, level=self.active_level_option, mode=self.mode)
        self.registration, self.county, self.answers = self.voivodeship.ask_question()
        self.questions_left = self.voivodeship.all
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
        self.multiplier = self.multiplier()
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
        time_delta = clock.tick(60) / 1000.0

        while self._play:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self._play = self.exit_execute()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._play = self.exit_execute()
                if event.type == pygame.VIDEORESIZE:
                    self._play = self.reset()
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

            self.draw_elements(time_delta)

            self.manager.draw_ui(self.screen)

            pygame.display.flip()

    def multiplier(self):
        level_base = ["Easy", "Medium", "Hard", "Extreme"]
        a = 0

        if self.active_option == self.voivodeship.voivodeship_options[-1]:
            b = 3
            if self.active_level_option == level_base[-1]:
                a = 2
            elif self.active_level_option == level_base[-2]:
                a = 1
            elif self.active_level_option == level_base[-4]:
                a = -1
        else:
            b = 1
            if self.active_level_option == level_base[-1]:
                a = 3
            elif self.active_level_option == level_base[-2]:
                a = 2
            elif self.active_level_option == level_base[-3]:
                a = 1

        return a + b

    def save_score(self, file):
        df = pd.read_excel(file)
        df.sort_values(by=df.columns[-1], ascending=False, inplace=True)

        updater = pd.DataFrame(columns=["Nazwa", "Poziom", "Województwo", "Skuteczność[%]"])
        updater.at[0, 'Nazwa'] = self.nickname
        updater.at[0, 'Poziom'] = self.active_level_option
        updater.at[0, 'Województwo'] = self.active_option
        updater.at[0, 'Skuteczność[%]'] = self.score_percentage

        df = pd.concat([updater, df], ignore_index=True)
        df = df.sort_values(by="Skuteczność[%]", ascending=False).head(50)
        df.to_excel(file, columns=["Nazwa", "Poziom", "Województwo", "Skuteczność[%]"])

    def next_question(self):
        try:
            self.registration, self.county, self.answers = self.voivodeship.ask_question()
        except IndexError as e:
            print(e)
            self.notification()
            self.update_question_info()
            self.update_score_info()
            self.save_score(os.path.join(os.path.dirname(os.path.abspath(regplates.__file__)),"ranking.xlsx"))
            self._play = False

    def update_answer_blocks(self):
        for i, answer_block in enumerate(self.answer_blocks):
            self.answer_blocks[i].update_text(self.answers[i])

    def draw_elements(self, delta):
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
            block.button.update(delta)

        self.exit_button.update(delta)
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
            self.score_percentage = round(100 * self._score / (self.multiplier * (self.voivodeship.all - self.questions_left)))
            text = font.render(f"Twój wynik: {self.score_percentage}%", True, black)
        else:
            text = font.render(f"Twój wynik: {self._score }", True, black)

        self.screen.blit(text, (0.9 * self.screen.get_width() - text.get_width(),
                                0.04 * self.screen.get_height() + 0.5 * text.get_height()))

    def handle_answer_click(self, clicked_block):
        for block in self.answer_blocks:
            if block.button == clicked_block:
                if block.text == self.county:
                    self._score += self.multiplier
                elif self.mode == 0:
                    self._score = 0
        self.questions_left += -1

    @staticmethod
    def reset():
        pygame.display.flip()
        messagebox.showinfo("Restart", "Zmiana rozdzielczości wymaga restartu!")
        return False

    @staticmethod
    def exit_execute():
        if messagebox.askquestion("Potwierdzenie", "Czy na pewno chcesz wyjść?") == "no":
            return True

    @staticmethod
    def notification():
        messagebox.showinfo("Brawo!", "Wszystkie indeksy zostały już wylosowane!")

    @staticmethod
    def config_notification():
        messagebox.showinfo("Zmień konfigurację",
                            'Dla obszaru wszystkich województw rozgrywka zaczyna się od poziomu medium '
                            '\n\nWybierz odpowiedni poziom trudności!')
