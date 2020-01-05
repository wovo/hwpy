"""
Blink a LED connected to a PCF8574A.
"""

import sys
sys.path.append( "../.." )
import hwpy


i2c = hwpy.i2c_from_scl_sda( 
   hwpy.gpoc( hwpy.db103.scl ),
   hwpy.gpoc( hwpy.db103.sda ))
pcf = hwpy.pcf8574a( i2c )
   
print( __doc__ )
hwpy.blink( pcf.p0 )