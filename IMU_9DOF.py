from Adafruit_Python_9DOF_unofficial import LSM303
from Adafruit_Python_9DOF_unofficial import L3DG20
from Adafruit_Python_9DOF_unofficial.micropythonFusion.fusion import Fusion


class Event:

    def __init__(self):
        pass


class IMU(Fusion):

    def __init__(self):
        super().__init__()
        self.accel = LSM303.Accelerometer()
        self.mag = LSM303.Magnetometer()
        self.gyro = L3DG20.Gyroscope()

        self.testing = False

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


if __name__ == "__main__":

    def vec_sum(*args):
        from math import sqrt
        return sqrt(sum((arg ** 2 for arg in args)))

    print("Testing configuration. Please rotate IMU about each axis individually.")

    imu = IMU()
    imu.testing = True

    while imu.testing:
        vals = imu.accel.read()
        accel_sum = vec_sum(vals)
        accelx_norm, accely_norm, accelz_norm = (val/accel_sum for val in vals)
        print("Acc x:{:<7.1f} Acc y:{:<7.1f} Acc z:{:<7.1f}".format(accelx_norm, accely_norm, accelz_norm))

        vals = imu.mag.read()
        mag_sum = vec_sum(vals)
        magx_norm, magy_norm, magz_norm = (val / mag_sum for val in vals)
        print("Mag x:{:<7.1f} Mag y:{:<7.1f} Mag z:{:<7.1f}".format(magx_norm, magy_norm, magz_norm))

        vals = imu.gyro.read()
        gyro_sum = vec_sum(vals)
        gyrox_norm, gyroy_norm, gyroz_norm = (val / gyro_sum for val in vals)
        print("Gyr x:{:<7.1f} Gyr y:{:<7.1f} Gyr z:{:<7.1f}".format(gyrox_norm, gyroy_norm, gyroz_norm))

        





