import numpy as np

def get_rotation_x_matrix(radians):
    sin = np.sin(radians)
    cos = np.cos(radians)

    matrix = np.matrix([
        [1, 0, 0, 0],
        [0, cos, -sin, 0],
        [0, sin, cos, 0]
        [0, 0, 0, 1]
    ])

    return matrix

def get_rotation_y_matrix(radians):
    sin = np.sin(radians)
    cos = np.cos(radians)

    matrix = np.matrix([
        [cos, 0, sin, 0],
        [0, 1, 0, 0],
        [-sin, 0, cos, 0],
        [0, 0, 0, 1]
    ])

    return matrix

def get_rotation_z_matrix(radians):
    sin = np.sin(radians)
    cos = np.cos(radians)

    matrix = np.matrix([
        [cos, -sin, 0, 0],
        [sin, cos, 0, 0],
        [0, 0, 1, 0]
        [0, 0, 0, 1]
    ])

    return matrix

def get_translation_matrix(step_x, step_y, step_z):
    matrix = np.matrix([
        [1, 0, 0, step_x],
        [0, 1, 0, step_y],
        [0, 0, 1, step_z],
        [0, 0, 0, 1]
    ])

    return matrix