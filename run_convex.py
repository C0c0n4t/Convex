#!/usr/bin/env -S python3 -B
from r2point import R2Point
from convex import Void, ConstRect

print("Введите точки для четырехугольника")
f = Void(ConstRect(R2Point(), R2Point()))
try:
    while True:
        f = f.add(R2Point())
        print(f"S = {f.area()}, P = {f.perimeter()}, "
              f"M = {f.inresection()}\n")
        print()
except (EOFError, KeyboardInterrupt):
    print("\nStop")
