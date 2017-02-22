# The MIT License (MIT)
#
# Copyright (c) 2016 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import struct
from I2C_Sensor import I2CSensor

L3GD20_ADDRESS = 0x6B  # 1101011
L3GD20_POLL_TIMEOUT = 100  # Maximum number of read attempts
L3GD20_ID = 0xD4
L3GD20H_ID = 0xD7

# Sensitivity values from the mechanical characteristics in the datasheet.
GYRO_SENSITIVITY = {'250DPS': 0.00875,
                    '500DPS': 0.0175,
                    '2000DPS': 0.070}

GYRO_RATE = {'250DPS': 0b00,
             '500DPS': 0b01,
             '2000DPS': 0b10}

GYRO_REGISTER = {'WHO_AM_I': 0x0F,  # 11010100   r
                 'CTRL_REG1': 0x20,  # 00000111   rw
                 'CTRL_REG2': 0x21,  # 00000000   rw
                 'CTRL_REG3': 0x22,  # 00000000   rw
                 'CTRL_REG4': 0x23,  # 00000000   rw
                 'CTRL_REG5': 0x24,  # 00000000   rw
                 'REFERENCE': 0x25,  # 00000000   rw
                 'OUT_TEMP': 0x26,  # r
                 'STATUS_REG': 0x27,  # r
                 'OUT_X_L': 0x28,  # r
                 'OUT_X_H': 0x29,  # r
                 'OUT_Y_L': 0x2A,  # r
                 'OUT_Y_H': 0x2B,  # r
                 'OUT_Z_L': 0x2C,  # r
                 'OUT_Z_H': 0x2D,  # r
                 'FIFO_CTRL_REG': 0x2E,  # 00000000   rw
                 'FIFO_SRC_REG': 0x2F,  # r
                 'INT1_CFG': 0x30,  # 00000000   rw
                 'INT1_SRC': 0x31,  # r
                 'TSH_XH': 0x32,  # 00000000   rw
                 'TSH_XL': 0x33,  # 00000000   rw
                 'TSH_YH': 0x34,  # 00000000   rw
                 'TSH_YL': 0x35,  # 00000000   rw
                 'TSH_ZH': 0x36,  # 00000000   rw
                 'TSH_ZL': 0x37,  # 00000000   rw
                 'INT1_DURATION': 0x38}  # 00000000   rw


class Gyroscope(I2CSensor):
    """L3DG20 Gyroscope.
    """

    def __init__(self, address=L3GD20_ADDRESS, registers=GYRO_REGISTER, rate='250DPS'):
        super().__init__(address, registers)
        """Initialize the L3DG20 Gyroscope. Set the refresh rate if it differs from the sensor default 250dps.
        """
        self.dps_to_rad = 0.017453293
        self.rate = rate
        self.bias = (0, 0, 0)

        # Set gyro refresh rate (250 DPS, 500 DPS, 2000 DPS) if it differs from sensor default (250dps) (0b00000000).
        if rate != '250DPS':
            self.set_rate(rate)

    def enable(self):
        """Gets called in super().__init__()"""
        # Enable the gyro by changing the power-down bit (default | PD bit)
        # (0: (default) PD enabled, 1: PD disabled)
        self._sensor.write8(GYRO_REGISTER['CTRL_REG1'], 0b00000000)
        self._sensor.write8(GYRO_REGISTER['CTRL_REG1'], 0b00000111 | 0b00001000)

    def set_rate(self, rate):
        self._sensor.write8(GYRO_REGISTER['CTRL_REG4'], 0b00000000 | GYRO_RATE[rate] << 4)

    def read_raw(self):
        """Read the raw gyroscope sensor values.  A tuple will be returned with:
          (gyro X, gyro Y, gyro Z)
        """
        # Read the gyro as signed 16-bit little endian values.
        gyro_raw = self._sensor.readList(GYRO_REGISTER['OUT_X_L'] | 0x80, 6)
        gyro_data = struct.unpack('<hhh', gyro_raw)

        return (data - bias for data, bias in zip(gyro_data, self.bias))

    def read(self):
        """Return the corrected gyro sensor reading in rad/s
        """
        reading = self.read_raw()

        if self.rate == 'AUTO' and any(abs(reading)) > 32760:
            self.range_up()

        return [value * GYRO_SENSITIVITY[self.rate] * self.dps_to_rad for value in reading]

    def range_up(self):
        # TODO: scale up to next range
        pass
