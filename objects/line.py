import numpy as np

class Line:
    def __init__(self, a: np.matrix, b: np.matrix):
        self.a = a
        self.b = b

    def project_3d_to_2d(self, focal_len):
        z1 = self.a[2, 0]
        z2 = self.b[2, 0]

        if abs(z1) < 1e-6 or abs(z2) < 1e-6:
            return None

        x1 = np.float16(self.a[0, 0]) * focal_len / z1 
        y1 = np.float16(self.a[1, 0]) * focal_len / z1 
        x2 = np.float16(self.b[0, 0]) * focal_len / z2 
        y2 = np.float16(self.b[1, 0]) * focal_len / z2 

        proj_a = np.matrix([[x1], [y1], [z1], [1]], dtype=np.float16)
        proj_b = np.matrix([[x2], [y2], [z2], [1]], dtype=np.float16)

        return Line(proj_a, proj_b)