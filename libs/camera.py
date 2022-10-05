from libs.transform import *


class Camera(Trackball):
    def __init__(self, yaw=0., roll=0., pitch=0., distance=3., radians=None):
        super(Camera, self).__init__(yaw=yaw, roll=roll, pitch=pitch, distance=distance, radians=radians)

    @staticmethod
    def place(eye, at, up):
        direction = eye - at
        distance = np.linalg.norm(direction)
        direction = direction / distance
        x, y, z = direction[0], direction[1], direction[2]
        pitch = math.asin(y) * (180. / math.pi)
        yaw = math.atan2(x, z) * (180. / math.pi)
        yaw = yaw - 90.0

        u = np.cross(up, direction)
        u = u / np.linalg.norm(u)
        v = np.cross(direction, u)
        v = v / np.linalg.norm(v)
        roll = math.acos(v[1]) * (180. / math.pi)
        roll = roll - 90.0
        return Camera(yaw=yaw, roll=roll, pitch=pitch, distance=distance)
