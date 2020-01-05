"""
simple pin and port demos

part of hwpy: an OO hardware interface library

home: https://www.github.com/wovo/hwpy
"""

import time
from hwpy_modules.gpio import *
from hwpy_modules.port import *

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


def kitt(p : port, t=0.5):
    """Kitt display on the pins in the port.

    t is the sweep time.
    The pins in the port must be outputs.
    """
    while True:
        for i in range(0, p.n):
            p.write(1 << i)
            time.sleep(1.0 * t / p.n)
        for i in range(p.n - 2, 0, -1):
            p.write(1 << i)
            time.sleep(1.0 * t / p.n)
            
def walk(p : port, t=0.5):
    """Walk (increasing-decreasing) display on the pins in the port.

    t is the sweep time.
    The pins in the port must be outputs.
    """
    while True:
        for i in range(0, p.n + 1):
            p.write( ( 1 << i ) - 1 )
            time.sleep(1.0 * t / p.n)
        for i in range(p.n, 1, -1):
            p.write(( 1 << i ) - 1 )
            time.sleep(1.0 * t / p.n)
            
            