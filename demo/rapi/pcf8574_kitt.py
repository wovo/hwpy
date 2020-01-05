"""
Blink on a single LED connected to a pcf8574
"""

import sys
sys.path.append( "../.." )
import hwpy
print( __doc__)

sda = hwpy.gpoc( 2 ) 
scl = hwpy.gpoc( 3 )
#i2c = hwpy.i2c_from_scl_sda( scl, sda )
i2c = hwpy.i2c_hardware( 1 )
chip = hwpy.pcf8574( i2c )
 
print( __doc__ ) 
hwpy.kitt( hwpy.invert( chip ))