import pygame as pg
import numpy as np
from camera import Camera
from objects.cube import Cube
#from bsp import BSPNode
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

MIN_FOCAL_LEN = 1000
MAX_FOCAL_LEN = 2000
DIST_FROM_CENTER = 100

projection_matrix = np.matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])    

class GraphicsEngine:
    def __init__(self, win_size=(int,int)):
        pg.init()
        pg.display.set_caption("Virtual Camera")
        
        self.WIN_SIZE = win_size
        self.screen = pg.display.set_mode(self.WIN_SIZE)

        self.clock = pg.time.Clock()

        self.objects = [Cube(DIST_FROM_CENTER, DIST_FROM_CENTER, DIST_FROM_CENTER, BLACK, MIN_FOCAL_LEN / 2),
                        Cube(-DIST_FROM_CENTER, DIST_FROM_CENTER, DIST_FROM_CENTER, RED, MIN_FOCAL_LEN / 2),
                        Cube(DIST_FROM_CENTER, -DIST_FROM_CENTER, DIST_FROM_CENTER, BLUE, MIN_FOCAL_LEN / 2),
                        Cube(DIST_FROM_CENTER, DIST_FROM_CENTER, -DIST_FROM_CENTER, GREEN, MIN_FOCAL_LEN / 2),
                        Cube(-DIST_FROM_CENTER, DIST_FROM_CENTER, -DIST_FROM_CENTER, YELLOW, MIN_FOCAL_LEN / 2),
                        Cube(DIST_FROM_CENTER, -DIST_FROM_CENTER, -DIST_FROM_CENTER, PINK, MIN_FOCAL_LEN / 2),
                        Cube(-DIST_FROM_CENTER, -DIST_FROM_CENTER, DIST_FROM_CENTER, PURPLE, MIN_FOCAL_LEN / 2),
                        Cube(-DIST_FROM_CENTER, -DIST_FROM_CENTER, -DIST_FROM_CENTER, ORANGE, MIN_FOCAL_LEN / 2),]

        self.camera = Camera(self)

        self.focal_len = 1000

    def check_events(self):        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    if self.focal_len <= MAX_FOCAL_LEN:
                        self.focal_len += 100
                if event.key == pg.K_x:
                    if self.focal_len >= MIN_FOCAL_LEN:
                        self.focal_len -= 100

        keys = pg.key.get_pressed()

        if keys[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()
        if keys[pg.K_SPACE]:
            self.camera.move_up()
        if keys[pg.K_LSHIFT]:
            self.camera.move_down()
        if keys[pg.K_d]:
            self.camera.move_right()
        if keys[pg.K_a]:
            self.camera.move_left()
        if keys[pg.K_w]:
            self.camera.move_forward()
        if keys[pg.K_s]:
            self.camera.move_back()

        if keys[pg.K_q]:
            self.camera.rotate_left()
        if keys[pg.K_e]:
            self.camera.rotate_right()
        if keys[pg.K_u]:
            self.camera.rotate_up()
        if keys[pg.K_i]:
            self.camera.rotate_down()
        if keys[pg.K_o]:
            self.camera.rotate_clockwise()
        if keys[pg.K_p]:
            self.camera.rotate_counter_clockwise()

        if keys[pg.K_EQUALS]:
            if self.focal_len <= MAX_FOCAL_LEN:
                self.focal_len += 100
        if keys[pg.K_MINUS]:
            if self.focal_len >= MIN_FOCAL_LEN:
                self.focal_len -= 100

    @staticmethod
    def project_point_3d_to_2d(point, focal_len, window_x_size, window_y_size):
        z1 = point[2, 0]

        x1 = np.float64(point[0, 0]) * focal_len / z1 + window_x_size / 2
        y1 = np.float64(point[1, 0]) * focal_len / z1 + window_y_size / 2

        proj_a = np.matrix([[x1], [y1], [z1]], dtype=np.float64)

        return proj_a

    def draw(self):
        self.screen.fill(WHITE)
        all_triangles = []

        for obj in self.objects:
            all_triangles.extend(obj.triangles)

        all_triangles.sort(key=lambda tri: (tri.a[2, 0] + tri.b[2, 0] + tri.c[2, 0]) / 3, reverse=True)

        for triangle in all_triangles:
            points = [GraphicsEngine.project_point_3d_to_2d(point, self.focal_len, WINDOW_X_SIZE, WINDOW_Y_SIZE) \
                      for point in triangle.points]

            if all(point[2, 0] > 0 for point in points):
                x1 = float(points[0][0, 0])
                y1 = float(points[0][1, 0])
                x2 = float(points[1][0, 0])
                y2 = float(points[1][1, 0])
                x3 = float(points[2][0, 0])
                y3 = float(points[2][1, 0])
                pg.draw.polygon(self.screen, triangle.color, [(x1, y1), (x2, y2), (x3, y3)])

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
                new_point = transform_matrix @ point
                for p in range(0, 3):
                    obj.points[idx][p] = new_point[p]

if __name__ == '__main__':
    app = GraphicsEngine((WINDOW_X_SIZE, WINDOW_Y_SIZE))
    app.run()