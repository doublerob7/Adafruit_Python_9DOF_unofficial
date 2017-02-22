from Adafruit_Python_9DOF_unofficial.IMU_9DOF import IMU

imu = IMU()

while True:
    imu.smart_update()
    print("pitch:{:<7.1f} roll:{:<7.1f} heading:{:<7.1f}".format(*imu.orientation()))
