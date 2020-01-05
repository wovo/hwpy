"""
sr04 ultra-sonic distance sensor

part of hwpy: an OO hardware interface library

home: https://www.github.com/wovo/hwpy
"""

from hwpy_modules.wait import *

class sr04:
    """SR04 ultrasonic distance sensor interface.

    The HC-SR04 is an ultrasonic distance sensor.
    It runs at 5 Volt. The Pi runs at 3.3V.
    The trigger output to the sr04 is no problem, the sr04 will
    recognise the 3.3V from the Pi as a valid signal.
    The 5V echo from the sr04 to the Pi must be reduced
    to 3.3V, for instance by a two-resistor (330 Ohm and 470 Ohm)
    divider.
    """

    def __init__(self, trigger, echo, temperature=20):
        """Create an sr04 interface object.

        Create an sr04 object from the trigger (output to sr04)
        and echo (input from sr04, via resistors) pins.

        The speed of sound is somewhat dependant on the temperature.
        By default a temperature of 20 degrees is assumed, but you
        can specify a different temperature.
        """
        self._trigger = trigger
        self._echo = echo
        self._speed_of_sound = 33100 + (0.6 * temperature)
        self._trigger.write(0)

    def read(self) -> float:
        """Measure and return the distance in cm.

        When the sr04 is not connected properly or malfunctions
        this call might block (never return).
        """
        # 10 us pulse
        self._trigger.write(1)
        wait_us(10)
        self._trigger.write(0)

        # wait for start of the pulse
        while self._echo.read() == 0:
            pass
        start = time.time()

        # wait for end of the pulse
        while self._echo.read() != 0:
            pass
        end = time.time()

        return ((end - start) * self._speed_of_sound) / 2
