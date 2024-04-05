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
                point_homogeneous = np.vstack((point, np.array([[1]])))
                new_point_homogeneous = np.dot(translation_up, point_homogeneous)
                obj.points[idx] = new_point_homogeneous[:-1]
            obj.update_lines()