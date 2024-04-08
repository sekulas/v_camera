import numpy as np
import matrix_transformations as mt

class Line:
    def __init__(self, a: np.matrix, b: np.matrix):
        self.a = a
        self.b = b

    def clip(self):
        if np.sign(self.a[2,0]) != np.sign(self.b[2,0]):
            #dx = self.b[0,0] - self.a[0,0]
            #dy = self.b[1,0] - self.a[1,0]
            #dz = self.b[2,0] - self.a[2,0]
            #y = np.float64(-dy * (self.a[2,0] - 1)) / dz + self.a[1,0]
            #x = np.float64(-dx * (self.a[2,0] - 1)) / dz + self.a[0,0]
            if self.a[2,0] < 0:
                return Line(np.matrix([[self.a[0,0]], [self.a[1,0]], [0], [1]], dtype=np.float64), self.b)
            else:
                return Line(self.a, np.matrix([[self.b[0,0]], [self.b[1,0]], [0], [1]], dtype=np.float64))
        return self

    def scale(self, zoom):
        print("SKALOWANIE")
        print(self.a)
        point_a = mt.get_zoom_matrix(zoom) @ self.a
        point_b = mt.get_zoom_matrix(zoom) @ self.b
        print(point_a)
        return Line(point_a, point_b)

    def project_3d_to_2d(self, focal_len):
        z1 = self.a[2, 0]
        z2 = self.b[2, 0]

        x1 = np.float64(self.a[0, 0]) * focal_len / z1 
        y1 = np.float64(self.a[1, 0]) * focal_len / z1 
        x2 = np.float64(self.b[0, 0]) * focal_len / z2 
        y2 = np.float64(self.b[1, 0]) * focal_len / z2 

        proj_a = np.matrix([[x1], [y1], [z1]], dtype=np.float64)
        proj_b = np.matrix([[x2], [y2], [z2]], dtype=np.float64)

        return Line(proj_a, proj_b)