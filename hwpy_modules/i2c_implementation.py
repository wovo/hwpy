# ===========================================================================
#
# part of hwpy: an OO hardware interface library
#
# home: https://www.github.com/wovo/hwpy
#
# ===========================================================================

# ===========================================================================
#
# i2c interface
#
# ===========================================================================

class i2c_implementation:
    """
    I2C implementation interface
    Implementations for i2c buses should implement at least the following methods
    """

    def read_command(self, address: int, command: int, n: int) -> list:
        raise NotImplementedError

    def write_command(self, address: int, command: int, data: list):
        raise NotImplementedError

    def write(self, address: int, data: list):
        raise NotImplementedError

    def read(self, address: int, count: int) -> list:
        raise NotImplementedError