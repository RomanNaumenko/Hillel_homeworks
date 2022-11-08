import unittest
from coord import Coord, line_length


class TestLineLength(unittest.TestCase):
    a = Coord(3, 3)
    b1 = Coord(1, 1)
    b2 = Coord(5, 1)
    b3 = Coord(5, 5)
    b4 = Coord(1, 5)
    b5 = Coord(3, 0)
    b6 = Coord(7, 3)
    b7 = Coord(3, 7)
    b8 = Coord(0, 3)
    b9 = Coord(-6, 7)
    b10 = Coord(-6, -7)
    b11 = Coord(6, 7)

    def test_ut1(self):
        self.assertEqual(line_length(self.a, self.b1), 5.66)

    def test_ut2(self):
        self.assertEqual(line_length(self.a, self.b2), 8.94)

    def test_ut3(self):
        self.assertEqual(line_length(self.a, self.b3), 11.31)

    def test_ut4(self):
        self.assertEqual(line_length(self.a, self.b4), 8.94)

    def test_ut5(self):
        self.assertEqual(line_length(self.a, self.b5), 6.71)

    def test_ut6(self):
        self.assertEqual(line_length(self.a, self.b6), 11.66)

    def test_ut7(self):
        self.assertEqual(line_length(self.a, self.b7), 11.66)

    def test_ut8(self):
        self.assertEqual(line_length(self.a, self.b8), 6.71)

    def test_ut9(self):
        self.assertEqual(line_length(self.a, self.b9), 10.44)

    def test_ut10(self):
        self.assertEqual(line_length(self.a, self.b10), 5)

    def test_ut11(self):
        self.assertEqual(line_length(self.a, self.b11), 13.45)
