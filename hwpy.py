"""
hwpy: an OO hardware interface library

This is a harware interface library for
- for the Raspberry Pi
- for Windows, connected to a GPIO server (Arduino Uno or Due)

Python 3 is required.

home: https://www.github.com/wovo/hwpy

authors: 
   - Wouter van Ooijen (wouter.vanooijen@hu.nl)
   - Niels Post (niels.post@student.hu.nl)

license:
   Boost license (see license_1_0.txt)

For the Pi http://domoticx.com/python-library-rpi-gpio/ is used
(which is pre-installed on the common RaPi Linux distributions).

For use with a server PySerial must be installed:
     python -m pip install pyserial

ToDo & wish list
- card reader?
- HC595?
- https://bitbucket.org/MattHawkinsUK/rpispy-misc/src/master/
- graphics?
- most appropriate char output interface?
- 8x8 LED matrix
- generate documentation (interactive, web)
- Some tests (xy, xyz, maybe mocked gpio?)
- targets: micro-python on due, esp8266 -> development cycle??
- pullup/pulldown for server pins
- a port and the pins of a pcf8574 should have the same interface
- document pin and port interfaces, and ad
"""

import os

#import time, typing, enum, sys
#import neopixel as adafruit_neopixel
#import board
#from copy import copy
#from enum import Enum

from hwpy_modules.wait import *
from hwpy_modules.xy import *
from hwpy_modules.gpio import *
from hwpy_modules.gpio_buffered import *
from hwpy_modules.port import *
from hwpy_modules.invert import *
from hwpy_modules.all import *
from hwpy_modules.keypad import *
from hwpy_modules.demos import *
from hwpy_modules.sr04 import *
from hwpy_modules.i2c_bb import *
from hwpy_modules.i2c_registers import *
from hwpy_modules.pcf8574 import *
from hwpy_modules.pcf8591 import *
#from hwpy_modules.mpu6050 import *
from hwpy_modules.servo import *
from hwpy_modules.hd44780 import *

if os.name != 'nt':
   from hwpy_modules.i2c_rapi import *
   from hwpy_modules.spi_rapi import *
   from hwpy_modules.neopixels_rapi import *
