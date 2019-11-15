"""
Blink on a single LED connected to a pcf8574
"""

import hwpy

sda = hwpy.gpoc( 2 ) 
scl = hwpy.gpoc( 3 )
#i2c = hwpy.i2c_from_scl_sda( scl, sda )
i2c = hwpy.i2c_hardware( 0 )
chip = hwpy.pcf8574( i2c )
 
hwpy.kitt( hwpy.invert( chip ))