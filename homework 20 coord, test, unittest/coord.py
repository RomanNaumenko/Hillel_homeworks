import math


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Coords are next: x = {self.x}, y = {self.y}"


def line_length(point1, point2):
    return round(math.sqrt((point1.x + point2.x) ** 2 + (point1.y + point2.y) ** 2), 2)


a1 = Coord(1, 2)
a2 = Coord(3, 4)
a3 = a1 + a2
print(a3)

print(line_length(a1, a2))