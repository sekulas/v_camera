import numpy as np
import matrix_transformations

class Camera:
    def __init__(self, app):
        self.app = app
        self.zoom = 1
        self.step = 50
        self.rotationDegree = 0.05
        self.zoom_change = 0.5

    def move_up(self):
        translation_up = matrix_transformations.get_translation_matrix(0, self.step, 0)
        self.app.update_points(translation_up)

    def move_down(self):
        translation_down = matrix_transformations.get_translation_matrix(0, -self.step, 0)
        self.app.update_points(translation_down)

    def move_left(self):
        translation_left = matrix_transformations.get_translation_matrix(self.step, 0, 0)
        self.app.update_points(translation_left)

    def move_right(self):
        translation_right = matrix_transformations.get_translation_matrix(-self.step, 0, 0)
        self.app.update_points(translation_right)

    def move_forward(self):
        translation_forward = matrix_transformations.get_translation_matrix(0, 0, -self.step)
        self.app.update_points(translation_forward)

    def move_back(self):
        translation_back = matrix_transformations.get_translation_matrix(0, 0, self.step)
        self.app.update_points(translation_back)

    def rotate_left(self):
        rotation_left = matrix_transformations.get_rotation_y_matrix(self.rotationDegree)
        self.app.update_points(rotation_left)

    def rotate_right(self):
        rotation_right = matrix_transformations.get_rotation_y_matrix(-self.rotationDegree)
        self.app.update_points(rotation_right)
