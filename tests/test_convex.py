from pytest import approx
from math import sqrt
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon, ConstRect


class TestVoid:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Void(ConstRect(
            R2Point(1, 1), R2Point(1, 1)))

    # Нульугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Void (нульугольник)
    def test_void(self):
        assert isinstance(self.f, Void)

    # Периметр нульугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь нульугольника нулевая
    def test_area(self):
        assert self.f.area() == 0.0

    # При добавлении точки нульугольник превращается в одноугольник
    def test_add(self):
        assert isinstance(self.f.add(R2Point(0.0, 0.0)), Point)


class TestPoint:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Point(R2Point(0.0, 0.0), ConstRect(
            R2Point(1, 1), R2Point(1, 1)))

    # Одноугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Point (одноугольник)
    def test_point(self):
        assert isinstance(self.f, Point)

    # Периметр одноугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь одноугольника нулевая
    def test_area(self):
        assert self.f.area() == 0.0

    # При добавлении точки одноугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.0, 0.0)) is self.f

    # При добавлении точки одноугольник может превратиться в двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(1.0, 0.0)), Segment)


class TestSegment:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Segment(R2Point(0.0, 0.0), R2Point(1.0, 0.0), ConstRect(
            R2Point(1, 1), R2Point(1, 1)))

    # Двуугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Segment (двуугольник)
    def test_segment(self):
        assert isinstance(self.f, Segment)

    # Периметр двуугольника равен удвоенной длине отрезка
    def test_perimeter(self):
        assert self.f.perimeter() == approx(2.0)

    # Площадь двуугольника нулевая
    def test_area(self):
        assert self.f.area() == 0.0

    # При добавлении точки двуугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.5, 0.0)) is self.f

    # При добавлении точки правее двуугольник может превратиться в другой
    # двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(2.0, 0.0)), Segment)

    # При добавлении точки левее двуугольник может превратиться в другой
    # двуугольник
    def test_add3(self):
        assert isinstance(self.f.add(R2Point(-1.0, 0.0)), Segment)

    # При добавлении точки двуугольник может превратиться в треугольник
    def test_add4(self):
        assert isinstance(self.f.add(R2Point(0.0, 1.0)), Polygon)


class TestPolygon:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.a = R2Point(0.0, 0.0)
        self.b = R2Point(1.0, 0.0)
        self.c = R2Point(0.0, 1.0)
        self.f = Polygon(self.a, self.b, self.c, ConstRect(
            R2Point(1, 1), R2Point(1, 1)), 0)

    # Многоугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Polygon (многоугольник)
    def test_polygon1(self):
        assert isinstance(self.f, Polygon)

    # Изменение порядка точек при создании объекта всё равно порождает Polygon
    def test_polygon2(self):
        self.f = Polygon(self.b, self.a, self.c, ConstRect(
            R2Point(1, 1), R2Point(1, 1)), 0)
        assert isinstance(self.f, Polygon)

    # Изменение количества вершин многоугольника
    #   изначально их три
    def test_vertexes1(self):
        assert self.f.points.size() == 3
    #   добавление точки внутрь многоугольника не меняет их количества

    def test_vertexes2(self):
        assert self.f.add(R2Point(0.1, 0.1)).points.size() == 3
    #   добавление другой точки может изменить их количество

    def test_vertexes3(self):
        assert self.f.add(R2Point(1.0, 1.0)).points.size() == 4
    #   изменения выпуклой оболочки могут и уменьшать их количество

    def test_vertexes4(self):
        assert self.f.add(
            R2Point(
                0.4,
                1.0)).add(
            R2Point(
                1.0,
                0.4)).add(
                    R2Point(
                        0.8,
                        0.9)).add(
                            R2Point(
                                0.9,
                                0.8)).points.size() == 7
        assert self.f.add(R2Point(2.0, 2.0)).points.size() == 4

    # Изменение периметра многоугольника
    #   изначально он равен сумме длин сторон
    def test_perimeter1(self):
        assert self.f.perimeter() == approx(2.0 + sqrt(2.0))
    #   добавление точки может его изменить

    def test_perimeter2(self):
        assert self.f.add(R2Point(1.0, 1.0)).perimeter() == approx(4.0)

    # Изменение площади многоугольника
    #   изначально она равна (неориентированной) площади треугольника
    def test_area1(self):
        assert self.f.area() == approx(0.5)
    #   добавление точки может увеличить площадь

    def test_area2(self):
        assert self.f.add(R2Point(1.0, 1.0)).area() == approx(1.0)


