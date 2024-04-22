from objects.line import Line

BLACK = (0, 0, 0)

class Triangle(object):
    def __init__(self, a, b, c, color=BLACK):
        self.a = a
        self.b = b
        self.c = c
        self.color = color
        self.lines = []
        self.points = [a, b, c]

        self.__init_lines()

    def __init_lines(self):
        lines = [Line(self.a, self.b), Line(self.b, self.c), Line(self.c, self.a)]
        self.lines = lines