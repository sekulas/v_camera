import numpy as np
import pygame as pg

BLACK = (0, 0, 0)

class Cube:
    def __init__(self, x, y, z, color, dist_to_camera, edge_len):
        self.points = []
        self.dist_to_camera = dist_to_camera
        self.edge_len = edge_len
        self.color = color

        self.__create_points(x, y, z)

    def __create_points(self, x, y, z): #TODO Use coordinates
        d = self.edge_len #todo by 2
        self.points.append(np.matrix([[-d + x], [-d + y], [d + self.dist_to_camera + z]], dtype=np.float16))
        self.points.append(np.matrix([[-d + x], [d + y], [d + self.dist_to_camera + z]], dtype=np.float16))
        self.points.append(np.matrix([[d + x], [d + y], [d + self.dist_to_camera + z]], dtype=np.float16))
        self.points.append(np.matrix([[d + x], [-d + y], [d + self.dist_to_camera + z]], dtype=np.float16))

        self.points.append(np.matrix([[-d + x], [-d + y], [d*3 + self.dist_to_camera + z]], dtype=np.float16))
        self.points.append(np.matrix([[-d + x], [d + y], [d*3 + self.dist_to_camera + z]], dtype=np.float16))
        self.points.append(np.matrix([[d + x], [d + y], [d*3 + self.dist_to_camera + z]], dtype=np.float16))
        self.points.append(np.matrix([[d + x], [-d + y], [d*3 + self.dist_to_camera + z]], dtype=np.float16))