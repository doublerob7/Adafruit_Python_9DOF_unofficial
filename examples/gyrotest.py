import L3DG20

gyro = L3DG20.L3DG20()

while True:
    print(gyro.read())
