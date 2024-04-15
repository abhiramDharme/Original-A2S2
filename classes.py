import pygame

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

class Textures:
    def __init__(self, image_loc, x, y, width, height):
        self.texture = pygame.image.load(image_loc).convert_alpha()
        self.X = x
        self.x = x
        self.Y = y
        self.y = y
        self.W = width
        self.w = width
        self.H = height
        self.h = height

    def update_dimensions(self, ratio):
        self.x = ratio * self.X
        self.y = ratio * self.Y
        self.w = ratio * self.W
        self.h = ratio * self.H

    def render(self, screen):
        screen.blit(pygame.transform.smoothscale(self.texture, (self.w, self.h)), (self.x, self.y))

class Page:
    def __init__(self):
        self.buttonList = []
        self.boxList = []
        self.textureList = []
        self.pos_marked = False
        self.error = False

    def resizePage(self, ratio):
        for box in self.boxList:
            box.update_dimensions(ratio)
        for button in self.buttonList:
            button.update_dimensions(ratio)
        for texture in self.textureList:
            texture.update_dimensions(ratio)

    def renderBoxes(self, screen):
        for box in self.boxList:
            box.render(screen)
    def renderButtons(self,screen):
        for button in self.buttonList:
            button.render(screen)
    def renderTextures(self, screen):
        for texture in self.textureList:
            texture.render(screen)
