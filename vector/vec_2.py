import math

from vec_3 import Vec3


class Vec2(Vec3):
    def rotate(self, angle):
        return Vec2(self.x * math.cos(angle) - self.y * math.sin(angle),
                    self.x * math.sin(angle) + self.y * math.cos(angle),
                    self.z)

