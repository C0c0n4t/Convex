import unittest
from math import sqrt
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon


class TestVoid(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.f = Void()

    # Нульугольник является фигурой
    def test_figure(self):
        self.assertIsInstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Void (нульугольник)
    def test_void(self):
        self.assertIsInstance(self.f, Void)

    # Периметр нульугольника нулевой
    def test_perimeter(self):
        self.assertEqual(self.f.perimeter(), 0.0)

    # Площадь нульугольника нулевая
    def test_area(self):
        self.assertEqual(self.f.area(), 0.0)

    # При добавлении точки нульугольник превращается в одноугольник
    def test_add(self):
        self.assertIsInstance(self.f.add(R2Point(0.0, 0.0)), Point)


class TestPoint(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.f = Point(R2Point(0.0, 0.0))

    # Одноугольник является фигурой
    def test_figure(self):
        self.assertIsInstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Point (одноугольник)
    def test_point(self):
        self.assertIsInstance(self.f, Point)

    # Периметр одноугольника нулевой
    def test_perimeter(self):
        self.assertEqual(self.f.perimeter(), 0.0)

    # Площадь одноугольника нулевая
    def test_area(self):
        self.assertEqual(self.f.area(), 0.0)

    # При добавлении точки одноугольник может не измениться
    def test_add1(self):
        self.assertIs(self.f.add(R2Point(0.0, 0.0)), self.f)

    # При добавлении точки одноугольник может превратиться в двуугольник
    def test_add2(self):
        self.assertIsInstance(self.f.add(R2Point(1.0, 0.0)), Segment)


class TestSegment(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.f = Segment(R2Point(0.0, 0.0), R2Point(1.0, 0.0))

    # Двуугольник является фигурой
    def test_figure(self):
        self.assertIsInstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Segment (двуугольник)
    def test_segment(self):
        self.assertIsInstance(self.f, Segment)

    # Периметр двуугольника равен удвоенной длине отрезка
    def test_perimeter(self):
        self.assertAlmostEqual(self.f.perimeter(), 2.0)

    # Площадь двуугольника нулевая
    def test_area(self):
        self.assertEqual(self.f.area(), 0.0)

    # При добавлении точки двуугольник может не измениться
    def test_add1(self):
        self.assertIs(self.f.add(R2Point(0.5, 0.0)), self.f)

    # Он не изменяется в том случае, когда добавляемая точка совпадает
    # с одним из концов отрезка
    def test_add2(self):
        self.assertIs(self.f.add(R2Point(0.0, 0.0)), self.f)

    # При добавлении точки правее двуугольник может превратиться в другой
    # двуугольник
    def test_add3(self):
        self.assertIsInstance(self.f.add(R2Point(2.0, 0.0)), Segment)

    # При добавлении точки левее двуугольник может превратиться в другой
    # двуугольник
    def test_add4(self):
        self.assertIsInstance(self.f.add(R2Point(-1.0, 0.0)), Segment)

    # При добавлении точки двуугольник может превратиться в треугольник
    def test_add5(self):
        self.assertIsInstance(self.f.add(R2Point(0.0, 1.0)), Polygon)


class TestPolygon(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(0.0, 0.0)
        self.b = R2Point(1.0, 0.0)
        self.c = R2Point(0.0, 1.0)
        self.f = Polygon(self.a, self.b, self.c)

    # Многоугольник является фигурой
    def test_figure(self):
        self.assertIsInstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Polygon (многоугольник)
    def test_polygon1(self):
        self.assertIsInstance(self.f, Polygon)

    # Изменение порядка точек при создании объекта всё равно порождает Polygon
    def test_polygon2(self):
        self.f = Polygon(self.b, self.a, self.c)
        self.assertIsInstance(self.f, Polygon)

    # Изменение количества вершин многоугольника
    #   изначально их три
    def test_vertexes1(self):
        self.assertEqual(self.f.points.size(), 3)

    #   добавление точки внутрь многоугольника не меняет их количества
    def test_vertexes2(self):
        self.assertEqual(self.f.add(R2Point(0.1, 0.1)).points.size(), 3)

    #   добавление другой точки может изменить их количество
    def test_vertexes3(self):
        self.assertEqual(self.f.add(R2Point(1.0, 1.0)).points.size(), 4)

    #   изменения выпуклой оболочки могут и уменьшать их количество
    def test_vertexes4(self):
        d = R2Point(0.4, 1.0)
        e = R2Point(1.0, 0.4)
        f = R2Point(0.8, 0.9)
        g = R2Point(0.9, 0.8)
        self.assertEqual(self.f.add(d).add(e).add(f).add(g).points.size(), 7)
        self.assertEqual(self.f.add(R2Point(2.0, 2.0)).points.size(), 4)

    # Изменение периметра многоугольника
    #   изначально он равен сумме длин сторон
    def test_perimeter1(self):
        self.assertAlmostEqual(self.f.perimeter(), 2.0 + sqrt(2.0))

    #   добавление точки может его изменить
    def test_perimeter2(self):
        self.assertAlmostEqual(self.f.add(R2Point(1.0, 1.0)).perimeter(), 4.0)

    # Изменение площади многоугольника
    #   изначально она равна (неориентированной) площади треугольника
    def test_area1(self):
        self.assertAlmostEqual(self.f.area(), 0.5)

    #   добавление точки может увеличить площадь
    def test_area2(self):
        self.assertAlmostEqual(self.f.add(R2Point(1.0, 1.0)).area(), 1.0)
