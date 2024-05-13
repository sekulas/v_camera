import math

import numpy as np

class Phong:
    def __init__(self, engine, ambient, kd, ks, material, n):
        self.engine = engine
        self.ambient = ambient
        self.kd = kd
        self.ks = ks
        self.material = material
        self.n = n

    def calc_light_reflection(self, point):
        light = self.engine.light
        camera = self.engine.camera_position

        pre_surface_vector = np.matrix([point.x, point.y, point.z])
        pre_light_vector = np.matrix([point.x-light[0], point.y-light[1], point.z-light[2]])
        pre_camera_vector = np.matrix([camera[0]-point.x, camera[1]-point.y, camera[2]-point.z])

        surface_vector = self.__calc_normal(pre_surface_vector)
        light_vector = self.__calc_normal(pre_light_vector)
        camera_vector = self.__calc_normal(pre_camera_vector)
        reflection_vector = 2*np.dot(light_vector, surface_vector.T)*surface_vector-light_vector

        res_cos=np.dot(reflection_vector, camera_vector.T)
        if res_cos>0:
            r=0
        else:
            r=self.ks*res_cos**self.n

        i = self.ambient-self.kd*np.dot(surface_vector, light_vector.T)+r
        point.change_illumination(i.item((0,0)))

    def __calc_normal(self, vector):
        row_sums = self.__calc_norm(vector)
        return vector / row_sums

    @staticmethod
    def __calc_norm(vector):
        return math.sqrt(vector[0].item((0, 0))**2+vector[0].item((0, 1))**2+vector[0].item((0, 2))**2)
