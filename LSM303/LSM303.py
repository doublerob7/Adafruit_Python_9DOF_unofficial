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
from .. import I2C_Sensor


# Minimal constants carried over from Arduino library:
LSM303_ADDRESS_ACCEL = (0x32 >> 1)  # 0011001x
LSM303_ADDRESS_MAG   = (0x3C >> 1)  # 0011110x

ACCEL_REGISTERS = {'CTRL_REG1_A': 0x20,  # 00000111   rw
                   'CTRL_REG4_A': 0x23,  # 00000000   rw
                   'OUT_X_L_A':   0x28}

MAG_REGISTERS = {'CRB_REG_M': 0x01,  # 00000111   rw
                 'MR_REG_M':  0x02,  # 00000000   rw
                 'OUT_X_H_M': 0x03}

# Gain settings for set_mag_gain()
LSM303_MAGGAIN_1_3 = 0x20 # +/- 1.3
LSM303_MAGGAIN_1_9 = 0x40 # +/- 1.9
LSM303_MAGGAIN_2_5 = 0x60 # +/- 2.5
LSM303_MAGGAIN_4_0 = 0x80 # +/- 4.0
LSM303_MAGGAIN_4_7 = 0xA0 # +/- 4.7
LSM303_MAGGAIN_5_6 = 0xC0 # +/- 5.6
LSM303_MAGGAIN_8_1 = 0xE0 # +/- 8.1


class Accelerometer(I2C_Sensor.I2CSensor):
    """LSM303 accelerometer
    """

    def __init__(self, hires=True, address=LSM303_ADDRESS_ACCEL):
        """Initialize the LSM303 accelerometer & magnetometer.  The hires
        boolean indicates if high resolution (12-bit) mode vs. low resolution
        (10-bit, faster and lower power) mode should be used.
        """
        super().__init__(address, registers=ACCEL_REGISTERS)
        self.set_res(hires=hires)

    def set_res(self, hires):
        # Select hi-res (12-bit) or low-res (10-bit) output mode.
        # Low-res mode uses less power and sustains a higher update rate,
        # output is padded to compatible 12-bit units.
        if hires:
            self._sensor.write8(self.registers['CTRL_REG4_A'], 0b00001000)
        else:
            self._sensor.write8(self.registers['CTRL_REG4_A'], 0)

    def enable(self):
        """Gets called in super().__init__()"""
        self._sensor.write8(self.registers['CTRL_REG1_A'], 0x27)

    def read(self):
        """Read the accelerometer value.  A tuple of tuples will be returned with:
          (accel X, accel Y, accel Z)
        """
        # Read the accelerometer as signed 16-bit little endian values.
        accel_raw = self._sensor.readList(self.registers['OUT_X_L_A'] | 0x80, 6)
        accel = struct.unpack('<hhh', accel_raw)

        # Convert to 12-bit values by shifting unused bits.
        accel = (accel[0] >> 4, accel[1] >> 4, accel[2] >> 4)

        return accel


class Magnetometer(I2C_Sensor.I2CSensor):
    """LSM303 magnetometer."""

    def __init__(self, address=LSM303_ADDRESS_MAG):
        """Initialize the LSM303 magnetometer.
        """
        super().__init__(address=address, registers=MAG_REGISTERS)

    def enable(self):
        """Gets called in super().__init__()"""
        self._sensor.write8(self.registers['MR_REG_M'], 0x00)

    def read(self):
        """Read the magnetometer value.  A tuple of tuples will be returned with:
          (mag X, mag Y, mag Z)
        """
        mag_raw = self._sensor.readList(self.registers['OUT_X_H_M'], 6)
        mag = struct.unpack('>hhh', mag_raw)

        return mag

    def set_mag_gain(self, gain=LSM303_MAGGAIN_1_3):
        """Set the magnetometer gain.  Gain should be one of the following
        constants:
         - LSM303_MAGGAIN_1_3 = +/- 1.3 (default)
         - LSM303_MAGGAIN_1_9 = +/- 1.9
         - LSM303_MAGGAIN_2_5 = +/- 2.5
         - LSM303_MAGGAIN_4_0 = +/- 4.0
         - LSM303_MAGGAIN_4_7 = +/- 4.7
         - LSM303_MAGGAIN_5_6 = +/- 5.6
         - LSM303_MAGGAIN_8_1 = +/- 8.1
        """
        self._sensor.write8(self.registers['CRB_REG_M'], gain)
