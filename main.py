import pygame as pg
import numpy as np
from camera import Camera
from objects.cube import Cube
from math import *
import matrix_transformations
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WINDOW_X_SIZE = 800
WINDOW_Y_SIZE = 600

projection_matrix = np.matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])    

scale = 30

circle_pos = (WINDOW_X_SIZE / 2, WINDOW_Y_SIZE / 2)


class GraphicsEngine:
    def __init__(self, win_size=(int,int)):
        pg.init()
        pg.display.set_caption("Virtual Camera")
        
        self.WIN_SIZE = win_size
        self.screen = pg.display.set_mode(self.WIN_SIZE)

        self.clock = pg.time.Clock()

        self.objects = [Cube(1, 1, 1, BLACK, 1, 5)]

        self.camera = Camera(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_SPACE:
                    self.camera.move_up()
                if event.key == pg.K_LSHIFT:
                    self.camera.move_down()
                if event.key == pg.K_d:
                    self.camera.move_right()
                if event.key == pg.K_a:
                    self.camera.move_left()

    def draw(self):
        self.screen.fill(WHITE)
        for obj in self.objects:
            for line in obj.lines:
                projected2d = np.dot(projection_matrix, line.a)
                projected2db = np.dot(projection_matrix, line.b)
                
                x = int(projected2d[0][0] * scale) + circle_pos[0]
                y = int(projected2d[1][0] * scale) + circle_pos[1]
                x2 = int(projected2db[0][0] * scale) + circle_pos[0]
                y2 = int(projected2db[1][0] * scale) + circle_pos[1]

                pg.draw.circle(self.screen, BLACK, (x,y), 5)
                pg.draw.circle(self.screen, BLACK, (x2,y2), 5)

                pg.draw.line(self.screen, obj.color, (x,y), (x2,y2))



    def render(self):
        pg.display.flip()

    def run(self):
        while True:
            self.check_events()
            self.draw()
            self.render()
            self.clock.tick(60)

    def update_points(self, transform_matrix):
        for obj in self.objects:
            for idx, point in enumerate(obj.points):
                new_point = np.dot(transform_matrix, point)
                for p in range(0, 3):
                    obj.points[idx][p] = new_point[p]

if __name__ == '__main__':
    app = GraphicsEngine((WINDOW_X_SIZE, WINDOW_Y_SIZE))
    app.run()