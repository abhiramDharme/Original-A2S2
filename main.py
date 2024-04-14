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
    GAME = 2
    PAUSE = 3
    MOTIVATION = 4
    SETTINGS = 5

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
RED = (255, 0, 0)
ORANGE = (255, 85, 28)
CYAN = (23, 129, 133)
BLACK = (0, 0, 0)

defaultCursor = pygame.SYSTEM_CURSOR_ARROW
handCursor = pygame.SYSTEM_CURSOR_HAND

icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

locations = [
    ("Images/1.jpg", (600, 494)),
    ("Images/2.jpg", (604, 511)),
]


def calculate_score(guess_pos, actual_pos):
    distance = math.sqrt((guess_pos[0] - actual_pos[0]) ** 2 + (guess_pos[1] - actual_pos[1]) ** 2)
    score = max(0, 100 - distance/3)
    return score

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

    def render(self, screen,):
        if not self.transparent:
            pygame.draw.rect(screen, self.box_color, (self.x, self.y, self.w, self.h), border_radius=self.current_roundedness)
        screen.blit(self.text_surface, self.text_rect)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("IITDGuessr")

main_menu_bg = pygame.image.load("home_page.jpg")
texture_main_menu_bg = main_menu_bg.convert()

# play_button_clicked = False
# showing_location = False
# location_image = None
# current_location = None
# total_score = 0
# actual_location_shown = False

pygame.mixer.music.load('bgm.mp3')
pygame.mixer.music.play(-1)

running = True
initialised_main_menu = False
initalised_settings = False

