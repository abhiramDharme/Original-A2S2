from classes import *
from colours import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

initialised_main_menu = False

menu_page = Page()

play_button = TextInBox("fonts/Quick Starter.ttf", "PLAY GAME", 20, SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 - 10, 180, 35, RED, WHITE, 5)
settings_button = TextInBox("fonts/Quick Starter.ttf", "SETTINGS", 20, SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 35, 180, 35, RED, WHITE, 5)
leaderboard_button = TextInBox("fonts/Quick Starter.ttf", "THE GOATS", 20, SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 80, 180, 35, RED, WHITE, 5)
motivation_button = TextInBox("fonts/Quick Starter.ttf", "MOTIVATION", 20, SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 125, 180, 35, RED, WHITE, 5)
quit_button = TextInBox("fonts/Quick Starter.ttf", "QUIT GAME", 20, SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 170, 180, 35, RED, WHITE, 5)
createdby_box = TextInBox("fonts/ARIBL0.ttf", "Created by", 13, 750, 420, 0, 0, BLACK, WHITE, 0, True, BLACK)
s_and_a_box = TextInBox("fonts/ARIBL0.ttf", "SK and ASD", 13, 750, 440, 0, 0, BLACK, WHITE, 0, True, BLACK)
iitd_guessr = TextInBox("fonts/Quick Starter.ttf", "IITDGUESSR", 70, SCREEN_WIDTH // 2 - 90, 70, 160, 40, BLACK, WHITE, 5, transparent = True)
iitd_guessr_outline = TextInBox("fonts/Quick Starter.ttf", "IITDGUESSR", 71, SCREEN_WIDTH // 2 - 91, 70, 160, 40, BLACK, BLACK, 5, transparent = True)
menu_page.buttonList = [play_button, settings_button, leaderboard_button, motivation_button, quit_button]
menu_page.boxList = [createdby_box, s_and_a_box, iitd_guessr_outline, iitd_guessr]