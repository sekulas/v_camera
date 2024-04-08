import numpy as np
import matrix_transformations as mt

class Line:
    def __init__(self, a: np.matrix, b: np.matrix):
        self.a = a
        self.b = b

    def clip(self):
        if np.sign(self.a[2,0]) != np.sign(self.b[2,0]):
            if self.a[2,0] < 0:
                return Line(np.matrix([[self.a[0,0]], [self.a[1,0]], [0], [1]], dtype=np.float64), self.b)
            else:
                return Line(self.a, np.matrix([[self.b[0,0]], [self.b[1,0]], [0], [1]], dtype=np.float64))
        return self

    def project_3d_to_2d(self, focal_len, window_x_size, window_y_size):
        z1 = self.a[2, 0]
        z2 = self.b[2, 0]

        x1 = np.float64(self.a[0, 0]) * focal_len / z1 + window_x_size / 2
        y1 = np.float64(self.a[1, 0]) * focal_len / z1 + window_y_size / 2
        x2 = np.float64(self.b[0, 0]) * focal_len / z2 + window_x_size / 2
        y2 = np.float64(self.b[1, 0]) * focal_len / z2 + window_y_size / 2

        proj_a = np.matrix([[x1], [y1]], dtype=np.float64)
        proj_b = np.matrix([[x2], [y2]], dtype=np.float64)

        return Line(proj_a, proj_b)