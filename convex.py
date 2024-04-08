from deq import Deq
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0


class Void(Figure):
    """ "Hульугольник" """

    def __init__(self, rect):
        self.__rect: ConstRect = rect

    def add(self, p):
        return Point(p, self.__rect)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p, rect):
        self.p: R2Point = p
        self.__rect: ConstRect = rect
        self._intersection_num: int = self.__rect.intersect_point(self.p)

    def intersection(self):
        return self._intersection_num

    def add(self, q):
        return self if self.p == q else Segment(self.p, q, self.__rect)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q, rect):
        self.p, self.q = p, q
        self.__rect: ConstRect = rect
        self._intersection_num = self.__rect.intersect_segment(self.p, self.q)

    def intersection(self):
        return self._intersection_num

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r, self.__rect,
                           self._intersection_num)
        elif self.q.is_inside(self.p, r):
            return Segment(self.p, r, self.__rect)
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q, self.__rect)
        else:
            return self


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c, rect, start_value: int | str):
        self.points = Deq()
        self.__rect: ConstRect = rect
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        self.inf_power = 0
        self._intersection_num: int = 0
        self.change_intersection(start_value, True)
        self.change_intersection(self.__rect.intersect_segment(b, c), True)
        self.change_intersection(self.__rect.intersect_segment(a, c), True)
        self.change_intersection(self.__rect.intersect_point(a), False)
        self.change_intersection(self.__rect.intersect_point(b), False)
        self.change_intersection(self.__rect.intersect_point(c), False)

    """правильный вывод пересечения"""
    def intersection(self):
        if self.inf_power > 0:
            return "inf"
        return self._intersection_num

    """безопасное изменение пересечения"""
    def change_intersection(self, value, adding: bool):
        if adding:
            if value == "inf":
                self.inf_power += 1
            else:
                self._intersection_num += value
        else:
            if value == "inf":
                self.inf_power -= 1
            else:
                self._intersection_num -= value

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    # добавление новой точки
    def add(self, t):
        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):
            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self.change_intersection(self.__rect.intersect_segment(
                self.points.first(), self.points.last()), False)
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))

            # удаление освещённых рёбер из начала дека + удаление пересечений
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self.change_intersection(self.__rect.intersect_segment(
                    p, self.points.first()), False)
                self.change_intersection(self.__rect.intersect_point(p), True)
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека + удаление пересечений
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self.change_intersection(self.__rect.intersect_segment(
                    p, self.points.last()), False)
                self.change_intersection(self.__rect.intersect_point(p), True)
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер + пересечений прямоугольника с ними
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())

            self.change_intersection(self.__rect.intersect_segment(
                t, self.points.first()), True)
            self.change_intersection(self.__rect.intersect_segment(
                t, self.points.last()), True)
            self.change_intersection(self.__rect.intersect_point(t), False)
            self.points.push_first(t)

        return self


class ConstSegment:
    def __init__(self, a: R2Point, b: R2Point):
        self.p1 = a
        self.p2 = b

    """пересечение проверяется посредством изучения образованных площадей,
    для 4х точек мы узнаем, по какую сторону отрезка лежит точка,
    отдельный случай совпадение отрезков -> бесконечно кол-во пересечений"""
    def is_intersect(self, other):
        s1 = R2Point.area(other.p1, self.p1, self.p2)
        s2 = R2Point.area(other.p2, self.p1, self.p2)
        s3 = R2Point.area(self.p1, other.p1, other.p2)
        s4 = R2Point.area(self.p2, other.p1, other.p2)
        if s1 == s2 == s3 == s4 == 0:
            return "inf"
        return s1 * s2 <= 0 and s3 * s4 <= 0

    '''если отрезок содержит точку, то площадь треугольника
    из этой точки и вершин отрезка == 0'''
    def has_point(self, p: R2Point):
        return R2Point.area(p, self.p1, self.p2) == 0 and \
            (self.p2.x <= p.x <= self.p1.x or
             self.p1.x <= p.x <= self.p2.x)\
            and (self.p2.y <= p.y <= self.p1.y or
                 self.p1.y <= p.y <= self.p2.y)


class ConstRect:
    def __init__(self, a: R2Point, b: R2Point):
        high = max(a.y, b.y)
        low = min(a.y, b.y)
        left = min(a.x, b.x)
        right = max(a.x, b.x)
        self.points = [R2Point(left, high), R2Point(left, low),
                       R2Point(right, low), R2Point(right, high)]
        self.segments = [ConstSegment(self.points[3], self.points[0]),
                         ConstSegment(self.points[0], self.points[1]),
                         ConstSegment(self.points[1], self.points[2]),
                         ConstSegment(self.points[2], self.points[3])]

    """количество пересечений точки с прямоугольником, т.е.
    принадлежит ли она его сторонам"""
    def intersect_point(self, point: R2Point) -> int:
        for s in self.segments:
            if s.has_point(point):
                return 1
        return 0

    """количество пересечений отрезка с прямоугольником, т.е
    количество пересечений четырех сторон с отрезком,
    в случае, когда отрезок попадает на угол прямоугольника,
    пересечение не должно учитывать два раза"""
    def intersect_segment(self, a: R2Point, b: R2Point):
        r = 0
        sub = 0
        segment = ConstSegment(a, b)
        for i in range(-1, 3):
            sub += segment.has_point(self.points[i])
            temp = segment.is_intersect(self.segments[i + 1])
            if temp == "inf":
                return "inf"
            r += temp
        return r - sub

    # """пересечение с оболочкой - несколько вариантов,
    # в зависимости от типа оболочки"""
    # def intersect_convex(self, convex):
    #     if type(convex) is Void:
    #         return 0
    #     if type(convex) is Point:
    #         return self.intersect_point(convex.p)
    #     if type(convex) is Segment:
    #         return self.intersect_segment(convex.p, convex.q)
    #     #
    #     r = 0
    #     sub = 0
    #     for i in range(-1, convex.points.size() - 1):
    #         '''если точка оболочки попадает на сторону прямоугольника,
    #         получается два пересечения - один отрезок и другой,
    #         поэтому кол-во таких точек надо вычесть из кол-ва пересечений'''
    #         sub += self.intersect_point(convex.points.at(i))
    #         temp = self.intersect_segment(
    #             convex.points.at(i),
    #             convex.points.at(i + 1))
    #         if temp == "inf":
    #             return temp
    #         r += temp
    #     return r - sub


if __name__ == "__main__":
    f = Void(None)
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
