import pygame
from scenes.cell_level_zones.cell_level import CellLevel
from scenes.IntroSceneV1 import IntroScene

if __name__ == "__main__":
    game = CellLevel()
    game = IntroScene()
    game.run()

