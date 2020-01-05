"""
neopixel (WS2812)

part of hwpy: an OO hardware interface library

home: https://www.github.com/wovo/hwpy
"""

from hwpy_modules.gpio import *

class neopixels:
    def __init__(self, pixel_count: int):
        try:
           import neopixel as adafruit_neopixel
           import board
        except ModuleNotFoundError:
             print(
                "To use neopixels, you need the adafruit neopixel libary, install it with \n"
                "\"sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel\"." )
             print("Exiting...")
             exit()
        
        self.pixel_count = pixel_count
        self.pixels = adafruit_neopixel.NeoPixel(board.D18, pixel_count)

    def set_pixel(self, pixel: int, color: tuple):
        self.pixels[pixel] = color
        self.pixels.show()

    def clear(self):
        for i in range(self.pixel_count):
            self.pixels[i] = (0, 0, 0)
        self.pixels.show()

    def gradient(self, start: tuple, start_pixel: int, end: tuple, end_pixel: int):
        size = end_pixel - start_pixel
        diff = []
        for i in range(3):
            diff.append((end[i] - start[i]) / size)

        current_color = list(start)
        for i in range(start_pixel, end_pixel + 1):
            self.set_pixel(i, tuple(int(comp) for comp in current_color))
            for i in range(3):
                current_color[i] += diff[i]
        self.pixels.show()

    def __del__(self):
        self.pixels.deinit()


