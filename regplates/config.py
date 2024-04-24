from regplates.Game import *
from regplates.Voivodeship import import_list
import pygame_gui
import pygame

"""
Configuration file with pygame initialization, color definitions, image imports and variable set

Variables
----------
WIN : object
    a pygame object instance generating game window with defined size and modifiers 
white, aqua, red, grey, dark_grey, green, active_green, black, dark_blue, bright_blue : tuple
    a color definitions expressed in rgb format
clock : object
    a pygame.time object instance for time monitoring
run : bool
    a variable for main program loop control
full_list : bool
    a variable for voivodeship selection dropdown list control
nick_executed : bool
    a variable for checking whether the nickname was already set
full_level_list : bool
    a variable for level selection dropdown list control  
nickname : str
    a string variable to set user nickname
active_option : str
    a string variable to set voivodeship choice
active_level_option : str
    a string variable to set difficulty level choice
tribes : dictionary
    a collection to enable tribe choosing 
mode : int
    a helper variable to enable tribe choosing control
app_logo : object
    an application logo image
registration_template : object
    a registration template image
voivodeship_options
    a list with available voivodeship names
level_options
    a list with available difficulty level names
"""

# PyGame initialization
pygame.init()
pygame.font.init()
try:
    pygame.mixer.init()
except pygame.error as e:
    print(str(e))
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

# Loading images
app_logo = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(regplates.__file__)),'Images', 'title_v1.png'))
registration_template = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(regplates.__file__)),'Images', 'registration_template.png'))

# Drop down options
voivodeship_options = import_list(file_name=os.path.join(os.path.dirname(os.path.abspath(regplates.__file__)),'voivodeship_options'))
level_options = ["Easy", "Medium", "Hard", "Extreme"]
