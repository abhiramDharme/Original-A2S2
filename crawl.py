from colours import *
from constants import *

initialised_motivation = False

crawl_text = open("motivation.txt", "r").read()
font_size_for_crawl = 15
font = pygame.font.Font("fonts/Quick Starter.ttf", font_size_for_crawl)

crawl_y_pos = SCREEN_HEIGHT
crawl_active = False

def start_crawl(screen, lines):
    global crawl_y_pos, crawl_active
    if not crawl_active:
        crawl_y_pos = SCREEN_HEIGHT
        crawl_active = True

    screen.fill(BLACK)
    crawl_y_pos -= 0.2

    for i, line in enumerate(lines):
        text_surface = font.render(line, True, YELLOW)
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, crawl_y_pos + i * 30))
        screen.blit(text_surface, text_rect)

    if crawl_y_pos + len(lines) * 30 < -100:
        crawl_active = False
        return False
    
    return True