while running:
    if STATE == State.MAIN_MENU:

        if not initialised_main_menu:
            play_button = TextInBox("fonts/Quick Starter.ttf", "PLAY GAME", 20, SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 - 10, 180, 35, RED, WHITE, 5)
            settings_button = TextInBox("fonts/Quick Starter.ttf", "SETTINGS", 20, SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 35, 180, 35, RED, WHITE, 5)
            motivation_button = TextInBox("fonts/Quick Starter.ttf", "MOTIVATION", 20, SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 80, 180, 35, RED, WHITE, 5)
            quit_button = TextInBox("fonts/Quick Starter.ttf", "QUIT GAME", 20, SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 125, 180, 35, RED, WHITE, 5)
            createdby_box = TextInBox("fonts/ARIBL0.ttf", "Created by", 13, 750, 420, 0, 0, BLACK, WHITE, 0, True, BLACK)
            s_and_a_box = TextInBox("fonts/ARIBL0.ttf", "SK and ASD", 13, 750, 440, 0, 0, BLACK, WHITE, 0, True, BLACK)
            iitd_guessr = TextInBox("fonts/Quick Starter.ttf", "IITDGUESSR", 70, SCREEN_WIDTH // 2 - 90, 70, 160, 40, BLACK, CYAN, 5, transparent = True)

            if ratio != 1:
                play_button.update_dimensions(ratio)
                motivation_button.update_dimensions(ratio)
                settings_button.update_dimensions(ratio)
                quit_button.update_dimensions(ratio)
                iitd_guessr.update_dimensions(ratio)
                createdby_box.update_dimensions(ratio)
                s_and_a_box.update_dimensions(ratio)

            initialised_main_menu = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                if play_button.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(handCursor)
                    play_button.box_color = ORANGE
                elif motivation_button.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(handCursor)
                    motivation_button.box_color = ORANGE

                elif settings_button.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(handCursor)
                    settings_button.box_color = ORANGE

                elif quit_button.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(handCursor)
                    quit_button.box_color = ORANGE

                else:
                    pygame.mouse.set_cursor(defaultCursor)
                    play_button.box_color = RED
                    motivation_button.box_color = RED
                    settings_button.box_color = RED
                    quit_button.box_color = RED
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if play_button.rect.collidepoint(mouse_pos):
                    STATE = State.GAME
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

                play_button.update_dimensions(ratio)
                motivation_button.update_dimensions(ratio)
                settings_button.update_dimensions(ratio)
                quit_button.update_dimensions(ratio)
                iitd_guessr.update_dimensions(ratio)
                createdby_box.update_dimensions(ratio)
                s_and_a_box.update_dimensions(ratio)

        screen.blit(pygame.transform.scale(main_menu_bg, (newWidth, newHeight)), (0, 0 ))

        play_button.render(screen)
        motivation_button.render(screen)
        settings_button.render(screen)
        quit_button.render(screen)
        iitd_guessr.render(screen)    
        createdby_box.render(screen)
        s_and_a_box.render(screen)
        pygame.display.flip()

        if STATE != State.MAIN_MENU:
            initialised_main_menu = False


    if STATE == State.SETTINGS:
        if not initalised_settings:
            pygame.mouse.set_cursor(defaultCursor)
            settings_container = TextInBox("fonts/Quick Starter.ttf", "", 1, 0, 0, SCREEN_WIDTH//2, SCREEN_HEIGHT, GRAY, GRAY, int(5), hover_color=GRAY)
            settings_box = TextInBox("fonts/Quick Starter.ttf", "SETTINGS", int(40), SCREEN_WIDTH//4, int(40), 0, 0, RED, RED, 0, True, RED)
            volume_box = TextInBox("fonts/Quick Starter.ttf", "MUSIC VOLUME", int(18), int(80), int(90), int(70), int(20), RED, RED, int(5), transparent= True, hover_color=RED)
            volume_slider = Slider(screen, int(230), int(95), int(140), int(5), min = 0, max = 100, colour = WHITE, handleColour = BLACK, handleRadius = int(10), initial = 100)
            iitdguessr_box = TextInBox("fonts/Quick Starter.ttf", "IITDGUESSR", int(40), (SCREEN_WIDTH * 3) // 4 - int(90), int(70), int(160), int(40), BLACK, CYAN, int(5), transparent = True)
            back_button = TextInBox("fonts/Quick Starter.ttf", "BACK", 25, 30, 410, 80, 25, BLACK, RED, 0, True)
            if ratio != 1:
                settings_container.update_dimensions(ratio)
                settings_box.update_dimensions(ratio)
                volume_box.update_dimensions(ratio)
                iitdguessr_box.update_dimensions(ratio)
                vol = volume_slider.getValue()
                back_button.update_dimensions(ratio)
                volume_slider = Slider(screen, int(230*ratio), int(95*ratio), int(140*ratio), int(5*ratio), min = 0, max = 100, colour = WHITE, handleColour = BLACK, handleRadius = int(10*ratio), initial = vol)
            initalised_settings = True
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

                settings_box.update_dimensions(ratio)
                settings_container.update_dimensions(ratio)
                volume_box.update_dimensions(ratio)
                iitdguessr_box.update_dimensions(ratio)
                back_button.update_dimensions(ratio)
                vol = volume_slider.getValue()
                volume_slider = Slider(screen, int(230*ratio), int(95*ratio), int(140*ratio), int(5*ratio), min = 0, max = 100, colour = WHITE, handleColour = BLACK, handleRadius = int(10*ratio), initial = vol)
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                if back_button.text_rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(handCursor)
                    back_button.font_color = ORANGE
                    back_button.update_dimensions(ratio)
                else:
                    back_button.font_color = RED
                    pygame.mouse.set_cursor(defaultCursor)
                    back_button.update_dimensions(ratio)
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
        pygame.display.flip()

        if STATE != State.SETTINGS:
            initialised_settings = False

    # if STATE == State.GAME:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #         elif event.type == pygame.WINDOWRESIZED:
            
        
    #     elif event.type == pygame.MOUSEBUTTONDOWN:
    #         mouse_pos = event.pos
    #         # Calculate the map's area on screen
    #         map_start_x = int(SCREEN_WIDTH * 1 / 5)
    #         map_end_x = SCREEN_WIDTH
    #         if not play_button_clicked:
    #             if play_button.text_rect.collidepoint(mouse_pos):
    #                 play_button_clicked = True
    #                 showing_location = True
    #                 current_location = random.choice(locations)
    #                 location_image = load_location_image(current_location[0], (int(SCREEN_WIDTH * 4 / 5), SCREEN_HEIGHT//(2)))
    #         elif showing_location:
    #             showing_location = False
    #         elif play_button_clicked and not showing_location and not actual_location_shown:
    #             if map_start_x <= mouse_pos[0] <= map_end_x:
    #                 # Calculate relative mouse position on the map
    #                 relative_mouse_pos = (mouse_pos[0] - map_start_x, mouse_pos[1])
    #                 map_relative_pos = (relative_mouse_pos[0] * campus_map_image.get_width() // (SCREEN_WIDTH * 4 // 5), relative_mouse_pos[1] * campus_map_image.get_height() // SCREEN_HEIGHT)
    #                 round_score = int(calculate_score(map_relative_pos, current_location[1]))
    #                 total_score += round_score
    #                 print(f"Guess made at {map_relative_pos}, actual location is {current_location[1]}. Round Score: {round_score}, Total Score: {total_score}")
    #                 actual_location_shown = True
    #         elif actual_location_shown:
    #             showing_location = True
    #             play_button_clicked = True
    #             actual_location_shown = False
    #             current_location = random.choice(locations)
    #             location_image = load_location_image(current_location[0], (int(SCREEN_WIDTH * 4 / 5), SCREEN_HEIGHT//(2)))


    # if not play_button_clicked:
    #     screen.blit(pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
    #     play_button.render(screen)
    # elif showing_location:
    #     screen.blit(pygame.transform.scale(location_image, (int(SCREEN_WIDTH * 1 / 5), SCREEN_HEIGHT//(2))), (0, 0))
    # else:
    #     map_surface = pygame.transform.scale(campus_map_image, (int(SCREEN_WIDTH * 4 / 5), SCREEN_HEIGHT))
    #     screen.blit(map_surface, (int(SCREEN_WIDTH * 1 / 5), 0))
    #     if actual_location_shown:
    #         # Adjust the position of the red dot relative to the scaled map
    #         adjusted_dot_pos = (int(current_location[1][0] * (SCREEN_WIDTH * 4 / 5) / campus_map_image.get_width() + SCREEN_WIDTH * 1 / 5), int(current_location[1][1] * SCREEN_HEIGHT / campus_map_image.get_height()))
    #         pygame.draw.circle(screen, RED, adjusted_dot_pos, 5)


pygame.quit()
sys.exit()