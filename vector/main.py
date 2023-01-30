from vec_3 import Vec3
from vec_2 import Vec2

vec1 = Vec3(2, 3, -1)
vec2 = Vec3(-4, 6, 2)

print(vec1.__add__(vec2))
print(vec1.__sub__(vec2))
print(vec1.__mul__(vec2))

vec_rotate = Vec2(2, 2, 2)
print(vec_rotate.rotate(90))