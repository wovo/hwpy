"""
Walk on the LEDs connected to a pcf8574a using sw i2c
"""

import sys
sys.path.append( "../.." )
import hwpy
print( __doc__)

sda = hwpy.gpoc( 2 ) 
scl = hwpy.gpoc( 3 )
i2c = hwpy.i2c_from_scl_sda( scl, sda )
chip = hwpy.pcf8574a( i2c )
 
hwpy.walk( hwpy.invert( chip ), 0.300 )