"""
neopixel ring demo
"""

import sys,time
sys.path.append( "../.." )
import hwpy
print( __doc__)


def neopixel_demo(ring, abort_when=lambda: False):
    for i in range(8):
        ring.set_pixel(i, (0, 0, 0))

    start = 0
    end = 2
    while not abort_when():
        ring.set_pixel(start, (0, 0, 0))
        ring.set_pixel(end, (10, 0, 0))
        start = (start + 1) % 8
        end = (end + 1) % 8

        ring.set_pixel(start, (5, 0, 0))
        ring.set_pixel(end, (5, 0, 0))

        time.sleep(.1)

    for i in range(8):
        ring.set_pixel(i, (0, 0, 0))


if __name__ == '__main__':
    ring = hwpy.neopixel(8)
    neopixel_demo(ring)
