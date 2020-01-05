"""
Blink all LEDs connected to a pcf8574
"""

import sys
sys.path.append( "../.." )
import hwpy
print( __doc__)

sda = hwpy.gpoc( 2 ) 
scl = hwpy.gpoc( 3 )
i2c = hwpy.i2c_from_scl_sda( scl, sda )
chip = hwpy.pcf8574( i2c )
 
hwpy.blink( hwpy.all( chip.pins ) )