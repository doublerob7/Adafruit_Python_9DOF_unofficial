from L3DG20 import L3DG20
from LSM303 import LSM303
from micropythonFusion.fusion import Fusion


class Event:

    def __init__(self):
        pass


class IMU(Fusion):

    def __init__(self):
        super().__init__()
        self.accel = LSM303.LSM303Accel()
        self.mag = LSM303.LSM303Mag()
        self.gyro = L3DG20()

    def smart_update(self):
        """Use update_nomag if magnetometer isn't configured, otherwise use update()"""
        if self.mag.bias == (0, 0, 0):
            self.update_nomag(self.accel.read(), self.gyro.read())
        else:
            self.update(self.accel.read(), self.gyro.read(), self.mag.read())

    def orientation(self):
        """Return pitch, roll, heading. Note heading is not accurate if magnetometer isn't calibrated"""
        return self.pitch, self.roll, self.heading

    def gravity(self):
        # TODO: output the gravity vector orientation result of sensor micropythonFusion
        # gravity =
        pass

    def linear_accel(self):
        # TODO: output the linear acceleration component of motion (translational acceleration)
        # a = F/m
        pass


