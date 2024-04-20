import math
import cProfile
import pygame as pg
import numpy as np
from camera import Camera
from objects.cube import Cube
# from bsp import BSPNode
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
devider = 2

WINDOW_X_SIZE = int(800/devider)
WINDOW_Y_SIZE = int(600/devider)

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
    def __init__(self, win_size=(int, int)):
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
                        Cube(-DIST_FROM_CENTER, -DIST_FROM_CENTER, -DIST_FROM_CENTER, ORANGE, MIN_FOCAL_LEN / 2), ]

        self.camera = Camera(self)
        self.z_buffer = []
        self.focal_len = 1000

    def check_events(self):
        click = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    if self.focal_len <= MAX_FOCAL_LEN:
                        self.focal_len += 100
                        click = True
                if event.key == pg.K_x:
                    if self.focal_len >= MIN_FOCAL_LEN:
                        self.focal_len -= 100
                        click = True

        keys = pg.key.get_pressed()

        if keys[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()
        if keys[pg.K_SPACE]:
            self.camera.move_up()
            click = True
        if keys[pg.K_LSHIFT]:
            self.camera.move_down()
            click = True
        if keys[pg.K_d]:
            self.camera.move_right()
            click = True
        if keys[pg.K_a]:
            self.camera.move_left()
            click = True
        if keys[pg.K_w]:
            self.camera.move_forward()
            click = True
        if keys[pg.K_s]:
            self.camera.move_back()
            click = True

        if keys[pg.K_q]:
            self.camera.rotate_left()
            click = True
        if keys[pg.K_e]:
            self.camera.rotate_right()
            click = True
        if keys[pg.K_u]:
            self.camera.rotate_up()
            click = True
        if keys[pg.K_i]:
            self.camera.rotate_down()
            click = True
        if keys[pg.K_o]:
            self.camera.rotate_clockwise()
            click = True
        if keys[pg.K_p]:
            self.camera.rotate_counter_clockwise()
            click = True

        if keys[pg.K_EQUALS]:
            if self.focal_len <= MAX_FOCAL_LEN:
                self.focal_len += 100
                click = True
        if keys[pg.K_MINUS]:
            if self.focal_len >= MIN_FOCAL_LEN:
                self.focal_len -= 100
                click = True

        return click

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

    def draw_z_buffer(self):
        self.screen.fill(WHITE)
        self.z_buffer = [[math.inf for j in range(WINDOW_X_SIZE+1)] for i in range(WINDOW_Y_SIZE)]
        all_triangles = []

        for obj in self.objects:
            all_triangles.extend(obj.triangles)

        all_triangles.sort(key=lambda tri: (tri.a[2, 0] + tri.b[2, 0] + tri.c[2, 0]) / 3)
        iter=0
        iter2=0
        seek =63
        seek2=20

        for triangle in all_triangles:
            if iter>seek:
                print(triangle.color)
            # a b c
            points_abc = [GraphicsEngine.project_point_3d_to_2d(point, self.focal_len, WINDOW_X_SIZE, WINDOW_Y_SIZE) \
                          for point in triangle.points]

            points_to_draw = self.get_point_inside_triangle(points_abc)
            for point in points_to_draw:
                self.screen.set_at((point[0], point[1]), triangle.color)

    def get_point_inside_triangle(self, points):
        z_const = points[0].item((2, 0)) == points[1].item((2, 0)) == points[2].item((2, 0))

        if z_const and points[0].item((2, 0)) > 0:
            z = points[0].item((2, 0))
            get_z = lambda zx, zy: z
        elif not z_const:
            # Get plane
            AB = np.array(points[1] - points[0]).T
            AC = np.array(points[2] - points[0]).T
            plane = np.cross(AB, AC)
            k = -(plane.item((0, 0)) * points[0].item((0, 0)) + plane.item((0, 1)) * points[0].item(
                (1, 0)) + plane.item(
                (0, 2)) * points[0].item((2, 0)))
            plane = plane.tolist()[0]
            plane.append(k)
            if plane[2] == 0:
                return
            get_z = lambda zx, zy: (-plane[0] * zx - plane[1] * zy - plane[3]) / plane[2]
        else:
            return

        # range generator
        points.sort(key=lambda p: (p.item((1, 0)), p.item((0, 0))))

        y_range_min1 = self.my_ceil(min(max(points[0].item((1, 0)), 0), WINDOW_Y_SIZE))
        y_range_max1 = self.my_ceil(min(max(points[1].item((1, 0)), 0), WINDOW_Y_SIZE))
        y_range_min2 = self.my_ceil(min(max(points[1].item((1, 0)), 0), WINDOW_Y_SIZE))
        y_range_max2 = self.my_ceil(min(max(points[2].item((1, 0)), 0), WINDOW_Y_SIZE))

        if points[0].item(0, 0) - points[1].item(0, 0) == 0:
            x1 = int(points[0].item(0, 0))
            f1 = lambda yy: [x1]
        elif points[0].item(1, 0) - points[1].item(1, 0) == 0:
            x11 = int(points[0].item(0, 0))
            x12 = int(points[1].item(0, 0))
            f1 = lambda yy: [x11, x12]
        else:
            a1 = (points[0].item(1, 0) - points[1].item(1, 0)) / (points[0].item(0, 0) - points[1].item(0, 0))
            b1 = points[0].item(1, 0) - a1 * points[0].item(0, 0)
            f1 = lambda yy: [int((yy - b1) / a1)]

        if points[0].item(0, 0) - points[2].item(0, 0) == 0:
            x2 = int(points[0].item(0, 0))
            f2 = lambda yy: [x2]
        elif points[0].item(1, 0) - points[2].item(1, 0) == 0:
            x21 = int(points[0].item(0, 0))
            x22 = int(points[2].item(0, 0))
            f2 = lambda yy: [x21, x22]
        else:
            a2 = (points[0].item(1, 0) - points[2].item(1, 0)) / (points[0].item(0, 0) - points[2].item(0, 0))
            b2 = points[0].item(1, 0) - a2 * points[0].item(0, 0)
            f2 = lambda yy: [int((yy - b2) / a2)]

        if points[1].item(0, 0) - points[2].item(0, 0) == 0:
            x3 = int(points[1].item(0, 0))
            f3 = lambda yy: [x3]
        elif points[1].item(1, 0) - points[2].item(1, 0) == 0:
            x31 = int(points[1].item(0, 0))
            x32 = int(points[2].item(0, 0))
            f3 = lambda yy: [x31, x32]
        else:
            a3 = (points[1].item(1, 0) - points[2].item(1, 0)) / (points[1].item(0, 0) - points[2].item(0, 0))
            b3 = points[1].item(1, 0) - a3 * points[1].item(0, 0)
            f3 = lambda yy: [int((yy - b3) / a3)]

        for y in range(y_range_min1, y_range_max1):
            x_range_start = min(max(min(f1(y)), 0), WINDOW_X_SIZE)
            x_range_end = min(max(max(f2(y)), 0), WINDOW_X_SIZE)
            if x_range_start>x_range_end:
                tmp = x_range_end
                x_range_end = x_range_start
                x_range_start = tmp
            for x in range(x_range_start, x_range_end):
                z = get_z(x, y)
                if self.z_buffer[y][x] > z > 0:
                    self.z_buffer[y][x] = z
                    yield [x, y, z]

        for y in range(y_range_min2, y_range_max2):
            x_range_start = min(max(min(f3(y)), 0), WINDOW_X_SIZE)
            x_range_end = min(max(max(f2(y)), 0), WINDOW_X_SIZE)
            if x_range_start>x_range_end:
                tmp = x_range_end
                x_range_end = x_range_start
                x_range_start = tmp
            for x in range(x_range_start, x_range_end):
                z = get_z(x, y)
                if self.z_buffer[y][x] > z > 0:
                    self.z_buffer[y][x] = z
                    yield [x, y, z]

    def my_ceil(self, num):
        r=num-num//1
        if r>0.01:
            return int(math.ceil(num))
        else:
            return int(math.floor(num))

    def render(self):
        pg.display.flip()

    def run(self):
        self.draw_z_buffer()
        self.render()
        while True:
            if self.check_events():
                self.draw_z_buffer()
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
    cProfile.run("app.run()")
    # app.run()
