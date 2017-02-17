import Adafruit_GPIO.I2C as I2C


class I2CSensor:
    """Class for the common traits and functions of modularized i2c sensor boards"""

    def __init__(self, address, registers, **kwargs):
        self.address = address
        self.registers = registers
        self._sensor = I2C.get_i2c_device(address=address, busnum=1, **kwargs)
        self.enable()
        self.bias = 0
        self.variance = 0

    def enable(self):
        """Many i2c devices require a bit in a specific register be flipped before
        they produce data. Put those commands in this function in a child class."""
        pass

    def read(self):
        """In a child class, put the code to retrieve data from the i2c devices
        registers in this function. Consult your chips data sheet for addresses and
        formats."""
        pass

    def calibrate(self):
        """calibration routine to measure 0 offset and sensor noise
        """
        from numpy import mean, var
        data = []

        while len(data) < 5000:
            sample = self.read()
            if sample > 5 * abs(data[len(data)]):
                break
            data.append(sample)

        self.bias = [mean(axis) for axis in data]
        self.variance = [var(axis) for axis in data]
