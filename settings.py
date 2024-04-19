from classes import *
from colours import *
from constants import *

initialised_settings = False

settings_page = Page()

settings_container = TextInBox("fonts/Quick Starter.ttf", "", 1, -30, 0, SCREEN_WIDTH//2 + 30, SCREEN_HEIGHT, GRAY, GRAY, int(30), hover_color=GRAY)
settings_box = TextInBox("fonts/Quick Starter.ttf", "SETTINGS", int(40), SCREEN_WIDTH//4, int(40), 0, 0, RED, RED, 0, True, RED)
volume_box = TextInBox("fonts/Quick Starter.ttf", "MUSIC VOLUME", int(18), int(80), int(90), int(70), int(20), RED, RED, int(5), transparent= True, hover_color=RED)
no_of_rounds_box = TextInBox("fonts/Quick Starter.ttf", "NO OF ROUNDS", int(18), int(80), int(140), int(70), int(20), RED, RED, int(5), transparent= True, hover_color=RED)

iitdguessr_box = TextInBox("fonts/Quick Starter.ttf", "IITDGUESSR", int(40), (SCREEN_WIDTH * 3) // 4 - int(90), int(70), int(160), int(40), BLACK, WHITE, int(5), transparent = True)
iitdguessr_outline = TextInBox("fonts/Quick Starter.ttf", "IITDGUESSR", int(41), (SCREEN_WIDTH * 3) // 4 - int(91), int(70), int(160), int(40), BLACK, BLACK, int(5), transparent = True)
back_button = TextInBox("fonts/Quick Starter.ttf", "BACK", 25, 30, 410, 80, 25, BLACK, RED, 0, True)
settings_page.boxList = [settings_container, settings_box, volume_box, no_of_rounds_box, iitdguessr_outline, iitdguessr_box]
settings_page.buttonList = [back_button]