import numpy as np
import pygame as pg
from objects.line import Line

BLACK = (0, 0, 0)

class Cube:
    def __init__(self, x, y, z, color, focal_len, edge_len = 150):
        self.points = []
        self.lines = []
        self.focal_len = focal_len
        self.edge_len = edge_len
        self.color = color

        self.__create_points(x, y, z)
        self.__init_lines()

    def __create_points(self, x, y, z):
        d = self.edge_len / 2
        self.points.append(np.matrix([[-d + x], [-d + y], [d + self.focal_len + z], [1]], dtype=np.float64))
        self.points.append(np.matrix([[-d + x], [d + y], [d + self.focal_len + z], [1]], dtype=np.float64))
        self.points.append(np.matrix([[d + x], [d + y], [d + self.focal_len + z], [1]], dtype=np.float64))
        self.points.append(np.matrix([[d + x], [-d + y], [d + self.focal_len + z], [1]], dtype=np.float64))

        self.points.append(np.matrix([[-d + x], [-d + y], [d*3 + self.focal_len + z], [1]], dtype=np.float64))
        self.points.append(np.matrix([[-d + x], [d + y], [d*3 + self.focal_len + z], [1]], dtype=np.float64))
        self.points.append(np.matrix([[d + x], [d + y], [d*3 + self.focal_len + z], [1]], dtype=np.float64))
        self.points.append(np.matrix([[d + x], [-d + y], [d*3 + self.focal_len + z], [1]], dtype=np.float64))

    def __init_lines(self):
        for i in range(0, 3):
            self.lines.append(Line(self.points[i], self.points[i + 1]))
            self.lines.append(Line(self.points[i + 4], self.points[i + 5]))
            self.lines.append(Line(self.points[i], self.points[i + 4]))

        self.lines.append(Line(self.points[0], self.points[3]))
        self.lines.append(Line(self.points[4], self.points[7]))
        self.lines.append(Line(self.points[3], self.points[7]))