import pygame
import pygame_gui


class AnswerRect:
    def __init__(self, x, y, width, height, text, manager):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.button = pygame_gui.elements.UIButton(
            relative_rect=self.rect,
            text=text,
            manager=manager
        )

    def update_text(self, new_text):
        self.text = new_text
        self.button.set_text(self.text)
