import numpy as np

class Phong:
    def __init__(self, engine, ia, ka, ip, kd, ks, material, n):
        self.engine = engine
        self.ia = ia
        self.ka = ka
        self.ip = ip
        self.kd = kd
        self.ks = ks
        self.material = material
        self.n = n

    def calc_light_reflection(self, point):

        N = self.calc_normal_vec(point)
        diffusion = np.dot(N, L)
        specular = np.dot(R, V)        

        i = (self.ia * self.ka) + (diffusion * self.ip) * (self.kd * dot + self.ks * specular**self.n)
        return i
    
    def __calc_normal(self, point):
        

    def __calc_normal_vec