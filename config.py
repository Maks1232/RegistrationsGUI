from Game import *

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Window creation
WIN = pygame.display.set_mode((1400, 800), pygame.RESIZABLE)
pygame.display.set_caption("Registration Plates Quiz")

# Colors
white = (255, 255, 255)
aqua = (0, 255, 255)
red = (255, 0, 0)
grey = (150, 150, 150)
dark_grey = (100, 100, 100)
green = (60, 179, 113)
active_green = (94, 180, 0)
black = (0, 0, 0)
dark_blue = (66, 0, 249)
bright_blue = (175, 238, 238)

# Variables
full_list = False
full_level_list = False
active_option = "Wybierz województwo"
active_level_option = "Wybierz poziom"
tribes = {0: 'Powtarzanie', 1: 'Bez powtórzeń'}
mode = 0
score = 0
nickname = "Unknown"
nick_executed = False
clock = pygame.time.Clock()
UI_REFRESH_RATE = clock.tick(60) / 10000
run = True

# Loading images
app_logo = pygame.image.load(os.path.join('Images', 'title_v1.png'))
registration_template = pygame.image.load(os.path.join('Images', 'registration_template.png'))

# Drop down options
voivodeship_options = import_list(file_name='voivodeship_options')
level_options = ["Easy", "Medium", "Hard", "Extreme"]
