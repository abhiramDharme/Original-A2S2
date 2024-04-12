.PHONY:compile run 

all : compile run

compile:
	@g++ main.cpp -o main.exe -Iinclude -Llib -lSDL2.a -lSDL2_image.a -lSDL2_ttf.a -lSDL2_gfx.a

run:
	@./main.exe