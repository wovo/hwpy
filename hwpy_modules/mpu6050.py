"""
mpu6050

part of hwpy: an OO hardware interface library

home: https://www.github.com/wovo/hwpy
"""

from hwpy_extern.bitstring.bitstring import Bits
from hwpy_modules.xy import *
from hwpy_modules.i2c_interface import *
from hwpy_modules.i2c_registers import *

class mpu6050:
    """A simple interface to the mpu6050 accelerometer.
    """

    # registers
    PWR_MGMT_1 = 0x6B
    PWR_MGMT_2 = 0x6C
    ACCEL_XOUT0 = 0x3B
    ACCEL_YOUT0 = 0x3D
    ACCEL_ZOUT0 = 0x3F
    TEMP_OUT0 = 0x41
    GYRO_XOUT0 = 0x43
    GYRO_YOUT0 = 0x45
    GYRO_ZOUT0 = 0x47
    ACCEL_CONFIG = 0x1C
    GYRO_CONFIG = 0x1B

    def __init__(self, i2c: i2c_interface, address=0x68):
        """Create an mpu6050 interface from an i2c bus and the chip address.
        """
        self.registers = i2c_registers(i2c, address)
        self.registers.write_byte(self.PWR_MGMT_1, 0x00)

    def temperature(self) -> float:
        """Read and return the temperature, in degrees Celcius.
        """
        raw_temp = Bits(uint=self.registers.read_word(self.TEMP_OUT0), length=16).int
        actual_temp = (raw_temp / 340.0) + 36.53
        return actual_temp

    def gyroscopes(self) -> xyz:
        """Read and return the gyroscope readings.
        """
        return xyz(
            Bits(uint=self.registers.read_word(self.GYRO_XOUT0), length=16).int / 131,
            Bits(uint=self.registers.read_word(self.GYRO_YOUT0), length=16).int / 131,
            Bits(uint=self.registers.read_word(self.GYRO_ZOUT0), length=16).int / 131)

    def acceleration(self) -> xyz:
        """Read and return the acceleration readings.
        """
        return xyz(
            Bits(uint=self.registers.read_word(self.ACCEL_XOUT0), length=16).int / 16384.0,
            Bits(uint=self.registers.read_word(self.ACCEL_YOUT0), length=16).int / 16384.0,
            Bits(uint=self.registers.read_word(self.ACCEL_ZOUT0), length=16).int / 16384.0)