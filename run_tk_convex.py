#!/usr/bin/env -S python3 -B
from tk_drawer import TkDrawer
from r2point import R2Point
from convex import Void, Point, Segment, Polygon, ConstRect


def void_draw(self, tk):
    pass


def point_draw(self, tk):
    tk.draw_point(self.p)


def segment_draw(self, tk):
    tk.draw_line(self.p, self.q)


def polygon_draw(self, tk):
    for n in range(self.points.size()):
        tk.draw_line(self.points.last(), self.points.first())
        self.points.push_last(self.points.pop_first())


setattr(Void, 'draw', void_draw)
setattr(Point, 'draw', point_draw)
setattr(Segment, 'draw', segment_draw)
setattr(Polygon, 'draw', polygon_draw)


# Размер окна
SIZE = 600
# Коэффициент гомотетии
SCALE = 50


# перевод экранных координат в нормальные
def from_screen_y(y):
    return (-y + SIZE / 2) / SCALE


# перевод экранных координат в нормальные
def from_screen_x(x):
    return (x - SIZE / 2) / SCALE


# отрисовка прямоугольника
def draw_rect():
    for p in rect.segments:
        tk.draw_line(p.p1, p.p2)


def add_point(event):
    global f, tk
    x, y = event.x, event.y

    # data = [[-1.9, 2.0], [1.74, 2.0], [0.02, -0.36], [-1.16, -0.82],
    #         [1.48, -0.82], [-0.06, -3.36], [-4.4, -2.24],
    #         [-2.4, 3.28], [3.54, 2.66], [3.44, -1.98]]
    # f = f.add(R2Point(data[n][0], data[n][1]))
    # n += 1
    f = f.add(R2Point())
    # возможность добавлять точки кликом мыши (ЛКМ)
    # f = f.add(R2Point(from_screen_x(x), from_screen_y(y)))

    tk.clean()
    f.draw(tk)
    draw_rect()
    print(f"S = {f.area()}, P = {f.perimeter()}, "
          f"M = {f.intersection()}\n")


tk = TkDrawer()

print("Введите точки для четырехугольника")
rect = ConstRect(R2Point(), R2Point())
f = Void(rect)
tk.clean()
draw_rect()
while True:
    "Введите точку для оболочки"
    f = f.add(R2Point())
    tk.clean()
    f.draw(tk)
    draw_rect()
    print(f"S = {f.area()}, P = {f.perimeter()}, "
          f"M = {f.intersection()}\n")
# tk.root.bind('<Button-1>', add_point)
# tk.root.mainloop()
