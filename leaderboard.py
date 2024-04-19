import pandas as pd
from classes import *
from colours import *

file_path = "leaderboard.csv"


def update_leaderboard(score):

    df = pd.read_csv(file_path)

    for i in range(0,5):
        if score > df.iloc[i, 2]:
            return True, i+1
    return False, 6

def write_leaderboard(rank, name, score):

    df = pd.read_csv(file_path)

    for i in range(4, rank - 1, -1):
        df.iloc[i, 1] = df.iloc[i-1, 1]
        df.iloc[i, 2] = df.iloc[i-1, 2]

    df.loc[rank-1] = rank, name, score

    df.to_csv(file_path, index = False)


initialised_leaderboard = False

leaderboard_page = Page()

leaderboard_container = TextInBox("fonts/Quick Starter.ttf", "", 1, 40, 60, 720, 370, GRAY, GRAY,15)
back_button = TextInBox("fonts/Quick Starter.ttf", "BACK", 22, x = 10, y = 10, w = 90, h = 40, box_color=RED, font_color=WHITE, roundedness=10, transparent=False)

df = pd.read_csv("leaderboard.csv")

rank_box = TextInBox("fonts/Quick Starter.ttf", "RANK", 25, 100, 90, 0, 0, RED, RED,15, transparent = True)
name_box = TextInBox("fonts/Quick Starter.ttf", "NAME", 25, 400, 90, 0, 0, RED, RED,15, transparent = True)
score_box = TextInBox("fonts/Quick Starter.ttf", "SCORE", 25, 680, 90, 0, 0, RED, RED,15, transparent = True)

leaderboard_page.buttonList = [back_button]
leaderboard_page.boxList = [leaderboard_container, rank_box, name_box, score_box]

for i in range(0,5):
    rank_box = TextInBox("fonts/Quick Starter.ttf", str(df.iloc[i,0]).upper() + '.', 25, 100, 150 + 60*i, 0, 0, RED, RED,15, transparent = True)
    name_box = TextInBox("fonts/Quick Starter.ttf", str(df.iloc[i,1]).upper(), 25, 400, 150 + 60 * i, 0, 0, RED, RED,15, transparent = True)
    score_box = TextInBox("fonts/Quick Starter.ttf", str(df.iloc[i, 2]).upper(), 25, 680, 150 + 60 * i, 0, 0, RED, RED,15, transparent = True)
    leaderboard_page.boxList = leaderboard_page.boxList + [rank_box, name_box, score_box]