from classes import *
from constants import *
from colours import *

initialised_mode_select = False

show_information_box_1 = False
show_information_box_2 = False

mode_select_page = Page()
information_page_1 = Page()
information_page_2 = Page()

hodophilic_box = TextInBox("fonts/Quick Starter.ttf", "HODOPHILIC", 45, x = SCREEN_WIDTH//2-360, y = 260, w = 385, h = 70, box_color=RED, font_color=WHITE, roundedness=20, transparent=False)
hodophilic_bg = TextInBox("fonts/Quick Starter.ttf", "", 45, x = SCREEN_WIDTH//2-360, y = 265, w = 385, h = 70, box_color=DARK_RED, font_color=WHITE, roundedness=20, transparent=False)
hodophobic_box = TextInBox("fonts/Quick Starter.ttf", "HODOPHOBIC", 45, x = SCREEN_WIDTH//2-50, y = 350, w = 410, h = 70, box_color=RED, font_color=WHITE, roundedness=20, transparent=False)
hodophobic_bg = TextInBox("fonts/Quick Starter.ttf", "", 45, x = SCREEN_WIDTH//2-50, y = 355, w = 410, h = 70, box_color=DARK_RED, font_color=WHITE, roundedness=20, transparent=False)
choose_your_box = TextInBox("fonts/Quick Starter.ttf", "CHOOSE YOUR", 50, x = 340, y = 5, w = 410, h = 70, box_color=DARK_RED, font_color=WHITE, roundedness=0, transparent=True)
game_mode_box = TextInBox("fonts/Quick Starter.ttf", "GAME MODE", 50, x = 372, y = 50, w = 410, h = 70, box_color=DARK_RED, font_color=WHITE, roundedness=0, transparent=True)
choose_your_bg = TextInBox("fonts/Quick Starter.ttf", "CHOOSE YOUR", 51, x = 339, y = 5, w = 410, h = 70, box_color=DARK_RED, font_color=BLACK, roundedness=0, transparent=True)
game_mode_bg =  TextInBox("fonts/Quick Starter.ttf", "GAME MODE", 51, x = 371, y = 50, w = 410, h = 70, box_color=DARK_RED, font_color=BLACK, roundedness=0, transparent=True)

back_box = TextInBox("fonts/Quick Starter.ttf", "BACK", 22, x = 40, y = 20, w = 90, h = 40, box_color=RED, font_color=WHITE, roundedness=10, transparent=False)
back_bg = TextInBox("fonts/Quick Starter.ttf", "", 22, x = 40, y = 25, w = 90, h = 40, box_color=DARK_RED, font_color=WHITE, roundedness=10, transparent=False)

mode_select_page.buttonList = [hodophilic_box, hodophobic_box, back_box]
mode_select_page.boxList = [hodophilic_bg, hodophobic_bg, choose_your_bg, game_mode_bg, choose_your_box, game_mode_box, back_bg]

information_box_1 = TextInBox("fonts/Quick Starter.ttf", "", 50, x = 10, y = 10, w = 280, h = 140, box_color=GRAY, font_color=CYAN, roundedness=10, transparent=False)
philic_line_1 = TextInBox("fonts/Quick Starter.ttf", "TRAVEL AROUND CAMPUS", 15, x = 10, y = 50, w = 280, h = 0, box_color=RED, font_color=RED, roundedness=20, transparent=True)
philic_line_2 = TextInBox("fonts/Quick Starter.ttf", "AND DISCOVER NEW", 15, x = 10, y = 80, w = 280, h = 0, box_color=RED, font_color=RED, roundedness=20, transparent=True)
philic_line_3 = TextInBox("fonts/Quick Starter.ttf", "SPOTS AND LOCATIONS!", 15, x = 10, y = 110, w = 280, h = 0, box_color=RED, font_color=RED, roundedness=20, transparent=True)
information_page_1.boxList = [information_box_1, philic_line_1, philic_line_2, philic_line_3]

information_box_2 = TextInBox("fonts/Quick Starter.ttf", "", 50, x = 10, y = 10, w = 280, h = 140, box_color=GRAY, font_color=CYAN, roundedness=10, transparent=False)
phobic_line_1 = TextInBox("fonts/Quick Starter.ttf", "FIND OUT SECRET", 15, x = 10, y = 50, w = 280, h = 0, box_color=RED, font_color=RED, roundedness=20, transparent=True)
phobic_line_2 = TextInBox("fonts/Quick Starter.ttf", "CORNERS WITHOUT", 15, x = 10, y = 80, w = 280, h = 0, box_color=RED, font_color=RED, roundedness=20, transparent=True)
phobic_line_3 = TextInBox("fonts/Quick Starter.ttf", "MOVING FROM YOUR BED!", 15, x = 10, y = 110, w = 280, h = 0, box_color=RED, font_color=RED, roundedness=20, transparent=True)
information_page_2.boxList = [information_box_2, phobic_line_1, phobic_line_2, phobic_line_3]