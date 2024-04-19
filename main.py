# changing submit button without movement
# find factor using best fit line
# add line between marked locations
# add save state for hodophobic mode


from classes import *
from geolocate import *
from image_preprocess import *

from colours import *
from constants import *


from main_menu import *
from settings import *
from leaderboard import *
from mode_select import *
from crawl import *


import random
from enum import Enum
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import sys
import csv
import threading
import pandas as pd

location = (28.546758, 77.185148)
thread_active = False

def update_location():
    global location
    global thread_active
    while thread_active:
        location = get_location()

class State(Enum):
    MAIN_MENU = 1
    GAME_HODOPHILE = 2
    GAME_HODOPHOBE_VERSUS = 3
    MOTIVATION_CRAWL = 4
    SETTINGS = 5
    MODE_SELECT = 6
    GAME_HODOPHOBE = 7
    TOTAL_SCORE = 8
    HODO_SELECT = 9
    TOTAL_SCORE_VERSUS = 10
    LEADERBOARD = 11


prevSTATE = State.MAIN_MENU
STATE = State.MAIN_MENU
IMAGE = 0


def change_no_of_rounds(val):
    global ROUNDS_PER_GAME
    if val != None:
        ROUNDS_PER_GAME = 2 * val


pygame.mixer.init()


newWidth = int(SCREEN_WIDTH * 1.8375)
newHeight = int(SCREEN_HEIGHT * 1.8375)
ratio = newHeight / SCREEN_HEIGHT

TOTAL_SCORE = 0
TOTAL_SCORE_1 = 0
TOTAL_SCORE_2 = 0

defaultCursor = pygame.SYSTEM_CURSOR_ARROW
handCursor = pygame.SYSTEM_CURSOR_HAND
crossCursor = pygame.SYSTEM_CURSOR_CROSSHAIR

icon = pygame.image.load("textures/logo.png")
pygame.display.set_icon(icon)

locations_pixel = []

with open('images/pixel_coordinates.csv', 'r') as file:
    reader = csv.reader(file)
    locations_pixel = list(reader)

locations_gps = []

with open('images/geographical_coordinates.csv', 'r') as file:
    reader = csv.reader(file)
    locations_gps = list(reader)

screen = pygame.display.set_mode((newWidth, newHeight), pygame.RESIZABLE)
pygame.display.set_caption("IITDGuessr")

main_menu_bg = pygame.image.load("home_page.jpg").convert()

