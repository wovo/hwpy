# ===========================================================================
#
# part of hwpy: an OO hardware interface library
#
# home: https://www.github.com/wovo/hwpy
#
# ===========================================================================

from hwpy_modules.gpio import *
from hwpy_modules.wait import *

# ===========================================================================
#
# servo
#
# ===========================================================================

class servo:
    """Interface to a (hobby) servo.

    Python threading is used to create the actual servo pulses.
    One thread is created per servo.

    The common hobby servo's must be powered with 5V.
    One small (9G) servo can probably be powered directly from the Pi's 5V,
    for more or larger servo's you should use a separate 5V power.
    The PWM pulse to the servo should be 5V, but in practice the
    3.3V pulse from a Pi GPIO seems tgo work fine.

    Servo connectors vary. This seems to be the most common one:
    image: images/servo-pinout.png
    """

    def __init__(self, pin: gpo, min: int = 1000, max: int = 2000):
        """A servo interface

        A servo interface is created from the output pin to the servo.

        The min and max values are the pulse duration for the minimum
        (write(0)) and maximum (write(1)) settings.
        The 1000 and 2000 microseconds are the pulse lengths
        for the 'extreme' angles of a typical servo.
        """
        self._pin = pin
        self._min = min
        self._max = max
        self._value = 0
        # threading.start_new_thread(lambda: self._thread(), ()) TODO python3-ify this

    def write(self, value: int):
        """Write a new setting to the servo.

        The setting must be in the range 0.0 .. 1.0.
        """
        self._value = value

    def _thread(self):
        """The thread that outputs the PWM pulses to the servo.
        """
        while True:
            wait_ms(50)
            self._pin.write(1)
            wait_us(self._min + self._value * (self._max - self._min))
            self._pin.write(0)