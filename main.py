#buttons translucent
#rounded corners
#heading white with black boundary and shadow
#settings box gradient
#pop up pannel electronic blue
#border buttons

#(300, 100) top left
#(790, 100) top right
#(300, 380) bottom left
#(790, 380) bottom right
#jwala circle (28.549072, 77.184548) (381, 157)
#sac circle (28.546758, 77.185148) (419, 218)
#himadri circle (28.544863, 77.194476)  (638, 171)
#entrance (28.545861, 77.196540) (673, 120)
# adch gate (28.539450, 77.198897) (789, 282)

from classes import *
from geolocate import *
import random
import math
from enum import Enum
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
import sys
import numpy as np

multiply = np.array([[-10284.8089, 21505.0252], [-29304.1486, -10938.0468]])
mul_inv = np.linalg.inv(multiply)
add = np.array([[-1365852.2896, 1681011.2609]])


class State(Enum):
    MAIN_MENU = 1
    GAME_HODOPHILE = 2
    PAUSE = 3
    MOTIVATION = 4
    SETTINGS = 5
    MODE_SELECT = 6
    GAME_HODOPHOBE = 7
    TOTAL_SCORE = 8

class Image(Enum):
    I0 = 0
    I1 = 1
    I2 = 2
    I3 = 3
    I4 = 4
    I5 = 5



STATE = State.MAIN_MENU
IMAGE = Image.I0

def nextState(state):
    if state == Image.I0:
        state = Image.I1
    elif state == Image.I1:
        state = Image.I2
    elif state == Image.I2:
        state = Image.I3
    elif state == Image.I3:
        state = Image.I4
    elif state == Image.I4:
        state = Image.I5
    elif state == Image.I5:
        state = Image.I0
        STATE = State.TOTAL_SCORE

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
newWidth = SCREEN_WIDTH
newHeight = SCREEN_HEIGHT
ratio = newHeight / SCREEN_HEIGHT

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

locations = [
    ("images/1.jpg", (28.548312, 77.185623)),
    ("images/2.jpg", (604, 511)),
]

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

            #cur_loc_list = random.sample(locations, 5)

            image_loc, coordinates = locations[0][0], locations[0][1]

            image_container = TextInBox("fonts/Quick Starter.ttf", "", 1, 5, 5, 280, 440, WHITE, WHITE, 10)
            image = Textures(image_loc, 55, 10, 180, 240)
            submit_button = TextInBox("fonts/arial.ttf", "SUBMIT", 15, 50, 410, 190, 25, RED, WHITE, 5)
            camp_map = Textures("campus_map.png", 300, 100, 490, 280)
            camp_map_rect = TextInBox("fonts/Quick Starter.ttf", "", 1, 300, 100, 490, 280, BLACK, WHITE, 0, transparent = True)
            camp_map_container = TextInBox("fonts/Quick Starter.ttf", "", 1, 295, 95, 500, 290, BLACK, WHITE, 5)
            marker_texture = Textures("marker.png", -150, -150, 24, 38)
            blue_marker_texture = Textures("blue_marker.png", -150, -150, 24, 38)
            logo_texture = Textures("logo.png", 65, 260, 150, 138)
            hodophobe_page.textureList = [camp_map, marker_texture, blue_marker_texture, logo_texture, image]
            hodophobe_page.boxList = [image_container, camp_map_container]
            hodophobe_page.buttonList = [submit_button, camp_map_rect]
            score = 0

            error_message_box = TextInBox("fonts/Quick Starter.ttf", "Please select a location", 10, newWidth//2 - 350, newHeight//2 - 30, 700, 60, GRAY, RED, 10)

            if ratio != 1:
                hodophobe_page.resizePage(ratio)
                error_message_box.update_dimensions(ratio)
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
                error_message_box.update_dimensions(ratio)

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
                if submit_button.rect.collidepoint(mouse_pos):
                    if hodophobe_page.pos_marked == True:
                        IMAGE = Image.I1
                        hodophobe_page.pos_marked = False
                    else:
                        hodophobe_page.error = True
                elif camp_map_rect.rect.collidepoint(mouse_pos):
                    hodophobe_page.pos_marked = True
                    x, y = mouse_pos
                    marker_texture.X, marker_texture.Y = int(x//ratio)-12, int(y//ratio)-38
                    marker_texture.update_dimensions(ratio)


        screen.blit(pygame.transform.smoothscale(main_menu_bg, (newWidth, newHeight)), (0, 0))
        hodophobe_page.renderBoxes(screen)
        hodophobe_page.renderTextures(screen)
        hodophobe_page.renderButtons(screen)

        if (IMAGE == Image.I1 or IMAGE == Image.I3 or IMAGE == Image.I5):

            if hodophobe_page.pos_marked == False:
                coord_image = np.array(coordinates)
                pixel_coord_image = multiply @ coord_image + add

                pixel_coord_map = [marker_texture.X + 12, marker_texture.Y + 38]
                blue_marker_texture.X, blue_marker_texture.Y =  pixel_coord_image[0][0]-12, pixel_coord_image[0][1]-38
                blue_marker_texture.update_dimensions(ratio)
                dis = round(pixel_distance(blue_marker_texture.X, blue_marker_texture.Y, marker_texture.X, marker_texture.Y))
                print("pixeldistance:", dis)
                score = score + 200 - dis
                hodophobe_page.pos_marked = True
            
            blue_marker_texture.render(screen)
            

        if hodophobe_page.error == True:
            error_message_box.render(screen)
            pygame.time.wait(2000)
        
        if STATE != State.GAME_HODOPHOBE:
            initialised_hodophobe = False

    pygame.display.flip()

pygame.quit()
sys.exit()