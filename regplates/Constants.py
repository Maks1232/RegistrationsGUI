from enum import Enum


class Color(Enum):
    WHITE = (255, 255, 255)
    AQUA = (0, 255, 255)
    RED = (255, 0, 0)
    GREY = (150, 150, 150)
    DARK_GREY = (100, 100, 100)
    GREEN = (60, 179, 113)
    ACTIVE_GREEN = (94, 180, 0)
    BLACK = (0, 0, 0)
    DARK_BLUE = (66, 0, 249)
    BRIGHT_BLUE = (175, 238, 238)


class Level(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    EXTREME = "Extreme"


VOIVODESHIP_OPTIONS_LIST = [
    "Podlaskie",
    "Kujawsko-Pomorskie",
    "Dolnośląskie",
    "Łódzkie",
    "Lubuskie",
    "Pomorskie",
    "Małopolskie",
    "Lubelskie",
    "Warmińsko-Mazurskie",
    "Opolskie",
    "Wielkopolskie",
    "Podkarpackie",
    "Śląskie",
    "Świętokrzyskie",
    "Mazowieckie",
    "Zachodniopomorskie",
    "Wszystkie",
]

RESOURCES_DIR_PATH = "Resources"

IMAGES_DIR_PATH = f"{RESOURCES_DIR_PATH}/Images"
APP_LOGO_IMAGE_PATH = f"{IMAGES_DIR_PATH}/title_v1.png"
REG_TEMPLATE_IMAGE_PATH = f"{IMAGES_DIR_PATH}/registration_template.png"

DICTS_JSON_PATH = f"{RESOURCES_DIR_PATH}/dicts.json"

EXTREME_MATRIX_CSV_PATH = f"{RESOURCES_DIR_PATH}/extreme_matrix.csv"
LEVENSHTEIN_MATRIX_CSV_PATH = f"{RESOURCES_DIR_PATH}/levenshtein_matrix.csv"

RANKING_XLSX_PATH = f"{RESOURCES_DIR_PATH}/ranking.xlsx"