pygame.mixer.music.load('bgm.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.50)

def video_resize(event, page):
    global newWidth
    global newHeight
    global ratio
    global screen

    newWidth, newHeight = event.size
    if newWidth * SCREEN_HEIGHT / SCREEN_WIDTH > newHeight:
        newWidth = newHeight * SCREEN_WIDTH / SCREEN_HEIGHT
    else:
        newHeight = newWidth * SCREEN_HEIGHT / SCREEN_WIDTH
    ratio = newWidth/SCREEN_WIDTH
    screen = pygame.display.set_mode((newWidth, newHeight), pygame.RESIZABLE)


    page.resizePage(ratio)

running = True

initialised_hodophobe = False
initialised_hodophobe_versus = False
initialised_hodophile = False
initialised_hodoselect = False



hodophobe_page = Page()
hodophobe_versus_page = Page()
hodophile_page = Page()
final_score_page = Page()
hodo_select_page = Page()

cur_loc_list = []

while running:
    if STATE == State.MAIN_MENU:

        if not initialised_main_menu:

            menu_page.resizePage(ratio)

            for button in menu_page.buttonList:
                button.box_color = RED

            initialised_main_menu = True
            continue
        
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
                elif settings_button.rect.collidepoint(mouse_pos):
                    STATE = State.SETTINGS
                elif leaderboard_button.rect.collidepoint(mouse_pos):
                    STATE = State.LEADERBOARD
                elif motivation_button.rect.collidepoint(mouse_pos):
                    STATE = State.MOTIVATION_CRAWL
                
                elif quit_button.rect.collidepoint(mouse_pos):
                    running = False
                    continue

            elif event.type == pygame.VIDEORESIZE:
                video_resize(event, menu_page)

        screen.blit(pygame.transform.smoothscale(main_menu_bg, (newWidth, newHeight)), (0, 0))
        menu_page.renderBoxes(screen)
        menu_page.renderButtons(screen)


        if STATE != State.MAIN_MENU:
            initialised_main_menu = False


    if STATE == State.LEADERBOARD:
        if not initialised_leaderboard:

            df = pd.read_csv("leaderboard.csv")

            leaderboard_page.buttonList = [back_button]
            leaderboard_page.boxList = [leaderboard_container, rank_box, name_box, score_word_box, note_box]

            for i in range(0,5):
                r_box = TextInBox("fonts/Quick Starter.ttf", str(df.iloc[i,0]).upper() + '.', 25, 100, 150 + 60*i, 0, 0, RED, RED,15, transparent = True)
                n_box = TextInBox("fonts/Quick Starter.ttf", str(df.iloc[i,1]).upper(), 25, 400, 150 + 60 * i, 0, 0, RED, RED,15, transparent = True)
                s_box = TextInBox("fonts/Quick Starter.ttf", str(df.iloc[i, 2]).upper(), 25, 680, 150 + 60 * i, 0, 0, RED, RED,15, transparent = True)
                leaderboard_page.boxList = leaderboard_page.boxList + [r_box, n_box, s_box]

            leaderboard_page.resizePage(ratio)

            initialised_leaderboard = True
            continue
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for button in leaderboard_page.buttonList:
                    if button.rect.collidepoint(mouse_pos):
                        button.box_color = ORANGE
                    else:
                        button.box_color = RED
                
                back_button.update_dimensions(ratio)

                if any(button.rect.collidepoint(mouse_pos) for button in leaderboard_page.buttonList):
                    pygame.mouse.set_cursor(handCursor)
                else:
                    pygame.mouse.set_cursor(defaultCursor)


            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if back_button.rect.collidepoint(mouse_pos):
                    STATE = State.MAIN_MENU

            elif event.type == pygame.VIDEORESIZE:
                video_resize(event, leaderboard_page)

        screen.blit(pygame.transform.smoothscale(main_menu_bg, (newWidth, newHeight)), (0, 0))
        leaderboard_page.renderBoxes(screen)
        leaderboard_page.renderButtons(screen)


        if STATE != State.LEADERBOARD:
            initialised_leaderboard = False


    if STATE == State.SETTINGS:
        if not initialised_settings:


            name_input = None
            
            vol = pygame.mixer.music.get_volume()
            volume_slider = Slider(screen, int(230*ratio), int(95*ratio), int(140*ratio), int(5*ratio), min = 0, max = 100, colour = RED, handleColour = BLACK, handleRadius = int(5*ratio), initial = vol*100)

            for button in settings_page.buttonList:
                button.font_color = RED

            rounds = ROUNDS_PER_GAME//2
            rounds_slider = Slider(screen, int(230*ratio), int(145*ratio), int(120*ratio), int(5*ratio), min = 1, max = 10, colour = RED, handleColour = BLACK, handleRadius = int(5*ratio), initial = rounds)
            rounds_box = TextInBox("fonts/ARIBL0.ttf", str(rounds_slider.getValue()), int(15), int(360), int(137), int(20), int(20), RED, WHITE, int(5))
            settings_page.boxList.append(rounds_box)
            settings_page.resizePage(ratio)
            initialised_settings = True
            continue

        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                video_resize(event, settings_page)

                vol = volume_slider.getValue()
                volume_slider = Slider(screen, int(230*ratio), int(95*ratio), int(140*ratio), int(5*ratio), min = 0, max = 100, colour = RED, handleColour = BLACK, handleRadius = int(5*ratio), initial = vol)

                rounds = rounds_slider.getValue()
                rounds_slider = Slider(screen, int(230*ratio), int(145*ratio), int(120*ratio), int(5*ratio), min = 1, max = 10, colour = RED, handleColour = BLACK, handleRadius = int(5*ratio), initial = rounds)
                

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for button in settings_page.buttonList:
                    if button.text_rect.collidepoint(mouse_pos):
                        button.font_color = ORANGE
                    else:
                        button.font_color = RED
                

                if any(button.text_rect.collidepoint(mouse_pos) for button in settings_page.buttonList):
                    pygame.mouse.set_cursor(handCursor)
                else:
                    pygame.mouse.set_cursor(defaultCursor)
                settings_page.resizePage(ratio)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if any(button.text_rect.collidepoint(mouse_pos) for button in settings_page.buttonList):
                    STATE = State.MAIN_MENU
            
        screen.blit(pygame.transform.smoothscale(main_menu_bg, (newWidth, newHeight)), (newWidth//4, 0))

        settings_page.renderBoxes(screen)
        settings_page.renderButtons(screen)
        pygame_widgets.update(events)
        pygame.mixer.music.set_volume(float(volume_slider.getValue()/100))

        rounds_box.text_to_print = str(rounds_slider.getValue())

        if STATE != State.SETTINGS:
            initialised_settings = False
            change_no_of_rounds(rounds_slider.getValue())


    if STATE == State.MODE_SELECT:

        if not initialised_mode_select:

            for button in mode_select_page.buttonList:
                button.box_color = RED

            show_information_box_1 = False
            show_information_box_2 = False

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
                video_resize(event, mode_select_page)
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
                    STATE = State.HODO_SELECT
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


    if STATE == State.HODO_SELECT:
        if not initialised_hodoselect:
            solo_box = TextInBox("fonts/Quick Starter.ttf", "SOLO MODE", int(45), x = int(SCREEN_WIDTH//2-360), y = int(160), w = int(385), h = int(90), box_color=RED, font_color=WHITE, roundedness=int(20), transparent=False)
            solo_bg = TextInBox("fonts/Quick Starter.ttf", "", int(45), x = int(SCREEN_WIDTH//2-360), y = int(165), w = int(385), h = int(90), box_color=DARK_RED, font_color=WHITE, roundedness=int(20), transparent=False)
            versus_box = TextInBox("fonts/Quick Starter.ttf", "VERSUS MODE", int(45), x = int(SCREEN_WIDTH//2-120), y = int(320), w = int(470), h = int(90), box_color=RED, font_color=WHITE, roundedness=int(20), transparent=False)
            versus_bg = TextInBox("fonts/Quick Starter.ttf", "", int(45), x = int(SCREEN_WIDTH//2-120), y = int(325), w = int(470), h = int(90), box_color=DARK_RED, font_color=WHITE, roundedness=int(20), transparent=False)

            back_box_hodo = TextInBox("fonts/Quick Starter.ttf", "BACK", 22, x = 40, y = 20, w = 90, h = 40, box_color=RED, font_color=WHITE, roundedness=10, transparent=False)
            back_bg_hodo = TextInBox("fonts/Quick Starter.ttf", "", 22, x = 40, y = 25, w = 90, h = 40, box_color=DARK_RED, font_color=WHITE, roundedness=10, transparent=False)

            hodo_select_page.boxList = [solo_bg, versus_bg, back_bg_hodo]
            hodo_select_page.buttonList = [solo_box, versus_box, back_box_hodo]

            if ratio != 1:
                hodo_select_page.resizePage(ratio)
            initialised_hodoselect = True
            continue
            
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                video_resize(event, hodo_select_page)

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for button in hodo_select_page.buttonList:
                    if button.rect.collidepoint(mouse_pos):
                        button.box_color = ORANGE
                        
                    else:
                        button.box_color = RED
                
                hodo_select_page.resizePage(ratio)

                if any(button.rect.collidepoint(mouse_pos) for button in hodo_select_page.buttonList):
                    pygame.mouse.set_cursor(handCursor)
                else:
                    pygame.mouse.set_cursor(defaultCursor)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if solo_box.rect.collidepoint(mouse_pos):
                    STATE = State.GAME_HODOPHOBE
                elif versus_box.rect.collidepoint(mouse_pos):
                    STATE = State.GAME_HODOPHOBE_VERSUS
                elif back_box_hodo.rect.collidepoint(mouse_pos):
                    STATE = State.MODE_SELECT


        screen.blit(pygame.transform.smoothscale(main_menu_bg, (newWidth, newHeight)), (0, 0))
        hodo_select_page.renderBoxes(screen)
        hodo_select_page.renderButtons(screen)

        
        if STATE != State.HODO_SELECT:
            initialised_hodoselect = False
        

    if STATE == State.GAME_HODOPHOBE:

        if not initialised_hodophobe:

            cur_loc_indexes = random.sample(range(DISTINCT_LOCS), ROUNDS_PER_GAME//2)

            image_loc = "images/" + str(cur_loc_indexes[0]+1) + ".jpg"

            coord_image = locations_pixel[cur_loc_indexes[0]]

            image_container = TextInBox("fonts/Quick Starter.ttf", "", 1, 5, 5, 280, 440, WHITE, WHITE, 10)
            image = Textures(image_loc, 55, 10, 180, 240)
            submit_button = TextInBox("fonts/arial.ttf", "SUBMIT", 15, 50, 410, 190, 25, RED, WHITE, 5)
            camp_map = Textures("textures/campus_map.png", 300, 100, 490, 280)
            camp_map_rect = TextInBox("fonts/Quick Starter.ttf", "", 1, 300, 100, 490, 280, BLACK, WHITE, 0, transparent = True)
            camp_map_container = TextInBox("fonts/Quick Starter.ttf", "", 1, 295, 95, 500, 290, BLACK, WHITE, 5)

            marker_texture = Textures("textures/marker.png", -150, -150, 18, 29)
            blue_marker_texture = Textures("textures/blue_marker.png", -150, -150, 12, 19)

            quit_to_box = TextInBox("fonts/ARIBL0.ttf", "Back To", 13, 660, 40, 100, 0, WHITE, RED, 5, True, BLACK)
            main_menu_box = TextInBox("fonts/ARIBL0.ttf", "Main Menu", 13, 660, 55, 100, 0, WHITE, RED, 5, True, BLACK)
            main_menu_button = TextInBox("fonts/ARIBL0.ttf", "", 13, 660, 32, 100, 33, WHITE, RED, 5)

            logo_texture = Textures("textures/logo.png", 65, 260, 150, 138)
            score = 0
            score_box = TextInBox("fonts/ARIBL0.ttf", "SCORE:" + str(score), 25, 325, 32, 150, 35, WHITE, RED, 5)
            select_location_box = TextInBox("fonts/Quick Starter.ttf", "PLEASE PICK A LOCATION", 15, 300, 400, 490, 35, WHITE, RED, 5)

            hodophobe_page.textureList = [camp_map, blue_marker_texture, marker_texture, logo_texture, image]
            hodophobe_page.boxList = [image_container, camp_map_container, score_box, select_location_box, main_menu_button, quit_to_box, main_menu_box]
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
                elif main_menu_button.rect.collidepoint(mouse_pos):
                    main_menu_button.box_color = GRAY
                else:
                    submit_button.box_color = RED
                    main_menu_button.box_color = WHITE
                
                hodophobe_page.resizePage(ratio)

                if submit_button.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(handCursor)
                elif main_menu_button.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(handCursor)
                elif camp_map_rect.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(crossCursor)
                else:
                    pygame.mouse.set_cursor(defaultCursor)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if main_menu_button.rect.collidepoint(mouse_pos):
                    STATE = State.MAIN_MENU
                
                elif(IMAGE%2 == 0):
                    
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

                            if dis<=25:
                                wow = pygame.mixer.Sound("wow.mp3")
                                wow.play()
                            elif dis >= 200:
                                fail = pygame.mixer.Sound("fail.mp3")
                                fail.play()

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
            prevSTATE = State.GAME_HODOPHOBE
            initialised_hodophobe = False
            IMAGE = 0


    if STATE == State.GAME_HODOPHOBE_VERSUS:
        if not initialised_hodophobe_versus:

            cur_loc_indexes = random.sample(range(DISTINCT_LOCS), ROUNDS_PER_GAME//2)

            image_loc = "images/" + str(cur_loc_indexes[0]+1) + ".jpg"

            coord_image = locations_pixel[cur_loc_indexes[0]]

            image_container = TextInBox("fonts/Quick Starter.ttf", "", 1, 5, 5, 280, 440, WHITE, WHITE, 10)
            image = Textures(image_loc, 55, 10, 180, 240)
            submit_button = TextInBox("fonts/arial.ttf", "SUBMIT", 15, 50, 410, 190, 25, RED, WHITE, 5)
            camp_map = Textures("textures/campus_map.png", 300, 100, 490, 280)
            camp_map_rect = TextInBox("fonts/Quick Starter.ttf", "", 1, 300, 100, 490, 280, BLACK, WHITE, 0, transparent = True)
            camp_map_container = TextInBox("fonts/Quick Starter.ttf", "", 1, 295, 95, 500, 290, BLACK, WHITE, 5)

            marker_texture = Textures("textures/marker.png", -150, -150, 18, 29)
            blue_marker_texture = Textures("textures/blue_marker.png", -150, -150, 12, 19)
            green_marker_texture = Textures("textures/green_marker.png", -150, -150, 12, 19)

            quit_to_box = TextInBox("fonts/ARIBL0.ttf", "Back To", 13, 660, 40, 100, 0, WHITE, RED, 5, True, BLACK)
            main_menu_box = TextInBox("fonts/ARIBL0.ttf", "Main Menu", 13, 660, 55, 100, 0, WHITE, RED, 5, True, BLACK)
            main_menu_button = TextInBox("fonts/ARIBL0.ttf", "", 13, 660, 32, 100, 33, WHITE, RED, 5)

            logo_texture = Textures("textures/logo.png", 65, 260, 150, 138)
            score1 = 0
            score2 = 0
            x1 = 0
            y1 = 0
            x2 = 0
            y2 = 0
            score_box = TextInBox("fonts/ARIBL0.ttf", "Player 1: " + str(score1) +"      Player 2: "+ str(score2), 20, 300, 32, 340, 35, WHITE, RED, 5)
            select_location_box = TextInBox("fonts/Quick Starter.ttf", "PLAYER 1'S TURN", 15, 300, 400, 490, 35, WHITE, RED, 5)

            hodophobe_versus_page.textureList = [camp_map, blue_marker_texture, green_marker_texture, marker_texture, logo_texture, image]
            hodophobe_versus_page.boxList = [image_container, camp_map_container, score_box, select_location_box, main_menu_button, quit_to_box, main_menu_box]
            hodophobe_versus_page.buttonList = [submit_button, camp_map_rect]

            if ratio != 1:
                hodophobe_versus_page.resizePage(ratio)
            initialised_hodophobe_versus = True
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

                hodophobe_versus_page.resizePage(ratio)

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos

                if submit_button.rect.collidepoint(mouse_pos):
                    submit_button.box_color = ORANGE
                elif main_menu_button.rect.collidepoint(mouse_pos):
                    main_menu_button.box_color = GRAY
                else:
                    submit_button.box_color = RED
                    main_menu_button.box_color = WHITE
                
                hodophobe_versus_page.resizePage(ratio)

                if submit_button.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(handCursor)
                elif main_menu_button.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(handCursor)
                elif camp_map_rect.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(crossCursor)
                else:
                    pygame.mouse.set_cursor(defaultCursor)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if main_menu_button.rect.collidepoint(mouse_pos):
                    STATE = State.MAIN_MENU
                
                elif(IMAGE%3 == 0):    #player 1 marks location
                    
                    if submit_button.rect.collidepoint(mouse_pos):
                        if hodophobe_versus_page.pos_marked == True:                           
                            IMAGE = IMAGE + 1

                            x1, y1 = blue_marker_texture.X, blue_marker_texture.Y
                            blue_marker_texture.X, blue_marker_texture.Y = -150, -150
                            blue_marker_texture.update_dimensions(ratio)

                            select_location_box.text_to_print = "PLAYER 2'S TURN"
                            select_location_box.initial_font_size = 15
                            select_location_box.update_dimensions(ratio)
                            hodophobe_versus_page.pos_marked = False
                    
                    elif camp_map_rect.rect.collidepoint(mouse_pos):
                        hodophobe_versus_page.pos_marked = True
                        x, y = mouse_pos
                        blue_marker_texture.x = x - 6 * ratio
                        blue_marker_texture.y = y - 17 * ratio
                        blue_marker_texture.X, blue_marker_texture.Y = blue_marker_texture.x / ratio, blue_marker_texture.y / ratio

                elif(IMAGE%3 == 1):       # player 2 marks location
                    if submit_button.rect.collidepoint(mouse_pos):
                        if hodophobe_versus_page.pos_marked == True:                           
                            IMAGE = IMAGE + 1

                            x2, y2 = green_marker_texture.X, green_marker_texture.Y

                            blue_marker_texture.X, blue_marker_texture.Y = x1, y1
                            blue_marker_texture.update_dimensions(ratio)

                            submit_button.text_to_print = "NEXT ROUND"
                            submit_button.initial_font_size = 15
                            submit_button.update_dimensions(ratio)
                            hodophobe_versus_page.pos_marked = False

                            marker_texture.X, marker_texture.Y =  int(coord_image[0])-9, int(coord_image[1])-27
                            marker_texture.update_dimensions(ratio)

                            dis1 = round(pixel_distance(marker_texture.X+9, marker_texture.Y+27, x1 + 6, y1 + 17))
                            dis2 = round(pixel_distance(marker_texture.X+9, marker_texture.Y+27, x2 + 6, y2 + 17))

                            additional_score1 = max(RADIUS_OF_SCORE - dis1, 0)
                            score1 = score1 + additional_score1

                            additional_score2 = max(RADIUS_OF_SCORE - dis2, 0)
                            score2 = score2 + additional_score2

                            score_box.text_to_print = "Player 1: " + str(score1) +"      Player 2: "+ str(score2)
                            score_box.update_dimensions(ratio)

                            select_location_box.text_to_print = "P1 SCORED " + str(additional_score1) + " POINTS, AND P2 SCORED " + str(additional_score2) + " POINTS"
                            select_location_box.initial_font_size = 12
                            select_location_box.update_dimensions(ratio)

                    
                    elif camp_map_rect.rect.collidepoint(mouse_pos):
                        hodophobe_versus_page.pos_marked = True
                        x, y = mouse_pos
                        green_marker_texture.x = x - 6 * ratio
                        green_marker_texture.y = y - 17 * ratio
                        green_marker_texture.X, green_marker_texture.Y = green_marker_texture.x / ratio, green_marker_texture.y / ratio

                elif(IMAGE%3 == 2):       #show both scores
                    if submit_button.rect.collidepoint(mouse_pos):
                        IMAGE = IMAGE + 1

                        if IMAGE == (ROUNDS_PER_GAME*3)//2:
                            STATE = State.TOTAL_SCORE_VERSUS
                            IMAGE = 0
                            TOTAL_SCORE_1, TOTAL_SCORE_2 = score1, score2
                            continue

                        else:
                            hodophobe_versus_page.pos_marked = False
                            blue_marker_texture.X = -150
                            blue_marker_texture.Y = -150
                            green_marker_texture.X = -150
                            green_marker_texture.Y = -150
                            marker_texture.X = -150
                            marker_texture.Y = -150
                            select_location_box.text_to_print = "PLEASE SELECT A LOCATION"
                            submit_button.text_to_print = "SUBMIT"
                            image_loc = "images/" + str(cur_loc_indexes[IMAGE//3]+1) + ".jpg"
                            coord_image = locations_pixel[cur_loc_indexes[IMAGE//3]]
                            image = Textures(image_loc, 55, 10, 180, 240)
                            image.update_dimensions(ratio)
                            hodophobe_versus_page.textureList[5] = image

        screen.blit(pygame.transform.smoothscale(main_menu_bg, (newWidth, newHeight)), (0, 0))
        hodophobe_versus_page.renderBoxes(screen)
        hodophobe_versus_page.renderTextures(screen)
        hodophobe_versus_page.renderButtons(screen)
        
        if STATE != State.GAME_HODOPHOBE_VERSUS:
            prevSTATE = State.GAME_HODOPHOBE_VERSUS
            initialised_hodophobe_versus = False
            IMAGE = 0


    if STATE == State.GAME_HODOPHILE:

        if not initialised_hodophile:

            thread_active = True
            update_thread = threading.Thread(target = update_location)
            update_thread.start()

            cur_loc_indexes = random.sample(range(DISTINCT_LOCS), ROUNDS_PER_GAME//2)

            image_loc = "images/" + str(cur_loc_indexes[0]+1) + ".jpg"

            coord_image = locations_pixel[cur_loc_indexes[0]]

            image_container = TextInBox("fonts/Quick Starter.ttf", "", 1, 5, 5, 280, 440, WHITE, WHITE, 10)
            image = Textures(image_loc, 55, 10, 180, 240)
            submit_button = TextInBox("fonts/arial.ttf", "FIX MY LOCATION", 15, 50, 410, 190, 25, RED, WHITE, 5)
            camp_map = Textures("textures/campus_map.png", 300, 100, 490, 280)
            camp_map_container = TextInBox("fonts/Quick Starter.ttf", "", 1, 295, 95, 500, 290, BLACK, WHITE, 5)

            marker_texture = Textures("textures/marker.png", -150, -150, 18, 29)
            blue_marker_texture = Textures("textures/blue_marker.png", -150, -150, 12, 19)

            quit_to_box = TextInBox("fonts/ARIBL0.ttf", "Back To", 13, 660, 40, 100, 0, WHITE, RED, 5, True, BLACK)
            main_menu_box = TextInBox("fonts/ARIBL0.ttf", "Main Menu", 13, 660, 55, 100, 0, WHITE, RED, 5, True, BLACK)
            main_menu_button = TextInBox("fonts/ARIBL0.ttf", "", 13, 660, 32, 100, 33, WHITE, RED, 5)

            logo_texture = Textures("textures/logo.png", 65, 260, 150, 138)
            score = 0
            score_box = TextInBox("fonts/ARIBL0.ttf", "SCORE:" + str(score), 25, 325, 32, 150, 35, WHITE, RED, 5)
            select_location_box = TextInBox("fonts/Quick Starter.ttf", "PLEASE GO TO THE LOCATION", 15, 300, 400, 490, 35, WHITE, RED, 5)

            hodophile_page.textureList = [camp_map, blue_marker_texture, marker_texture, logo_texture, image]
            hodophile_page.boxList = [image_container, camp_map_container, score_box, select_location_box, main_menu_button, quit_to_box, main_menu_box]
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
                elif main_menu_button.rect.collidepoint(mouse_pos):
                    main_menu_button.box_color = GRAY
                else:
                    submit_button.box_color = RED
                    main_menu_button.box_color = WHITE
                
                hodophile_page.resizePage(ratio)

                if submit_button.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(handCursor)
                elif main_menu_button.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(handCursor)
                else:
                    pygame.mouse.set_cursor(defaultCursor)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if main_menu_button.rect.collidepoint(mouse_pos):
                    STATE = State.MAIN_MENU
                if(IMAGE%2 == 0):
                    if submit_button.rect.collidepoint(mouse_pos):
                        dis = round(haversine_distance(location[0], location[1], float(locations_gps[cur_loc_indexes[IMAGE//2]][0]), float(locations_gps[cur_loc_indexes[IMAGE//2]][1])))
                        
                        IMAGE = IMAGE + 1

                        marker_texture.X, marker_texture.Y =  int(coord_image[0])-9, int(coord_image[1])-27
                        marker_texture.update_dimensions(ratio)
                        additional_score = max(RADIUS_OF_SCORE - dis, 0)

                        if dis <=25:
                            success = pygame.mixer.Sound("success.mp3")
                            success.play()

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
            prevSTATE = State.GAME_HODOPHILE
            IMAGE = 0
            initialised_hodophile = False
            thread_active = False
            update_thread.join()


    if STATE == State.TOTAL_SCORE:

        if not initialised_mode_select:

            score_final_container = TextInBox("fonts/Quick Starter.ttf", "", 40, x = 40, y = 40, w = 720, h = 300, box_color=WHITE, font_color=RED, roundedness=20, transparent=False)
            score_final_box = TextInBox("fonts/Quick Starter.ttf", "YOUR FINAL SCORE : " + str(TOTAL_SCORE), 40, x = 40, y = 10, w = 720, h = 300, box_color=WHITE, font_color=RED, roundedness=20, transparent=True)
            good_job_box = TextInBox("fonts/Quick Starter.ttf", "GOOD JOB!", 40, x = 40, y = 50, w = 720, h = 300, box_color=WHITE, font_color=RED, roundedness=20, transparent=True)

            main_menu_button_box = TextInBox("fonts/Quick Starter.ttf", "MAIN MENU", 22, x = 40, y = 370, w = 200, h = 40, box_color=RED, font_color=WHITE, roundedness=10, transparent=False)
            main_menu_button_bg = TextInBox("fonts/Quick Starter.ttf", "", 22, x = 40, y = 375, w = 200, h = 40, box_color=DARK_RED, font_color=WHITE, roundedness=10, transparent=False)

            play_again_box = TextInBox("fonts/Quick Starter.ttf", "PLAY AGAIN", 22, x = 560, y = 370, w = 200, h = 40, box_color=RED, font_color=WHITE, roundedness=10, transparent=False)
            play_again_bg = TextInBox("fonts/Quick Starter.ttf", "", 22, x = 560, y = 375, w = 200, h = 40, box_color=DARK_RED, font_color=WHITE, roundedness=10, transparent=False)

            final_score_page.buttonList = [main_menu_button_box, play_again_box]
            final_score_page.boxList = [main_menu_button_bg, play_again_bg, score_final_container, score_final_box, good_job_box]


            volume_slider = None

            rounds_slider = None

            goat_visible = False
            if ROUNDS_PER_GAME == 10 and prevSTATE == State.GAME_HODOPHOBE:
                goat_visible, rank = update_leaderboard(TOTAL_SCORE)
            

            if goat_visible:
                name_input = TextBox(screen, 300, 400, 800, 80, fontSize=50,
                    borderColour=(255, 0, 0), textColour=(0, 200, 0),
                    radius=10, borderThickness=5, placeholderText = "NAME")
                good_job_box.text_to_print = "YOU'RE A GOAT! ENTER YOUR NAME:"
                good_job_box.initial_font_size = 25
                good_job_box.update_dimensions(ratio)

            if ratio != 1:

                final_score_page.resizePage(ratio)

                if goat_visible:
                    name_input = TextBox(screen, int(250*ratio), int(250*ratio), int(300*ratio), int(45*ratio), fontSize=int(25*ratio),
                    borderColour=(255, 0, 0), textColour=RED,
                    radius=10, borderThickness=5, font = pygame.font.Font("fonts/Quick Starter.ttf", int(25*ratio)), placeholderText = "NAME")

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
                if goat_visible:
                    name_input = TextBox(screen, int(100*ratio), int(250*ratio), int(300*ratio), int(45*ratio), fontSize=int(25*ratio),
                    borderColour=(255, 0, 0), textColour=RED,
                    radius=10, borderThickness=5, font = pygame.font.Font("fonts/Quick Starter.ttf", int(25*ratio)))

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
                    STATE = prevSTATE


        screen.blit(pygame.transform.smoothscale(main_menu_bg, (newWidth, newHeight)), (0, 0))
        final_score_page.renderBoxes(screen)
        final_score_page.renderButtons(screen)
        pygame_widgets.update(events)

        
        
        if STATE != State.TOTAL_SCORE:
            initialised_mode_select = False
            if goat_visible:
                write_leaderboard(rank, name_input.getText(), TOTAL_SCORE)
            goat_visible = False


    if STATE == State.TOTAL_SCORE_VERSUS:

        if not initialised_mode_select:

            score_final_box = TextInBox("fonts/Quick Starter.ttf", "PLAYER 1 : " + str(TOTAL_SCORE_1) + " & PLAYER 2 : " + str(TOTAL_SCORE_2), 20, x = 40, y = 40, w = 720, h = 300, box_color=WHITE, font_color=RED, roundedness=20, transparent=False)

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
                video_resize(event, final_score_page)

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
                    STATE = prevSTATE


        screen.blit(pygame.transform.smoothscale(main_menu_bg, (newWidth, newHeight)), (0, 0))
        final_score_page.renderBoxes(screen)
        final_score_page.renderButtons(screen)
        
        if STATE != State.TOTAL_SCORE_VERSUS:
            initialised_mode_select = False


    if STATE == State.MOTIVATION_CRAWL:
        if not initialised_motivation:
            back_button_motivation = TextInBox("fonts/Quick Starter.ttf", "BACK", 25, 30, 410, 80, 25, BLACK, RED, 0, True)
            motivation_page = Page()
            motivation_page.buttonList = [back_button_motivation]
            motivation_page.boxList = []
            if ratio != 1:
                motivation_page.resizePage(ratio)
            initialised_motivation = True
            continue
    
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                video_resize(event, motivation_page)

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for button in motivation_page.buttonList:
                    if button.text_rect.collidepoint(mouse_pos):
                        button.font_color = ORANGE
                    else:
                        button.font_color = RED
                motivation_page.resizePage(ratio)

                if any(button.text_rect.collidepoint(mouse_pos) for button in motivation_page.buttonList):
                    pygame.mouse.set_cursor(handCursor)
                else:
                    pygame.mouse.set_cursor(defaultCursor)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if motivation_button.rect.collidepoint(mouse_pos):
                    # crawl_y_pos = SCREEN_HEIGHT
                    crawl_active = True
                    STATE = State.MOTIVATION_CRAWL
                elif back_button_motivation.text_rect.collidepoint(mouse_pos) and STATE == State.MOTIVATION_CRAWL:
                    crawl_y_pos = SCREEN_HEIGHT
                    crawl_active = False
                    STATE = State.MAIN_MENU

        screen.fill(BLACK)
        lines = crawl_text.upper().split("\n")
        if not start_crawl(screen, lines):
            STATE = State.MAIN_MENU
            crawl_active = False

        motivation_page.renderBoxes(screen)
        motivation_page.renderButtons(screen)

        if STATE != State.MOTIVATION_CRAWL:
            initialised_motivation = False

        screen.blit(back_button_motivation.text_surface, back_button_motivation.text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()