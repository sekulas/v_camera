import matrix_transformations as mt

class Camera:
    def __init__(self, app):
        self.app = app
        # self.step = 5
        self.step = 50
        self.rotationDegree = 0.15

    def move_up(self):
        translation_up = mt.get_translation_matrix(0, self.step, 0)
        self.app.update_points(translation_up)

    def move_down(self):
        translation_down = mt.get_translation_matrix(0, -self.step, 0)
        self.app.update_points(translation_down)

    def move_left(self):
        translation_left = mt.get_translation_matrix(self.step, 0, 0)
        self.app.update_points(translation_left)

    def move_right(self):
        translation_right = mt.get_translation_matrix(-self.step, 0, 0)
        self.app.update_points(translation_right)

    def move_forward(self):
        translation_forward = mt.get_translation_matrix(0, 0, -self.step)
        self.app.update_points(translation_forward)

    def move_back(self):
        translation_back = mt.get_translation_matrix(0, 0, self.step)
        self.app.update_points(translation_back)

    def rotate_left(self):
        rotation_left = mt.get_rotation_y_matrix(self.rotationDegree)
        self.app.update_points(rotation_left)

    def rotate_right(self):
        rotation_right = mt.get_rotation_y_matrix(-self.rotationDegree)
        self.app.update_points(rotation_right)

    def rotate_up(self):
        rotate_up = mt.get_rotation_x_matrix(self.rotationDegree)
        self.app.update_points(rotate_up)
    
    def rotate_down(self):
        rotate_down = mt.get_rotation_x_matrix(-self.rotationDegree)
        self.app.update_points(rotate_down)
    
    def rotate_clockwise(self):
        rotate_clockwise = mt.get_rotation_z_matrix(self.rotationDegree)
        self.app.update_points(rotate_clockwise)
    
    def rotate_counter_clockwise(self):
        rotate_counter_clockwise = mt.get_rotation_z_matrix(-self.rotationDegree)
        self.app.update_points(rotate_counter_clockwise)