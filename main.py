import pygame
from scenes.cell_level_zones.cell_level import CellLevel
from scenes.IntroSceneV1 import IntroScene

if __name__ == "__main__":
    while True:
        intro = IntroScene()
        intro.run()
        game = CellLevel()
        game.run()