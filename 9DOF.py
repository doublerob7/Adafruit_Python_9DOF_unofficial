from L3DG20 import L3DG20_2 as L3DG20
from LSM303 import LSM303_2 as LSM303


class Event:

    def __init__(self):
        pass


class IMU:

    def __init__(self):
        self.accel = LSM303.LSM303Accel()
        self.mag = LSM303.LSM303Mag()
        self.gyro = L3DG20.L3DG20()

    def orientation_accel(self):
        # TODO: raw orientation vector (just accelerometer)
        return self.accel.read()
        pass

    def orientation_mag(self):
        # TODO: raw orientation vector (magnetometer)
        pass

    def gravity(self):
        # TODO: output the gravity vector orientation result of sensor fusion
        # gravity =
        pass

    def linear_accel(self):
        # TODO: output the linear acceleration component of motion (translational acceleration)
        # a = F/m
        pass


