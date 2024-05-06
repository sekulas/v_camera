import colorsys

class Point:
    def __init__(self, x, y, z, color):
        self.x = x
        self.y = y
        self.z = z
        self.origin_color = colorsys.rgb_to_hls(color[0]/255, color[1]/255, color[2]/255)
        self.color = color

    def change_color(self, color):
        self.origin_color = colorsys.rgb_to_hls(color[0]/255, color[1]/255, color[2]/255)
        self.color = color

    def change_illumination(self, new_illumination):
        if new_illumination<0:
            new_illumination=0
        elif new_illumination>1:
            new_illumination=1
        h = (self.origin_color[0],new_illumination,self.origin_color[2])
        c = colorsys.hls_to_rgb(*h)
        c = (c[0]*255,c[1]*255,c[2]*255)
        self.color = c
