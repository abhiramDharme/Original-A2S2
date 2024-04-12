#define SDL_MAIN_HANDLED
#include "SDL2/include/SDL.h" 
#include "SDL2/include/SDL_image.h"
#include "SDL2/include/SDL_ttf.h"
#include "SDL2/include/SDL2_gfxPrimitives.h"
#include <string>
#include <iostream>

using namespace std;

const float SCREEN_WIDTH = 640;
const float SCREEN_HEIGHT = 360;

class text_in_box {
public:
    string font_location;
    string text_to_print;
    int initial_font_size;
    int x;
    int y;
    int w;
    int h;
    Uint16 roundedness;
    Uint32 box_color;
    SDL_Surface* text_box_play;
    SDL_Texture* texture_box_play;
    TTF_Font* font;
    SDL_Rect rect;
    SDL_Rect text_rect;

    text_in_box (string font_location, string text_to_print, int initial_font_size, 
                int x, int y, int w, int h, 
                Uint32 box_color, Uint32 font_color, Uint16 roundedness, 
                SDL_Renderer* &renderer) {
        this->x=x; this->y=y; this->w=w; this->h=h; this->box_color=box_color;
        this->font = TTF_OpenFont(font_location.c_str(), initial_font_size);

        SDL_Color f_color;
        f_color.r = (font_color >> 24) & 0xFF; // Extract red
        f_color.g = (font_color >> 16) & 0xFF; // Extract green
        f_color.b = (font_color >> 8) & 0xFF;  // Extract blue
        f_color.a = font_color & 0xFF;

        SDL_Rect rect = {x, y, w, h};
        this->rect = rect;

        this->text_box_play = TTF_RenderText_Solid(font, text_to_print.c_str(), f_color);

        this->texture_box_play = SDL_CreateTextureFromSurface(renderer, text_box_play);

        int text_width, text_height;
        TTF_SizeText(font, text_to_print.c_str(), &text_width, &text_height);

        SDL_Rect text_rect;
        text_rect.x = rect.x + (rect.w - text_width) / 2; // Center the text within the rectangle
        text_rect.y = rect.y + (rect.h - text_height) / 2;
        text_rect.w = text_width;
        text_rect.h = text_height;
        this->text_rect = text_rect;

    }

    void render(SDL_Renderer* &renderer) {
        SDL_SetRenderDrawColor(renderer, (box_color >>24) & 0xFF, (box_color >> 16) & 0xFF, (box_color >> 8) & 0xFF, (box_color) & 0xFF);
        SDL_RenderFillRect(renderer, &rect); // Draw the box
        roundedBoxColor(renderer, rect.x, rect.y, rect.x + rect.w, rect.y + rect.h, roundedness, box_color);
        SDL_RenderCopy(renderer, texture_box_play, NULL, &text_rect);
    }

    ~text_in_box() {
        SDL_DestroyTexture(texture_box_play);
        SDL_FreeSurface(text_box_play);
        TTF_CloseFont(font);       
    }
};

int main( int argc, char* args[] ) {
    
    if( SDL_Init( SDL_INIT_VIDEO ) < 0 ) {
        printf( "SDL could not initialize! SDL_Error: %s\n", SDL_GetError() );
        return 1;
    }

    if (TTF_Init() == -1) {
        printf("TTF_Init: %s\n", TTF_GetError());
        return 1;
    }

    SDL_Cursor* defaultCursor = SDL_GetDefaultCursor();
    SDL_Cursor* handCursor = SDL_CreateSystemCursor(SDL_SYSTEM_CURSOR_HAND);

    int initial_font_size = 30;

    SDL_Window * window = SDL_CreateWindow( "IITDGuessr", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN | SDL_WINDOW_RESIZABLE);
    if( window == NULL ) {
        printf( "Window could not be created! SDL_Error: %s\n", SDL_GetError() );
        return 1;
    }

    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    
    SDL_Surface* image = IMG_Load("home_page.jpg");
    SDL_Texture* texture = SDL_CreateTextureFromSurface(renderer, image);

    text_in_box* play_button = new text_in_box("fonts/Quick Starter.ttf", "play", 30, SCREEN_WIDTH/2 - 70, SCREEN_HEIGHT/2 - 100, 140, 70, 0x888888, 0xF0F0F0, 5, renderer);

    SDL_RenderCopy(renderer, texture, NULL, NULL);
    play_button->render(renderer);
    SDL_RenderPresent(renderer);

    //Hack to get window to stay up
    SDL_Event e; 
    bool quit = false; 
    while( quit == false ){ 
        SDL_RenderClear(renderer);
        float newWidth, newHeight;
        while( SDL_PollEvent( &e ) ) { 
            SDL_Point mouse_pos;
            switch(e.type) {
                case SDL_QUIT:
                    quit = true;
                    break;
                case SDL_WINDOWEVENT:
                    if (e.window.event == SDL_WINDOWEVENT_RESIZED) {
                        newWidth = e.window.data1;
                        newHeight = e.window.data2;

                        if (newWidth * SCREEN_HEIGHT / SCREEN_WIDTH > newHeight) {
                            newWidth = newHeight * SCREEN_WIDTH / SCREEN_HEIGHT;
                        } 
                        else {
                            newHeight = newWidth * SCREEN_HEIGHT / SCREEN_WIDTH;
                        }

                        float ratio = newWidth / SCREEN_WIDTH;

                        play_button->x = newWidth / 2 - 100*ratio;
                        play_button->y = newHeight / 2 - 100*ratio;
                        play_button->w = 200*ratio;
                        play_button->h = 50*ratio;
                        play_button->initial_font_size = 20*ratio;
                        play_button->roundedness = 10*ratio;

                        SDL_SetWindowSize(window, newWidth, newHeight);
                    }
                    break;

                case SDL_MOUSEMOTION:
                    mouse_pos.x = e.motion.x;
                    mouse_pos.y = e.motion.y;

                    if (SDL_PointInRect(&mouse_pos, &play_button->rect)) {
                        SDL_SetCursor(handCursor);
                    } 
                    else {
                        SDL_SetCursor(defaultCursor);
                    }
                    break;

                case SDL_MOUSEBUTTONDOWN:
                    SDL_GetMouseState(&mouse_pos.x, &mouse_pos.y);
                    // Check if the click was within the rectangle for each option
                    if (SDL_PointInRect(&mouse_pos, &play_button->rect)) {
                        // Perform action for option 1
                    }
                    // else if (SDL_PointInRect(&mouse_pos, &option2)) {
                    //     // Perform action for option 2
                    // }
                    // else if (SDL_PointInRect(&mouse_pos, &option3)) {
                    //     // Perform action for option 3
                    // }
                    // else if (SDL_PointInRect(&mouse_pos, &option4)) {
                    //     // Perform action for option 4
                    // }

            }
        }

        SDL_RenderCopy(renderer, texture, NULL, NULL);
        play_button->render(renderer);
        SDL_RenderPresent(renderer);
    }


    SDL_FreeCursor(handCursor);
    SDL_FreeCursor(defaultCursor);
    delete play_button;
    SDL_DestroyTexture(texture);
    SDL_FreeSurface(image);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);

    SDL_Quit();

    return 0;
}