class TestIntersection:
    @staticmethod
    def check(data, results_m, rect):
        f = Void(rect)
        for i in range(len(data)):
            f = f.add(R2Point(data[i][0], data[i][1]))
            assert results_m[i] == f.intersection()

    def test_inter1(self):
        # точки оболочки
        data = [[1, 0], [1, 1], [2, 4], [-3, 2], [-3, -3]]
        # мощность множества пересечения
        results_m = [1, 'inf', 'inf', 2, 2]
        # прямоугольник
        rect = ConstRect(R2Point(1, 1), R2Point(-1, -1))
        self.check(data, results_m, rect)

    def test_inter2(self):
        data = [[-1.78, 0.16], [-0.18, 1.42], [1.32, 0.4], [1.34, -0.32],
                [1.28, -0.78], [0.22, -1.52], [1.52, -1.88],
                [-1.96, -1.76], [-1.62, 2.2], [1.7, 1.76]]
        results_m = [0, 2, 6, 6, 6, 8, 6, 4, 2, 0]
        rect = ConstRect(R2Point(1, 1), R2Point(-1, -1))
        self.check(data, results_m, rect)

    def test_inter3(self):
        data = [[-2.88, 1.5], [-1.06, 0.72], [-0.42, -1.64],
                [-2.92, -1.84], [2.2, 1.9], [2.48, -1.54]]
        results_m = [0, 1, 4, 2, 2, 0]
        rect = ConstRect(R2Point(1, 1), R2Point(-2, -1))
        self.check(data, results_m, rect)

    def test_inter4(self):
        data = [[-3.62, 0.94], [-1.92, -1.16], [-0.1, -0.68],
                [-0.62, 0.24], [-0.94, 1.44], [-0.7, 3.78],
                [1.68, 3.42], [1.66, -1.6]]
        results_m = [0, 0, 2, 2, 2, 4, 4, 2]
        rect = ConstRect(R2Point(1, 3), R2Point(-2, -1))
        self.check(data, results_m, rect)

    def test_inter5(self):
        data = [[-1.9, 2.0], [1.74, 2.0], [0.02, -0.36], [-1.16, -0.82],
                [1.48, -0.82], [-0.06, -3.36], [-4.4, -2.24],
                [-2.4, 3.28], [3.54, 2.66], [3.44, -1.98]]
        results_m = [1, 'inf', 'inf', 'inf', 'inf', 'inf', 'inf', 2, 2, 0]
        rect = ConstRect(R2Point(2, 2), R2Point(-2, -2))
        self.check(data, results_m, rect)

    def test_inter6(self):
        data = [[0, 2], [-2, 0], [0, -2], [2, 0], [4, 0]]
        results_m = [1, 2, 3, 4, 5]
        rect = ConstRect(R2Point(2, 2), R2Point(-2, -2))
        self.check(data, results_m, rect)

    def test_inter7(self):
        data = [[1, 1], [2, 2], [-2, -2], [0, -2], [-1, -4], [-6, 3]]
        results_m = [0, 1, 2, "inf", 3, 2]
        rect = ConstRect(R2Point(2, 2), R2Point(-2, -2))
        self.check(data, results_m, rect)

    def test_inter8(self):
        data = [[2, 2], [-2, 2], [-2, -2], [2, -2], [3, -3], [-3, 3]]
        results_m = [1, "inf", "inf", "inf", "inf", 2]
        rect = ConstRect(R2Point(2, 2), R2Point(-2, -2))
        self.check(data, results_m, rect)
