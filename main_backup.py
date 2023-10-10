import pygame
import os
import pickle


pygame.font.init()
pygame.mixer.init()

# Window creation
WIDTH, HEIGHT = (1080, 1000)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Registration Plates Quiz")

# Kolory
active_color = (0, 255, 255)
background_color = (255, 255, 255)
button_color = (150, 150, 150)
active_button_color = (100, 100, 100)
text_color = (255, 255, 255)

# Variables
play = False
full_list = False
full_level_list = False
active_option = "Choose voivodeship"
active_level_option = "Choose level"

# Font
font = pygame.font.Font(None, 24)

# Loading images
registration = pygame.image.load(os.path.join('Images', 'title_v1.png'))


# Export list to the file
def export_list(voivodeship_options, file_name):
    with open(file_name, 'wb') as file:
        pickle.dump(voivodeship_options, file)


# Import list from the file
def import_list(file_name):
    with open(file_name, 'rb') as file:
        imported_list = pickle.load(file)
    return imported_list


# Pozycja pola rozwijanego
field_for_list_place = pygame.Rect(100, 200, 200, 40)
field_for_level_list_place = pygame.Rect(700, 200, 200, 40)

# Opcje pola rozwijanego
voivodeship_options = import_list(file_name='voivodeship_options')
level_options = ["Easy", "Hard"]


def draw_window(color):
    WIN.fill(color)
    WIN.blit(registration, (100, 50))


def write_text(text, location):
    text_surface = font.render(text, True, text_color)
    text_location = text_surface.get_rect(center=location)
    WIN.blit(text_surface, text_location)


def draw_list(position, options, active_list, active_choice):
    pygame.draw.rect(WIN, button_color, position)
    pygame.draw.rect(WIN, text_color, position, 2)
    write_text(active_choice,
               (position[0] + position.width // 2, position[1] + position.height // 2))
    if active_list:

        for i, option in enumerate(options):
            y = position[1] + (i + 1) * position.height
            pygame.draw.rect(WIN, button_color, (position[0], y, position.width, position.height))
            pygame.draw.rect(WIN, text_color, (position[0], y, position.width, position.height), 2)
            write_text(option, (position[0] + position.width // 2, y + position.height // 2))


clock = pygame.time.Clock()
run = True

while run:

    clock.tick(60)
    draw_window(background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if field_for_list_place.collidepoint(event.pos):
                full_list = not full_list
                full_level_list = False
            elif field_for_level_list_place.collidepoint(event.pos):
                full_level_list = not full_level_list
                full_list = False
            elif full_list:
                for i, option in enumerate(voivodeship_options):
                    y = field_for_list_place.y + (i + 1) * field_for_list_place.height

                    square_option = pygame.Rect(field_for_list_place.x, y, field_for_list_place.width,
                                    field_for_list_place.height)
                    if square_option.collidepoint(event.pos):
                        active_option = option
                        full_list = False
            elif full_level_list:
                for i, option in enumerate(level_options):
                    y = field_for_level_list_place.y + (i + 1) * field_for_level_list_place.height

                    square_option = pygame.Rect(field_for_level_list_place.x, y, field_for_level_list_place.width,
                                    field_for_level_list_place.height)
                    if square_option.collidepoint(event.pos):
                        active_level_option = option
                        full_level_list = False

    draw_list(field_for_list_place, voivodeship_options, active_list=full_list, active_choice=active_option)
    draw_list(field_for_level_list_place, level_options, active_list=full_level_list, active_choice=active_level_option)

    pygame.display.flip()

print("Voivodeship: ", active_option)
print("Level: ", active_level_option)