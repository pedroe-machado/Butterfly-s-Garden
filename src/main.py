import pygame as pg
from game import Game
from settings import Settings

def main():
    pg.init()
    settings = Settings()
    game = Game(settings)
    game.run()
    pg.quit()

if __name__ == "__main__":
    main()