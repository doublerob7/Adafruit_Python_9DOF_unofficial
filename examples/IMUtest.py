import sys
sys.path.append("~/Adafruit_Python_9DOF_unofficial")
import IMU_9DOF

imu = IMU_9DOF.IMU()

while True:
    imu.smart_update()
    print(imu.orientation())
