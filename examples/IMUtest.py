#import sys
#sys.path.append("~/Adafruit_Python_9DOF_unofficial
from Adafruit_Python_9DOF_unofficial.IMU_9DOF import IMU

imu = IMU()

while True:
    imu.smart_update()
    print(imu.orientation())
