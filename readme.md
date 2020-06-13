This is an OO (Object Oriented) Python library
for interfacing the Raspberry Pi to external hardware.
Python 3 is required.

The intended target is the RaspberryPi, but it can use an
Arduino Uno, Due, or a DB103 board as remote I/O pins.

Don't be scared of OO: it makes your life much easier,
and you are probably already using OO features without realizing.

authors:
   - Wouter van Ooijen (wouter.vanooijen@hu.nl)
   - Niels Post (niels.post@student.hu.nl)

Features:
   - pins: input, output, input-output, open-collector
   - set of pins: port
   - pin/port decorators: invert, all
   - serial interfaces: i2c, spi
   - chip interfaces: pcf8574(a), pcf8591, mpu6050
   - displays: hd44780 (direct, or througha pcf8574 i2c backpack)
   - other interfaces: servo, matrix keypad
   - on a RaspberryPi only: neopixels (WS2812)

license:
   - hwpy: Boost license (see license_1_0.txt)
   - Packages in the hwlib_extern directory have their own license

usage examples:
   - check the files in the demo directory

ToDo:
   - WS2801 biut-banged
   - 5x4 matrix keypad
   - embedded Python

