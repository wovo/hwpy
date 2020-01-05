"""
Raspberry Pi hardware i2c

part of hwpy: an OO hardware interface library

home: https://www.github.com/wovo/hwpy
"""

from hwpy_modules.i2c_interface import *
import smbus

class _rapi_i2c_hardware(i2c_interface):
    """Hardware i2c interface.

    This is the hardware i2c interface.
    It is much faster than the bit banged (software) version,
    but it must be enabled
    (sudo raspi-config; select 5 Interfacing Options; enable i2c),
    and it can only use the hardware i2c pins.
    """

    def __init__(self, interface: int = 1):
        """Create an interface to the hardware i2c.

        Recent Pi's use interface 1, which is the default.
        For older Pi's, if you get the error
        'IOError: [Errno 2] No such file or directory'
        try with interface=0.
        """
        import smbus
        try:
           self._bus = smbus.SMBus(interface)
        except FileNotFoundError:
             print(
                "To use the hardware i2c, enable i2c in the kernel using "
                "\"sudo raspi-config\"." )
             print("Exiting...")
             exit()
              

    def write(self, address: int, data: list):
        """An i2c write transaction.

        Perform an i2c write transaction, writing the values
        in the data list to the device at the specified address.
        """
        self._bus.write_i2c_block_data(address, data[0], data[1:])

    def read(self, address: int, n: int) -> list:
        """An i2c read transaction.

        Perform an i2c read transaction, reading and returning
        n bytes from the device at the specified address.
        """
        return self._bus.read_i2c_block_data(address, 0, n)

    def read_command(self, address: int, command: int, n: int) -> list:
        return self._bus.read_i2c_block_data(address, command, n)

    def write_command(self, address: int, command: int, data: list):
        self._bus.write_i2c_block_data(address, command, data)

# ===========================================================================
#
# hardware i2c
#
# ===========================================================================

"""Hardware i2c interface.
   
This is the hardware i2c interface supported by the target.
"""
i2c_hardware = _rapi_i2c_hardware