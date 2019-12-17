"""
Show the values resad from an mpu6050
"""

import hwpy, time

i2c = hwpy.i2c_hardware()

chip = hwpy.mpu6050(i2c)

while True:
    val = chip.temperature()
