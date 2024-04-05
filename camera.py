import numpy as np
import matrix_transformations

class Camera:
    def __init__(self, app):
        self.app = app
        self.zoom = 1
        self.step = 1
        self.rotationDegree = 100
        self.zoom_change = 0.5

    def move_up(self):
        translation_up = matrix_transformations.get_translation_matrix(0, self.step, 0)
        for obj in self.app.objects:
            for idx, point in enumerate(obj.points):
                new_point = np.dot(translation_up, point)
                
                for p in range(0, 3):
                    obj.points[idx][p] = new_point[p]