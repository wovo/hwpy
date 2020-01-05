"""
copy PCF8574A pin p0 to p1
"""

import sys
sys.path.append( "../.." )
import hwpy

import time

i2c = hwpy.i2c_from_scl_sda( 
   hwpy.gpoc( hwpy.db103.scl ),
   hwpy.gpoc( hwpy.db103.sda ))
pcf = hwpy.pcf8574a( i2c )
   
print( __doc__ )
pcf.write(0xFF)
while True:
   pcf.p1.write( pcf.p0.read())