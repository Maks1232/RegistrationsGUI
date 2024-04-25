import pygame
import pygame_gui


class AnswerRect:
    """
    A class used to store and display text content of provided information and enable mouse button click spot

    Attributes
    ----------
    rect : object
       a pygame.Rect object instance to set the screen part as a reserved area for answer block creation
    text : str
       an attribute that determines answer block displaying content
    button : object
       a pygame_gui.elements.UIButton object instance used to display ready product which one the AnswerRect class
       description defines

    Methods
    -------
    random_plate()
       a method used to make text content inside the answer block update
    """

    def __init__(self, x, y, width, height, text, manager):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.button = pygame_gui.elements.UIButton(
            relative_rect=self.rect, text=text, manager=manager
        )

    def update_text(self, new_text):
        self.text = new_text
        self.button.set_text(self.text)
