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
        # Maybe opaque?
        #pre_light_vector = np.matrix([light[0]-point.x, light[1]-point.y, light[2]-point.z])
        pre_light_vector = np.matrix([point.x-light[0], point.y-light[1], point.z-light[2]])
        pre_camera_vector = np.matrix([camera[0]-point.x, camera[1]-point.y, camera[2]-point.z])
        #pre_reflection_vector = 2*np.dot(pre_light_vector, pre_surface_vector.T)*pre_surface_vector-pre_light_vector
        #reflected_camera = self.__project_point(point, light, pre_surface_vector)
        #pre_reflection_vector = np.matrix([reflected_camera[0]-point.x, reflected_camera[1]-point.y, reflected_camera[2]-point.z])
        #pre_reflection_vector = pre_surface_vector-pre_light_vector

        surface_vector = self.__calc_normal(pre_surface_vector)
        light_vector = self.__calc_normal(pre_light_vector)
        camera_vector = self.__calc_normal(pre_camera_vector)
        #reflection_vector = self.__calc_normal(pre_reflection_vector)
        reflection_vector = 2*np.dot(light_vector, surface_vector.T)*surface_vector-light_vector

        i = self.ambient-self.kd*np.dot(surface_vector, light_vector.T)+self.ks*np.dot(reflection_vector, camera_vector.T)**self.n
        point.change_illumination(i.item((0,0)))
        return i.item((0,0))


    def __project_point(self, start_point, point, vector):
        d = (point[0] * vector.item((0, 0)) + point[1] * vector.item((0, 1)) + point[2] * vector.item((0, 2)))
        dd = d-(vector.item((0, 0))+start_point.x+vector.item((0, 1))+start_point.y+vector.item((0, 2))+start_point.z)
        t = dd/(vector.item((0, 0))*vector.item((0, 0))+vector.item((0, 1))*vector.item((0, 1))+vector.item((0, 2))*vector.item((0, 2)))
        p = (start_point.x+point[0] + vector.item((0, 0)) * t, start_point.y+point[1] + vector.item((0, 1)) * t, start_point.z+point[2] + vector.item((0, 2)) * t)
        e = (2*p[0]-point[0], 2*p[1]-point[1], 2*p[2]-point[2])
        return e


    def __calc_dist(self,point_a,point_b):
        dist = math.sqrt((point_b[0]-point_a[0])**2+(point_b[1]-point_a[1])**2+(point_b[2]-point_a[2])**2)
        return dist


    def __calc_normal(self, vector):
        row_sums = self.__calc_norm(vector)
        return vector / row_sums


    def __calc_angle(self, vector_a,vector_b):
        ab = np.dot(vector_a, vector_b)
        a = self.__calc_norm(vector_a)
        b = self.__calc_norm(vector_b)
        return math.acos(ab/(a*b))


    def __calc_cos(self, vector_a,vector_b):
        ab = np.dot(vector_a, vector_a.T).item((0,0))
            #vector_a[0].item((0, 0))*vector_b[0].item((0, 0))+vector_a[0].item((0, 1))*vector_b[0].item((0, 1))+vector_a[0].item((0, 2))*vector_b[0].item((0, 2))
        a = self.__calc_norm(vector_a)
        b = self.__calc_norm(vector_b)
        return ab/(a*b)
        #return (a*b)/ab


    def __calc_norm(self,vector):
        return math.sqrt(vector[0].item((0, 0))**2+vector[0].item((0, 1))**2+vector[0].item((0, 2))**2)
