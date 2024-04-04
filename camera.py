class Camera:
    def __init__(self, app):
        self.app = app
        self.zoom = 1
        self.step = 100
        self.rotationDegree = 100
        self.zoom_change = 0.5