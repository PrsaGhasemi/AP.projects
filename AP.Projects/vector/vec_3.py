import math


class Vec3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __str__(self):
        # return "Vec3(%s, %s, %s)" % (self.x, self.y, self.z)
        return "Vec3({}, {}, {})".format(self.x, self.y, self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y or self.z != other.z

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __ge__(self, other):
        return abs(self) >= abs(other)

    def __le__(self, other):
        return abs(self) <= abs(other)

    def __gt__(self, other):
        return abs(self) > abs(other)

    def __lt__(self, other):
        return abs(self) < abs(other)

    def out_prod(self, other):
        return Vec3(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z,
                    self.x * other.y - self.y * other.x)

    # def dist(self, other):

    def angle(self, other):
        return math.acos((self * other) / (abs(self) * abs(other)))

    def proj(self, other):
        return (self * other) / abs(other)

    def rej(self, other):
        return self - self.proj(other)

    def parallel(self, other):
        return self.proj(other) == self

    def prepend(self, other):
        return self.proj(other) == other

    def triangle_area(self, other):
        return abs(self.out_prod(other)) / 2

    def parallelogram_area(self, other):
        return abs(self.out_prod(other))

    def parallelepiped_vol(self, other1, other2):
        return abs(self.out_prod(other1).out_prod(other2))

    def prism_vol(self, other1, other2):
        return self.parallelepiped_vol(other1, other2) * abs(self)

    def pyramid_vol(self, other1, other2):
        return self.parallelepiped_vol(other1, other2) * abs(self) / 3

    
