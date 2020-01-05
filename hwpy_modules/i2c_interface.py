"""
i2c interface

part of hwpy: an OO hardware interface library

home: https://www.github.com/wovo/hwpy
"""

class i2c_interface:
    """
    I2C interface
    Implementations should implement at least the methods defined here.
    """

    def read_command(self, address: int, command: int, n: int) -> list:
        raise NotImplementedError

    def write_command(self, address: int, command: int, data: list):
        raise NotImplementedError

    def write(self, address: int, data: list):
        raise NotImplementedError

    def read(self, address: int, count: int) -> list:
        raise NotImplementedError