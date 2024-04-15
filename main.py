#buttons translucent
#rounded corners
#heading white with black boundary and shadow
#settings box gradient
#pop up pannel electronic blue
#border buttons

import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import sys
import random
import math
from enum import Enum

class State(Enum):
    MAIN_MENU = 1
    GAME_HODOPHILE = 2
    PAUSE = 3
    MOTIVATION = 4
    SETTINGS = 5
    MODE_SELECT = 6
    GAME_HODOPHOBE = 7

STATE = State.MAIN_MENU

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
newWidth = SCREEN_WIDTH
newHeight = SCREEN_HEIGHT
ratio = newHeight / SCREEN_HEIGHT

WHITE = (240, 240, 240)
GRAY = (135, 130, 124)
RED = (156, 50, 50)
ORANGE = (255, 85, 28)
CYAN = (25, 41, 11)
BLACK = (0, 0, 0)
DARK_RED = (97, 15, 15)

defaultCursor = pygame.SYSTEM_CURSOR_ARROW
handCursor = pygame.SYSTEM_CURSOR_HAND

icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

locations = [
    ("Images/1.jpg", (600, 494)),
    ("Images/2.jpg", (604, 511)),
]



class TextInBox:
    def __init__(self, font_location, text_to_print, initial_font_size, x, y, w, h, box_color, font_color, roundedness, transparent=False, hover_color = (0,0,0)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.initial_x = x
        self.initial_y = y
        self.initial_w = w
        self.initial_h = h
        self.font_location = font_location
        self.initial_font_size = initial_font_size
        self.current_font_size = initial_font_size
        self.text_to_print = text_to_print
        self.box_color = box_color
        self.inital_box_color = box_color
        self.font_color = font_color
        self.initial_roundedness = roundedness
        self.current_roundedness = roundedness
        self.transparent = transparent
        self.hover_color = hover_color
        self.font = pygame.font.Font(self.font_location, self.current_font_size)
        self.text_surface = self.font.render(self.text_to_print, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def update_dimensions(self, ratio):
        self.x = int(self.initial_x * ratio)
        self.y = int(self.initial_y * ratio) 
        self.w = int(self.initial_w * ratio)
        self.h = int(self.initial_h * ratio)
        self.current_font_size = int(self.initial_font_size * ratio)
        self.current_roundedness = int(self.initial_roundedness * ratio)

        self.font = pygame.font.Font(self.font_location, self.current_font_size)
        self.text_surface = self.font.render(self.text_to_print, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def render(self, screen):
        if not self.transparent:
            pygame.draw.rect(screen, self.box_color, (self.x, self.y, self.w, self.h), border_radius=self.current_roundedness)
        screen.blit(self.text_surface, self.text_rect)

class Page:
    def __init__(self):
        self.buttonList = []
        self.boxList = []
        self.background = None

    def resizePage(self, ratio):
        for box in self.boxList:
            box.update_dimensions(ratio)
        for button in self.buttonList:
            button.update_dimensions(ratio)

    def renderBoxes(self, screen):
        for box in self.boxList:
            box.render(screen)
    def renderButtons(self,screen):
        for button in self.buttonList:
            button.render(screen)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("IITDGuessr")

main_menu_bg = pygame.image.load("home_page.jpg")
texture_main_menu_bg = main_menu_bg.convert()

pygame.mixer.music.load('bgm.mp3')
pygame.mixer.music.play(-1)

running = True
initialised_main_menu = False
initialised_settings = False
initialised_mode_select = False

show_information_box_1 = False
show_information_box_2 = False

menu_page = Page()
settings_page = Page()
mode_select_page = Page()
information_page_1 = Page()
information_page_2 = Page()

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
            iitd_guessr_outline = TextInBox("fonts/Quick Starter.ttf", "IITDGUESSR", 70, SCREEN_WIDTH // 2 - 90, 70, 160, 40, BLACK, WHITE, 5, transparent = True)
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


            #FIX THIS!!!!!
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

        screen.blit(pygame.transform.scale(main_menu_bg, (newWidth, newHeight)), (0, 0 ))
        menu_page.renderBoxes(screen)
        menu_page.renderButtons(screen)


        if STATE != State.MAIN_MENU:
            initialised_main_menu = False


    if STATE == State.SETTINGS:
        if not initialised_settings:
            pygame.mouse.set_cursor(defaultCursor)
            settings_container = TextInBox("fonts/Quick Starter.ttf", "", 1, 0, 0, SCREEN_WIDTH//2, SCREEN_HEIGHT, GRAY, GRAY, int(30), hover_color=GRAY)
            settings_box = TextInBox("fonts/Quick Starter.ttf", "SETTINGS", int(40), SCREEN_WIDTH//4, int(40), 0, 0, RED, RED, 0, True, RED)
            volume_box = TextInBox("fonts/Quick Starter.ttf", "MUSIC VOLUME", int(18), int(80), int(90), int(70), int(20), RED, RED, int(5), transparent= True, hover_color=RED)
            volume_slider = Slider(screen, int(230), int(95), int(140), int(5), min = 0, max = 100, colour = WHITE, handleColour = BLACK, handleRadius = int(10), initial = 100)
            iitdguessr_box = TextInBox("fonts/Quick Starter.ttf", "IITDGUESSR", int(40), (SCREEN_WIDTH * 3) // 4 - int(90), int(70), int(160), int(40), BLACK, CYAN, int(5), transparent = True)
            back_button = TextInBox("fonts/Quick Starter.ttf", "BACK", 25, 30, 410, 80, 25, BLACK, RED, 0, True)
            settings_page.boxList = [settings_container, settings_box, volume_box, iitdguessr_box]
            settings_page.buttonList = [back_button]
            if ratio != 1:
                settings_page.resizePage(ratio)
                vol = volume_slider.getValue()
                volume_slider = Slider(screen, int(230*ratio), int(95*ratio), int(140*ratio), int(5*ratio), min = 0, max = 100, colour = WHITE, handleColour = BLACK, handleRadius = int(10*ratio), initial = vol)
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

            
        screen.blit(pygame.transform.scale(main_menu_bg, (newWidth, newHeight)), (newWidth//4, 0))

        settings_container.render(screen)
        settings_box.render(screen)
        volume_box.render(screen)
        iitdguessr_box.render(screen)
        back_button.render(screen)
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
            choose_your_box = TextInBox("fonts/Quick Starter.ttf", "CHOOSE YOUR", 50, x = 340, y = 5, w = 410, h = 70, box_color=DARK_RED, font_color=CYAN, roundedness=0, transparent=True)
            game_mode_box = TextInBox("fonts/Quick Starter.ttf", "GAME MODE", 50, x = 372, y = 50, w = 410, h = 70, box_color=DARK_RED, font_color=CYAN, roundedness=0, transparent=True)
            mode_select_page.buttonList = [hodophilic_box, hodophobic_box]
            mode_select_page.boxList = [hodophilic_bg, hodophobic_bg, choose_your_box, game_mode_box]

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
                    if button.text_rect.collidepoint(mouse_pos):
                        button.box_color = ORANGE
                        
                        if button is hodophilic_box:
                            show_information_box_1 = True
                            break
                        else:
                            show_information_box_2 = True
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


        screen.blit(pygame.transform.scale(main_menu_bg, (newWidth, newHeight)), (0, 0))
        mode_select_page.renderBoxes(screen)
        mode_select_page.renderButtons(screen)

        print("1:", show_information_box_1)
        print("2:", show_information_box_2)

        if show_information_box_1:
            information_page_1.renderBoxes(screen)

        if show_information_box_2:
            information_page_2.renderBoxes(screen)

        
        if STATE != State.MODE_SELECT:
            initialised_mode_select = False


    pygame.display.flip()

pygame.quit()
sys.exit()