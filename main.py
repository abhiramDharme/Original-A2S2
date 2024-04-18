#emphatic response at <50
#STORE NAME AND HIGH SCORE, leaderboard
#changing id without movement
# tracker to save kaunsi kaunsi location visit kari
# add zooming in on map
#check zanskar location
#settings volume bug
#versus mode
# how to play


from classes import *
from geolocate import *
from image_preprocess import *
import random
from enum import Enum
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
import sys
import csv
import threading

location = (28.546758, 77.185148)
thread_active = False

class State(Enum):
    MAIN_MENU = 1
    GAME_HODOPHILE = 2
    PAUSE = 3
    MOTIVATION = 4
    SETTINGS = 5
    MODE_SELECT = 6
    GAME_HODOPHOBE = 7
    TOTAL_SCORE = 8


STATE = State.MAIN_MENU
IMAGE = 0
ROUNDS_PER_GAME = 10

def update_location():
    global location
    global thread_active
    while thread_active:
        location = get_location()

update_thread = threading.Thread(target = update_location)

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
newWidth = SCREEN_WIDTH
newHeight = SCREEN_HEIGHT
ratio = newHeight / SCREEN_HEIGHT

RADIUS_OF_SCORE = 200
DISTINCT_LOCS = 23
TOTAL_SCORE = 0

MAP_RATIO = 1.82

WHITE = (240, 240, 240)
GRAY = (227, 200, 200)
RED = (181, 40, 40)
ORANGE = (255, 85, 28)
CYAN = (25, 41, 11)
BLACK = (0, 0, 0)
DARK_RED = (97, 15, 15)

defaultCursor = pygame.SYSTEM_CURSOR_ARROW
handCursor = pygame.SYSTEM_CURSOR_HAND
crossCursor = pygame.SYSTEM_CURSOR_CROSSHAIR

icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)

locations_pixel = []

with open('images/pixel_coordinates.csv', 'r') as file:
    reader = csv.reader(file)

    # Read all lines into a list
    locations_pixel = list(reader)

locations_gps = []

with open('images/geographical_coordinates.csv', 'r') as file:
    reader = csv.reader(file)

    # Read all lines into a list
    locations_gps = list(reader)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("IITDGuessr")

main_menu_bg = pygame.image.load("home_page.jpg").convert()

pygame.mixer.music.load('bgm.mp3')
pygame.mixer.music.play(-1)

running = True
initialised_main_menu = False
initialised_settings = False
initialised_mode_select = False
initialised_hodophobe = False
initialised_hodophile = False

show_information_box_1 = False
show_information_box_2 = False

menu_page = Page()
settings_page = Page()
mode_select_page = Page()
information_page_1 = Page()
information_page_2 = Page()
hodophobe_page = Page()
hodophile_page = Page()
final_score_page = Page()

cur_loc_list = []

