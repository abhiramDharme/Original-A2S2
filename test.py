import pygame
import sys
import random
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
GRAY = (136, 136, 136)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

locations = [
    ("Images/1.jpg", (604, 497)),
    ("Images/2.jpg", (606, 512)),
]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("IITDGuessr")

def calculate_score(guess_pos, actual_pos):
    distance = math.sqrt((guess_pos[0] - actual_pos[0]) ** 2 + (guess_pos[1] - actual_pos[1]) ** 2)
    score = max(0, 100 - distance)
    return score

def maintain_aspect_ratio(src_size, target_size):
    src_width, src_height = src_size
    target_width, target_height = target_size

    src_aspect = src_width / src_height
    target_aspect = target_width / target_height

    if src_aspect > target_aspect:
        new_width = target_width
        new_height = target_width / src_aspect
    else:
        new_width = target_height * src_aspect
        new_height = target_height

    return int(new_width), int(new_height)

class TextInBox:
    def __init__(self, font_location, text_to_print, initial_font_size, x, y, w, h, box_color, font_color, roundedness, screen_size):
        self.font_location = font_location
        self.initial_font_size = initial_font_size
        self.text_to_print = text_to_print
        self.box_color = box_color
        self.font_color = font_color
        self.roundedness = roundedness
        self.update_dimensions(x, y, w, h, screen_size)

    def update_dimensions(self, x, y, w, h, screen_size):
        self.x = x * screen_size[0] // SCREEN_WIDTH
        self.y = y * screen_size[1] // SCREEN_HEIGHT
        self.w = w * screen_size[0] // SCREEN_WIDTH
        self.h = h * screen_size[1] // SCREEN_HEIGHT
        font_size = self.initial_font_size * min(screen_size[0] // SCREEN_WIDTH, screen_size[1] // SCREEN_HEIGHT)
        self.font = pygame.font.Font(self.font_location, font_size)
        self.text_surface = self.font.render(self.text_to_print, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))

    def render(self, screen):
        pygame.draw.rect(screen, self.box_color, (self.x, self.y, self.w, self.h), border_radius=self.roundedness)
        screen.blit(self.text_surface, self.text_rect)

def load_images():
    try:
        background = pygame.image.load("home_page.jpg").convert()
        campus_map = pygame.image.load("campus_map.png").convert_alpha()
    except pygame.error as e:
        print(f"Error loading the image: {e}")
        sys.exit()
    return background, campus_map

def load_location_image(path, target_size):
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(image, maintain_aspect_ratio(image.get_size(), target_size))
    except pygame.error as e:
        print(f"Error loading the location image: {e}")
        sys.exit()

background_image, campus_map_image = load_images()
campus_map_image = pygame.transform.scale(campus_map_image, (SCREEN_WIDTH * 4 // 5, SCREEN_HEIGHT))

play_button = TextInBox(pygame.font.match_font('arial'), "play", 30, SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 100, 140, 70, GRAY, WHITE, 5, screen.get_size())

play_button_clicked = False
showing_location = False
location_image = None
current_location = None
total_score = 0
actual_location_shown = False

map_start_x = SCREEN_WIDTH // 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if not play_button_clicked and play_button.text_rect.collidepoint(mouse_pos):
                play_button_clicked = True
                showing_location = True
                current_location = random.choice(locations)
                location_image = load_location_image(current_location[0], (SCREEN_WIDTH // 5, SCREEN_HEIGHT // 3))
                actual_location_shown = False
            elif actual_location_shown:
                play_button_clicked = True
                showing_location = True
                actual_location_shown = False
                current_location = random.choice(locations)
                location_image = load_location_image(current_location[0], (SCREEN_WIDTH // 5, SCREEN_HEIGHT // 3))
            elif play_button_clicked and not showing_location and not actual_location_shown:
                if map_start_x <= mouse_pos[0] <= SCREEN_WIDTH:
                    relative_mouse_pos = (mouse_pos[0] - map_start_x, mouse_pos[1])
                    map_relative_pos = (relative_mouse_pos[0] * campus_map_image.get_width() // (SCREEN_WIDTH * 4 // 5), relative_mouse_pos[1] * campus_map_image.get_height() // SCREEN_HEIGHT)
                    round_score = int(calculate_score(map_relative_pos, current_location[1]))
                    total_score += round_score
                    actual_location_shown = True

    # screen.fill(WHITE)

    if not play_button_clicked:
        screen.blit(background_image, (0, 0))
        play_button.render(screen)
    elif showing_location:
        screen.blit(location_image, (0, 0))
    else:
        screen.blit(campus_map_image, (map_start_x, 0))
        if actual_location_shown:
            adjusted_dot_pos = (int(current_location[1][0] * (SCREEN_WIDTH * 4 // 5) / campus_map_image.get_width() + map_start_x), int(current_location[1][1] * SCREEN_HEIGHT / campus_map_image.get_height()))
            pygame.draw.circle(screen, RED, adjusted_dot_pos, 5)

        # Display score in the green box
        score_text = f'Score: {total_score}'
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(score_text, True, BLACK)
        screen.blit(text_surface, (10, SCREEN_HEIGHT * 2 // 3 + 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
