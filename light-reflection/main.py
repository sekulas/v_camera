import pygame as pg
import numpy as np
from math import *
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 1, 0)
PURPLE = (171, 32, 253)
BLUE = (0, 9, 255)
PINK = (255, 0, 177)
YELLOW = (255, 227, 0)
GREEN = (0, 255, 13)
ORANGE = (255, 95, 31)

WINDOW_X_SIZE = 800
WINDOW_Y_SIZE = 600

X_INDEX = 0
Y_INDEX = 1
Z_INDEX = 2
LIGHT_STEP = 10

projection_matrix = np.matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])    

class GraphicsEngine:
    def __init__(self, win_size=(int,int)):
        pg.init()
        pg.display.set_caption("Phong: Light Reflection")
        
        self.WIN_SIZE = win_size
        self.screen = pg.display.set_mode(self.WIN_SIZE)

        self.clock = pg.time.Clock()

        self.light = [0, 0, 0]

    def check_events(self):        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_a:
                    self.light[X_INDEX] += LIGHT_STEP
                if event.key == pg.K_d:
                    self.light[X_INDEX] -= LIGHT_STEP
                if event.key == pg.K_w:
                    self.light[Y_INDEX] += LIGHT_STEP
                if event.key == pg.K_s:
                    self.light[Y_INDEX] -= LIGHT_STEP


    def draw(self):
        self.screen.fill(BLACK)
        pg.draw.circle(self.screen, RED, (WINDOW_X_SIZE//2 - self.light[X_INDEX], WINDOW_Y_SIZE//2 - self.light[Y_INDEX]), 5)


    def render(self):
        pg.display.flip()

    def run(self):
        while True:
            self.check_events()
            self.draw()
            self.render()
            self.clock.tick(60)

if __name__ == '__main__':
    app = GraphicsEngine((WINDOW_X_SIZE, WINDOW_Y_SIZE))
    app.run()