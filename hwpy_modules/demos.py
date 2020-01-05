"""
simple pin and port demos

part of hwpy: an OO hardware interface library

home: https://www.github.com/wovo/hwpy
"""

import time
from hwpy_modules.gpio import *

def blink( pin : gpo, t: float = 0.5 ):
    """Blink a LED on the pin.

    t is the period.
    The pin must be an output.
    """
    while True:
        pin.write(0)
        time.sleep(1.0 * t / 2)
        pin.write(1)
        time.sleep(1.0 * t / 2)


def kitt(kitt_port, t=0.5):
    """Kitt display on the pins in the port.

    t is the sweep time.
    The pins must be outputs.
    """
    while True:
        for p in range(0, kitt_port.n):
            kitt_port.write(1 << p)
            time.sleep(1.0 * t / kitt_port.n)
        for p in range(kitt_port.n - 2, 0, -1):
            kitt_port.write(1 << p)
            time.sleep(1.0 * t / kitt_port.n)