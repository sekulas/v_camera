import colorsys

class Point:
    def __init__(self, x, y, z, color):
        self.x = x
        self.y = y
        self.z = z
        self.origin_color = color
        self.color = color

    def change_illumination(self, new_illumination):
        #new_illumination*=4
        if new_illumination<0:
            new_illumination=0
        elif new_illumination>1:
            new_illumination=1
        #new_illumination=1-new_illumination
        h = colorsys.rgb_to_hls(self.origin_color[0]/255,self.origin_color[1]/255,self.origin_color[2]/255)
        h=(h[0],new_illumination,h[2])
        c = colorsys.hls_to_rgb(*h)
        c = (c[0]*255,c[1]*255,c[2]*255)
        self.color = c
