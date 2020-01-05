"""
raspberry pi hardware spi

part of hwpy: an OO hardware interface library

home: https://www.github.com/wovo/hwpy
"""

import enum
from hwpy_modules.gpio import *

class _rapi_spi_hardware:
    class SPEED( enum.Enum ):
        M125 = 125000000
        M62_5 = 62500000
        M32_2 = 31200000
        M15_6 = 15600000
        M7_8 = 7800000
        M3_9 = 3900000
        K1953 = 1953000
        K976 = 976000
        K488 = 488000
        K244 = 244000
        K122 = 122000
        K61 = 61000
        K30_5 = 30500
        K15_2 = 15200
        K7_629 = 7629

    def __init__(self, bus: int, device: int, clock_polarity: bool = False, clock_phase: bool = False,
                 speed: SPEED = SPEED.K976):
        """
        Create a hardware SPI interface.
        The speed is set to 1M by default so the bus is easily debuggable with a simple logic analyzer
        See https://en.wikipedia.org/wiki/Serial_Peripheral_Interface#Clock_polarity_and_phase for information about clock phase and polarity
        On a raspberry pi, bus should be 0 most of the time,
        Device can either be 0 or 1, depending on the chip select line you are using
        """
        import spidev
        self.bus = spidev.SpiDev()
        self.bus.open(bus, device)
        self.bus.mode = (clock_polarity << 1) | clock_phase
        self.bus.max_speed_hz = speed.value

    def write_read(self, data_bytes, cs_pin: gpo = None):
        """
        Write and read on the SPI bus

        When passing a cs_pin, the given pin will be used instead of the raspberry Pi's CS0 or CS1,
        Use this if CS0 and CS1 are unavailable for your design
        """
        if cs_pin is not None:
            self.bus.no_cs = True
            cs_pin.write(self.bus.mode & 1)
        data = self.bus.xfer3(data_bytes)
        if cs_pin is not None:
            self.bus.no_cs = False
            cs_pin.write((~self.bus.mode) & 1)
        return data