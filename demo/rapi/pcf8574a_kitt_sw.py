"""
Blink on a single LED connected to a pcf8574a via software i2c
"""

import sys
sys.path.append( "../.." )
import hwpy
print( __doc__)

sda = hwpy.gpoc( 2 ) 
scl = hwpy.gpoc( 3 )
i2c = hwpy.i2c_from_scl_sda( scl, sda )
chip = hwpy.pcf8574a( i2c )
 
hwpy.kitt( hwpy.invert( chip ))