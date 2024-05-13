import pygame as pg
import numpy as np
from point import Point
from math import *
import sys
from phong import Phong

RED = (255, 1, 0)
GREY = (192,192,192)

METALIC = (187,187,187)
BRICK = (188, 74, 60)
PLASTIC = (0,0,255)
WOOD = (139,69,19)

WINDOW_X_SIZE = 800
WINDOW_Y_SIZE = 600

X_INDEX = 0
Y_INDEX = 1
Z_INDEX = 2
LIGHT_STEP = 20
SPHERE_SIZE = 100

projection_matrix = np.matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])    

class GraphicsEngine:
    def __init__(self, win_size=(int,int)):
        self.aprox = 2
        pg.init()
        pg.display.set_caption("Phong: Light Reflection")
        
        self.WIN_SIZE = win_size
        self.screen = pg.display.set_mode(self.WIN_SIZE)

        self.clock = pg.time.Clock()

        self.light = [0, 0, -300]
        self.sphere_points = self.__init_sphere()
        self.redraw = True
        self.camera_position = [0, 0, -200]
        self.phong = Phong(self, 0.1, 0.4, 0.9, "", 150)

    def check_events(self):        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_1:
                    self.__change_sphere_color(METALIC)
                    # self.phong = Phong(self, 0.1, 0.4, 0.9, "", 150)
                    self.phong = Phong(self, 0.1, 0.1, 0.9, "", 150)
                    self.redraw = True
                if event.key == pg.K_2:
                    self.__change_sphere_color(PLASTIC)
                    # self.phong = Phong(self, 0.2, 0.8, 0.6, "", 50)
                    self.phong = Phong(self, 0.2, 0.4, 0.6, "", 50)
                    self.redraw = True
                if event.key == pg.K_3:
                    self.__change_sphere_color(WOOD)
                    # self.phong = Phong(self, 0.3, 0.8, 0.2, "", 20)
                    self.phong = Phong(self, 0.3, 0.8, 0.2, "", 20)
                    self.redraw = True
                if event.key == pg.K_4:
                    self.__change_sphere_color(BRICK)
                    # self.phong = Phong(self, 0.3, 0.8, 0.1, "", 10)
                    self.phong = Phong(self, 0.3, 0.9, 0.1, "", 10)
                    self.redraw = True

        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.light[X_INDEX] += LIGHT_STEP
            self.redraw = True
        elif keys[pg.K_d]:
            self.light[X_INDEX] -= LIGHT_STEP
            self.redraw = True
        if keys[pg.K_w]:
            self.light[Y_INDEX] += LIGHT_STEP
            self.redraw = True
        elif keys[pg.K_s]:
            self.light[Y_INDEX] -= LIGHT_STEP
            self.redraw = True


    def draw(self):
        self.screen.fill(GREY)
        for point in self.sphere_points:
            self.phong.calc_light_reflection(point)
            pg.draw.circle(self.screen, point.color, (WINDOW_X_SIZE//2 - point.x, WINDOW_Y_SIZE//2 - point.y), self.aprox)
        pg.draw.circle(self.screen, RED, (WINDOW_X_SIZE//2 - self.light[X_INDEX], WINDOW_Y_SIZE//2 - self.light[Y_INDEX]), 5)


    def render(self):
        pg.display.flip()

    def run(self):
        while True:
            self.check_events()
            if(self.redraw):
                self.draw()
            self.render()
            self.clock.tick(60)
            self.redraw = False

    def __init_sphere(self):
        x_range = range(-SPHERE_SIZE, SPHERE_SIZE+1, self.aprox)

        points = [Point(x, y, -sqrt(SPHERE_SIZE**2 - x**2 - y**2), METALIC) 
            for x in x_range 
            for y in range(int(-sqrt(SPHERE_SIZE**2 - x**2)), int(sqrt(SPHERE_SIZE**2 - x**2)), self.aprox)]

        return points
    
    def __change_sphere_color(self, color):
        for point in self.sphere_points:
            point.change_color(color);

if __name__ == '__main__':
    app = GraphicsEngine((WINDOW_X_SIZE, WINDOW_Y_SIZE))
    app.run()