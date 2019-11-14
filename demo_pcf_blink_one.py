"""
Blink on a single LED connected to a pcf8574
"""

import hwpy

scl = hwpy.gpoc( 3 ) 
sda = hwpy.gpoc( 2 )
i2c = hwpy.i2c_from_scl_sda( scl, sda )
chip = hwpy.pcf8574( i2c )
 
hwpy.blink( chip.pins[ 0 ] )