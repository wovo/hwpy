"""
Blink on a single LED connected to a pcf8574 using hardware i2c
"""

import sys
sys.path.append( "../.." )
import hwpy
print( __doc__)

i2c = hwpy.i2c_hardware( 1 )
chip = hwpy.pcf8574( i2c )
 
hwpy.kitt( hwpy.invert( chip ))