while running:
    if STATE == State.MAIN_MENU:

        if not initialised_main_menu:
            play_button = TextInBox("fonts/Quick Starter.ttf", "PLAY GAME", 20, SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 - 10, 180, 35, RED, WHITE, 5)
            settings_button = TextInBox("fonts/Quick Starter.ttf", "SETTINGS", 20, SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 35, 180, 35, RED, WHITE, 5)
            motivation_button = TextInBox("fonts/Quick Starter.ttf", "MOTIVATION", 20, SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 80, 180, 35, RED, WHITE, 5)
            quit_button = TextInBox("fonts/Quick Starter.ttf", "QUIT GAME", 20, SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 125, 180, 35, RED, WHITE, 5)
            createdby_box = TextInBox("fonts/ARIBL0.ttf", "Created by", 13, 750, 420, 0, 0, BLACK, WHITE, 0, True, BLACK)
            s_and_a_box = TextInBox("fonts/ARIBL0.ttf", "SK and ASD", 13, 750, 440, 0, 0, BLACK, WHITE, 0, True, BLACK)
            iitd_guessr = TextInBox("fonts/Quick Starter.ttf", "IITDGUESSR", 70, SCREEN_WIDTH // 2 - 90, 70, 160, 40, BLACK, WHITE, 5, transparent = True)
            iitd_guessr_outline = TextInBox("fonts/Quick Starter.ttf", "IITDGUESSR", 71, SCREEN_WIDTH // 2 - 91, 70, 160, 40, BLACK, BLACK, 5, transparent = True)
            menu_page.buttonList = [play_button, settings_button, motivation_button, quit_button]
            menu_page.boxList = [createdby_box, s_and_a_box, iitd_guessr_outline, iitd_guessr]

            if ratio != 1:
                menu_page.resizePage(ratio)

            initialised_main_menu = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for button in menu_page.buttonList:
                    if button.rect.collidepoint(mouse_pos):
                        button.box_color = ORANGE
                    else:
                        button.box_color = RED

                if any(button.rect.collidepoint(mouse_pos) for button in menu_page.buttonList):
                    pygame.mouse.set_cursor(handCursor)
                else:
                    pygame.mouse.set_cursor(defaultCursor)


            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if play_button.rect.collidepoint(mouse_pos):
                    STATE = State.MODE_SELECT
                elif motivation_button.rect.collidepoint(mouse_pos):
                    STATE = State.MOTIVATION
                elif settings_button.rect.collidepoint(mouse_pos):
                    STATE = State.SETTINGS
                elif quit_button.rect.collidepoint(mouse_pos):
                    running = False
                    continue

            elif event.type == pygame.VIDEORESIZE:
                newWidth, newHeight = event.size
                if newWidth * SCREEN_HEIGHT / SCREEN_WIDTH > newHeight:
                    newWidth = newHeight * SCREEN_WIDTH / SCREEN_HEIGHT
                else:
                    newHeight = newWidth * SCREEN_HEIGHT / SCREEN_WIDTH
                ratio = newWidth/SCREEN_WIDTH
                screen = pygame.display.set_mode((newWidth, newHeight), pygame.RESIZABLE)

                menu_page.resizePage(ratio)

        screen.blit(pygame.transform.smoothscale(main_menu_bg, (newWidth, newHeight)), (0, 0))
        menu_page.renderBoxes(screen)
        menu_page.renderButtons(screen)


        if STATE != State.MAIN_MENU:
            initialised_main_menu = False


    if STATE == State.SETTINGS:
        if not initialised_settings:
            pygame.mouse.set_cursor(defaultCursor)
            settings_container = TextInBox("fonts/Quick Starter.ttf", "", 1, -30, 0, SCREEN_WIDTH//2 + 30, SCREEN_HEIGHT, GRAY, GRAY, int(30), hover_color=GRAY)
            settings_box = TextInBox("fonts/Quick Starter.ttf", "SETTINGS", int(40), SCREEN_WIDTH//4, int(40), 0, 0, RED, RED, 0, True, RED)
            volume_box = TextInBox("fonts/Quick Starter.ttf", "MUSIC VOLUME", int(18), int(80), int(90), int(70), int(20), RED, RED, int(5), transparent= True, hover_color=RED)
            volume_slider = Slider(screen, int(230), int(95), int(140), int(5), min = 0, max = 100, colour = RED, handleColour = BLACK, handleRadius = int(5), initial = 100)
            iitdguessr_box = TextInBox("fonts/Quick Starter.ttf", "IITDGUESSR", int(40), (SCREEN_WIDTH * 3) // 4 - int(90), int(70), int(160), int(40), BLACK, WHITE, int(5), transparent = True)
            iitdguessr_outline = TextInBox("fonts/Quick Starter.ttf", "IITDGUESSR", int(41), (SCREEN_WIDTH * 3) // 4 - int(91), int(70), int(160), int(40), BLACK, BLACK, int(5), transparent = True)
            back_button = TextInBox("fonts/Quick Starter.ttf", "BACK", 25, 30, 410, 80, 25, BLACK, RED, 0, True)
            settings_page.boxList = [settings_container, settings_box, volume_box, iitdguessr_outline, iitdguessr_box]
            settings_page.buttonList = [back_button]
            if ratio != 1:
                settings_page.resizePage(ratio)
                vol = volume_slider.getValue()
                volume_slider = Slider(screen, int(230*ratio), int(95*ratio), int(140*ratio), int(5*ratio), min = 0, max = 100, colour = RED, handleColour = BLACK, handleRadius = int(5*ratio), initial = vol)
            initialised_settings = True
            continue

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                newWidth, newHeight = event.size
                if newWidth * SCREEN_HEIGHT / SCREEN_WIDTH > newHeight:
                    newWidth = newHeight * SCREEN_WIDTH / SCREEN_HEIGHT
                else:
                    newHeight = newWidth * SCREEN_HEIGHT / SCREEN_WIDTH
                
                ratio = newWidth/SCREEN_WIDTH
                screen = pygame.display.set_mode((newWidth, newHeight), pygame.RESIZABLE)

                settings_page.resizePage(ratio)
                vol = volume_slider.getValue()
                volume_slider = Slider(screen, int(230*ratio), int(95*ratio), int(140*ratio), int(5*ratio), min = 0, max = 100, colour = WHITE, handleColour = BLACK, handleRadius = int(10*ratio), initial = vol)
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for button in settings_page.buttonList:
                    if button.text_rect.collidepoint(mouse_pos):
                        button.font_color = ORANGE
                    else:
                        button.font_color = RED
                settings_page.resizePage(ratio)

                if any(button.text_rect.collidepoint(mouse_pos) for button in settings_page.buttonList):
                    pygame.mouse.set_cursor(handCursor)
                else:
                    pygame.mouse.set_cursor(defaultCursor)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if back_button.text_rect.collidepoint(mouse_pos):
                    STATE = State.MAIN_MENU

            
        screen.blit(pygame.transform.smoothscale(main_menu_bg, (newWidth, newHeight)), (newWidth//4, 0))

        settings_page.renderBoxes(screen)
        settings_page.renderButtons(screen)
        pygame_widgets.update(events)
        volume = volume_slider.getValue()
        pygame.mixer.music.set_volume(float(volume/100))

        if STATE != State.SETTINGS:
            initialised_settings = False


    if STATE == State.MODE_SELECT:

        if not initialised_mode_select:

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

            if ratio != 1:
                mode_select_page.resizePage(ratio)
                information_page_1.resizePage(ratio)
                information_page_2.resizePage(ratio)
            initialised_mode_select = True
            continue

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                newWidth, newHeight = event.size
                if newWidth * SCREEN_HEIGHT / SCREEN_WIDTH > newHeight:
                    newWidth = newHeight * SCREEN_WIDTH / SCREEN_HEIGHT
                else:
                    newHeight = newWidth * SCREEN_HEIGHT / SCREEN_WIDTH
                
                ratio = newWidth/SCREEN_WIDTH
                screen = pygame.display.set_mode((newWidth, newHeight), pygame.RESIZABLE)

                mode_select_page.resizePage(ratio)
                information_page_1.resizePage(ratio)
                information_page_2.resizePage(ratio)

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for button in mode_select_page.buttonList:
                    if button.rect.collidepoint(mouse_pos):
                        button.box_color = ORANGE
                        
                        if button is hodophilic_box:
                            show_information_box_1 = True
                            show_information_box_2 = False
                            break
                        elif button is hodophobic_box:
                            show_information_box_2 = True
                            show_information_box_1 = False
                            break
                    else:
                        button.box_color = RED
                        show_information_box_1 = False
                        show_information_box_2 = False
                
                mode_select_page.resizePage(ratio)

                if any(button.rect.collidepoint(mouse_pos) for button in mode_select_page.buttonList):
                    pygame.mouse.set_cursor(handCursor)
                else:
                    pygame.mouse.set_cursor(defaultCursor)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if hodophilic_box.rect.collidepoint(mouse_pos):
                    STATE = State.GAME_HODOPHILE
                elif hodophobic_box.rect.collidepoint(mouse_pos):
                    STATE = State.GAME_HODOPHOBE
                elif back_box.rect.collidepoint(mouse_pos):
                    STATE = State.MAIN_MENU


        screen.blit(pygame.transform.smoothscale(main_menu_bg, (newWidth, newHeight)), (0, 0))
        mode_select_page.renderBoxes(screen)
        mode_select_page.renderButtons(screen)


        if show_information_box_1:
            information_page_1.renderBoxes(screen)

        if show_information_box_2:
            information_page_2.renderBoxes(screen)

        
        if STATE != State.MODE_SELECT:
            initialised_mode_select = False


    if STATE == State.GAME_HODOPHOBE:

        if not initialised_hodophobe:

            cur_loc_indexes = random.sample(range(23), 5)

            image_loc = "images/" + str(cur_loc_indexes[0]+1) + ".jpg"

            coord_image = locations_pixel[cur_loc_indexes[0]]

            image_container = TextInBox("fonts/Quick Starter.ttf", "", 1, 5, 5, 280, 440, WHITE, WHITE, 10)
            image = Textures(image_loc, 55, 10, 180, 240)
            submit_button = TextInBox("fonts/arial.ttf", "SUBMIT", 15, 50, 410, 190, 25, RED, WHITE, 5)
            camp_map = Textures("campus_map.png", 300, 100, 490, 280)
            camp_map_rect = TextInBox("fonts/Quick Starter.ttf", "", 1, 300, 100, 490, 280, BLACK, WHITE, 0, transparent = True)
            camp_map_container = TextInBox("fonts/Quick Starter.ttf", "", 1, 295, 95, 500, 290, BLACK, WHITE, 5)

            marker_texture = Textures("marker.png", -150, -150, 18, 29)
            blue_marker_texture = Textures("blue_marker.png", -150, -150, 12, 19) #AHAHA

            logo_texture = Textures("logo.png", 65, 260, 150, 138)
            score = 0
            score_box = TextInBox("fonts/ARIBL0.ttf", "SCORE:" + str(score), 25, 465, 32, 150, 35, WHITE, RED, 5)
            select_location_box = TextInBox("fonts/Quick Starter.ttf", "PLEASE PICK A LOCATION", 15, 300, 400, 490, 35, WHITE, RED, 5)

            hodophobe_page.textureList = [camp_map, blue_marker_texture, marker_texture, logo_texture, image]
            hodophobe_page.boxList = [image_container, camp_map_container, score_box, select_location_box]
            hodophobe_page.buttonList = [submit_button, camp_map_rect]

            if ratio != 1:
                hodophobe_page.resizePage(ratio)
            initialised_hodophobe = True
            continue

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                newWidth, newHeight = event.size
                if newWidth * SCREEN_HEIGHT / SCREEN_WIDTH > newHeight:
                    newWidth = newHeight * SCREEN_WIDTH / SCREEN_HEIGHT
                else:
                    newHeight = newWidth * SCREEN_HEIGHT / SCREEN_WIDTH
                
                ratio = newWidth/SCREEN_WIDTH
                screen = pygame.display.set_mode((newWidth, newHeight), pygame.RESIZABLE)

                hodophobe_page.resizePage(ratio)

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos

                if submit_button.rect.collidepoint(mouse_pos):
                    submit_button.box_color = ORANGE
                else:
                    submit_button.box_color = RED
                
                hodophobe_page.resizePage(ratio)

                if submit_button.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(handCursor)
                elif camp_map_rect.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(crossCursor)
                else:
                    pygame.mouse.set_cursor(defaultCursor)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if(IMAGE%2 == 0):
                    if submit_button.rect.collidepoint(mouse_pos):
                        if hodophobe_page.pos_marked == True:
                            
                            IMAGE = IMAGE + 1

                            marker_texture.X, marker_texture.Y =  int(coord_image[0])-9, int(coord_image[1])-27
                            marker_texture.update_dimensions(ratio)
                            dis = round(pixel_distance(marker_texture.X+9, marker_texture.Y+27, blue_marker_texture.X + 6, blue_marker_texture.Y + 17))
                            additional_score = max(RADIUS_OF_SCORE - dis, 0)
                            score = score + additional_score
                            score_box.text_to_print = "Score:" + str(score)
                            score_box.update_dimensions(ratio)
                            select_location_box.text_to_print = "YOU SCORED " + str(additional_score) + " POINTS, BEING " + str(dis) + " M AWAY FROM TARGET"
                            select_location_box.initial_font_size = 12
                            select_location_box.update_dimensions(ratio)
                            submit_button.text_to_print = "NEXT"
                    
                    elif camp_map_rect.rect.collidepoint(mouse_pos):

                        hodophobe_page.pos_marked = True
                        x, y = mouse_pos
                        blue_marker_texture.x = x - 6 * ratio
                        blue_marker_texture.y = y - 17 * ratio
                        blue_marker_texture.X, blue_marker_texture.Y = blue_marker_texture.x / ratio, blue_marker_texture.y / ratio

                else:
                    if submit_button.rect.collidepoint(mouse_pos):
                        IMAGE = IMAGE + 1

                        if IMAGE == ROUNDS_PER_GAME:
                            STATE = State.TOTAL_SCORE
                            IMAGE = 0
                            TOTAL_SCORE = score
                            continue

                        else:
                            hodophobe_page.pos_marked = False
                            blue_marker_texture.X = -150
                            blue_marker_texture.Y = -150
                            marker_texture.X = -150
                            marker_texture.Y = -150
                            select_location_box.text_to_print = "PLEASE SELECT A LOCATION"
                            submit_button.text_to_print = "SUBMIT"
                            image_loc = "images/" + str(cur_loc_indexes[IMAGE//2]+1) + ".jpg"
                            coord_image = locations_pixel[cur_loc_indexes[IMAGE//2]]
                            image = Textures(image_loc, 55, 10, 180, 240)
                            image.update_dimensions(ratio)
                            hodophobe_page.textureList[4] = image

        screen.blit(pygame.transform.smoothscale(main_menu_bg, (newWidth, newHeight)), (0, 0))
        hodophobe_page.renderBoxes(screen)
        hodophobe_page.renderTextures(screen)
        hodophobe_page.renderButtons(screen)
        
        if STATE != State.GAME_HODOPHOBE:
            initialised_hodophobe = False


    if STATE == State.GAME_HODOPHILE:

        if not initialised_hodophile:

            thread_active = True
            update_thread.start()

            cur_loc_indexes = random.sample(range(23), 5)

            image_loc = "images/" + str(cur_loc_indexes[0]+1) + ".jpg"

            coord_image = locations_pixel[cur_loc_indexes[0]]

            image_container = TextInBox("fonts/Quick Starter.ttf", "", 1, 5, 5, 280, 440, WHITE, WHITE, 10)
            image = Textures(image_loc, 55, 10, 180, 240)
            submit_button = TextInBox("fonts/arial.ttf", "FIX LOCATION", 15, 50, 410, 190, 25, RED, WHITE, 5)
            camp_map = Textures("campus_map.png", 300, 100, 490, 280)
            camp_map_container = TextInBox("fonts/Quick Starter.ttf", "", 1, 295, 95, 500, 290, BLACK, WHITE, 5)

            marker_texture = Textures("marker.png", -150, -150, 18, 29)
            blue_marker_texture = Textures("blue_marker.png", -150, -150, 12, 19)

            logo_texture = Textures("logo.png", 65, 260, 150, 138)
            score = 0
            score_box = TextInBox("fonts/ARIBL0.ttf", "SCORE:" + str(score), 25, 465, 32, 150, 35, WHITE, RED, 5)
            select_location_box = TextInBox("fonts/Quick Starter.ttf", "PLEASE GO TO THE LOCATION", 15, 300, 400, 490, 35, WHITE, RED, 5)

            hodophile_page.textureList = [camp_map, blue_marker_texture, marker_texture, logo_texture, image]
            hodophile_page.boxList = [image_container, camp_map_container, score_box, select_location_box]
            hodophile_page.buttonList = [submit_button]

            if ratio != 1:
                hodophile_page.resizePage(ratio)
            initialised_hodophile = True
            continue

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                thread_active = False
                update_thread.join()
                running = False
            elif event.type == pygame.VIDEORESIZE:
                newWidth, newHeight = event.size
                if newWidth * SCREEN_HEIGHT / SCREEN_WIDTH > newHeight:
                    newWidth = newHeight * SCREEN_WIDTH / SCREEN_HEIGHT
                else:
                    newHeight = newWidth * SCREEN_HEIGHT / SCREEN_WIDTH
                
                ratio = newWidth/SCREEN_WIDTH
                screen = pygame.display.set_mode((newWidth, newHeight), pygame.RESIZABLE)

                hodophile_page.resizePage(ratio)

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos

                if submit_button.rect.collidepoint(mouse_pos):
                    submit_button.box_color = ORANGE
                else:
                    submit_button.box_color = RED
                
                hodophile_page.resizePage(ratio)

                if submit_button.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(handCursor)
                else:
                    pygame.mouse.set_cursor(defaultCursor)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if(IMAGE%2 == 0):
                    if submit_button.rect.collidepoint(mouse_pos):
                        dis = round(haversine_distance(location[0], location[1], float(locations_gps[cur_loc_indexes[IMAGE//2]][0]), float(locations_gps[cur_loc_indexes[IMAGE//2]][1])))
                        
                        IMAGE = IMAGE + 1

                        marker_texture.X, marker_texture.Y =  int(coord_image[0])-9, int(coord_image[1])-27
                        marker_texture.update_dimensions(ratio)
                        additional_score = max(RADIUS_OF_SCORE - dis, 0)
                        score = score + additional_score
                        score_box.text_to_print = "Score:" + str(score)
                        score_box.update_dimensions(ratio)
                        select_location_box.text_to_print = "YOU SCORED " + str(additional_score) + " POINTS, BEING " + str(dis) + " M AWAY FROM TARGET"
                        select_location_box.initial_font_size = 12
                        select_location_box.update_dimensions(ratio)
                        submit_button.text_to_print = "NEXT"
                    

                else:
                    if submit_button.rect.collidepoint(mouse_pos):
                        IMAGE = IMAGE + 1

                        if IMAGE == ROUNDS_PER_GAME:
                            STATE = State.TOTAL_SCORE
                            IMAGE = 0
                            TOTAL_SCORE = score
                            continue

                        else:
                            hodophile_page.pos_marked = False
                            blue_marker_texture.X = -150
                            blue_marker_texture.Y = -150
                            marker_texture.X = -150
                            marker_texture.Y = -150
                            select_location_box.text_to_print = "PLEASE GO TO THE LOCATION"
                            submit_button.text_to_print = "FIX LOCATION"
                            image_loc = "images/" + str(cur_loc_indexes[IMAGE//2]+1) + ".jpg"
                            coord_image = locations_pixel[cur_loc_indexes[IMAGE//2]]
                            image = Textures(image_loc, 55, 10, 180, 240)
                            image.update_dimensions(ratio)
                            hodophile_page.textureList[4] = image

        pixel_coord = coord_to_pixel(location[0], location[1])
        blue_marker_texture.X, blue_marker_texture.Y = pixel_coord[0]-6, pixel_coord[1]-17

        screen.blit(pygame.transform.smoothscale(main_menu_bg, (newWidth, newHeight)), (0, 0))
        hodophile_page.renderBoxes(screen)
        hodophile_page.renderTextures(screen)
        hodophile_page.renderButtons(screen)
        
        if STATE != State.GAME_HODOPHILE:
            initialised_hodophile = False
            thread_active = False
            update_thread.join()


    if STATE == State.TOTAL_SCORE:

        if not initialised_mode_select:

            score_final_box = TextInBox("fonts/Quick Starter.ttf", "YOUR FINAL SCORE : " + str(TOTAL_SCORE), 40, x = 40, y = 40, w = 720, h = 300, box_color=WHITE, font_color=RED, roundedness=20, transparent=False)

            main_menu_button_box = TextInBox("fonts/Quick Starter.ttf", "MAIN MENU", 22, x = 40, y = 370, w = 200, h = 40, box_color=RED, font_color=WHITE, roundedness=10, transparent=False)
            main_menu_button_bg = TextInBox("fonts/Quick Starter.ttf", "", 22, x = 40, y = 375, w = 200, h = 40, box_color=DARK_RED, font_color=WHITE, roundedness=10, transparent=False)

            play_again_box = TextInBox("fonts/Quick Starter.ttf", "PLAY AGAIN", 22, x = 560, y = 370, w = 200, h = 40, box_color=RED, font_color=WHITE, roundedness=10, transparent=False)
            play_again_bg = TextInBox("fonts/Quick Starter.ttf", "", 22, x = 560, y = 375, w = 200, h = 40, box_color=DARK_RED, font_color=WHITE, roundedness=10, transparent=False)

            final_score_page.buttonList = [main_menu_button_box, play_again_box]
            final_score_page.boxList = [main_menu_button_bg, play_again_bg, score_final_box]

            if ratio != 1:
                final_score_page.resizePage(ratio)
            initialised_mode_select = True
            continue

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                newWidth, newHeight = event.size
                if newWidth * SCREEN_HEIGHT / SCREEN_WIDTH > newHeight:
                    newWidth = newHeight * SCREEN_WIDTH / SCREEN_HEIGHT
                else:
                    newHeight = newWidth * SCREEN_HEIGHT / SCREEN_WIDTH
                
                ratio = newWidth/SCREEN_WIDTH
                screen = pygame.display.set_mode((newWidth, newHeight), pygame.RESIZABLE)

                final_score_page.resizePage(ratio)

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for button in final_score_page.buttonList:
                    if button.rect.collidepoint(mouse_pos):
                        button.box_color = ORANGE
                        
                    else:
                        button.box_color = RED
                
                final_score_page.resizePage(ratio)

                if any(button.rect.collidepoint(mouse_pos) for button in final_score_page.buttonList):
                    pygame.mouse.set_cursor(handCursor)
                else:
                    pygame.mouse.set_cursor(defaultCursor)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if main_menu_button_box.rect.collidepoint(mouse_pos):
                    STATE = State.MAIN_MENU
                elif play_again_box.rect.collidepoint(mouse_pos):
                    STATE = State.GAME_HODOPHOBE


        screen.blit(pygame.transform.smoothscale(main_menu_bg, (newWidth, newHeight)), (0, 0))
        final_score_page.renderBoxes(screen)
        final_score_page.renderButtons(screen)
        
        if STATE != State.TOTAL_SCORE:
            initialised_mode_select = False

    pygame.display.flip()

pygame.quit()
sys.exit()