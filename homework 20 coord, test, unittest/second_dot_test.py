from coord import Coord, line_length


def test_a1():
    a1 = Coord(4, 4)
    a2 = Coord(8, 8)
    assert line_length(a1, a2) == 16.97


def test_a2():
    a1 = Coord(8, 4)
    a2 = Coord(8, 8)
    assert line_length(a1, a2) == 20


def test_a3():
    a1 = Coord(12, 4)
    a2 = Coord(8, 8)
    assert line_length(a1, a2) == 23.32


def test_a4():
    a1 = Coord(12, 8)
    a2 = Coord(8, 8)
    assert line_length(a1, a2) == 25.61


def test_a5():
    a1 = Coord(12, 12)
    a2 = Coord(8, 8)
    assert line_length(a1, a2) == 28.28


def test_a6():
    a1 = Coord(8, 12)
    a2 = Coord(8, 8)
    assert line_length(a1, a2) == 25.61


def test_a7():
    a1 = Coord(4, 12)
    a2 = Coord(8, 8)
    assert line_length(a1, a2) == 23.32


def test_a8():
    a1 = Coord(4, 8)
    a2 = Coord(8, 8)
    assert line_length(a1, a2) == 20


def test_a9():
    a1 = Coord(-8, 8)
    a2 = Coord(8, 8)
    assert line_length(a1, a2) == 16


def test_a10():
    a1 = Coord(-8, -8)
    a2 = Coord(8, 8)
    assert line_length(a1, a2) == 0


def test_a11():
    a1 = Coord(8, -8)
    a2 = Coord(8, 8)
    assert line_length(a1, a2) == 16