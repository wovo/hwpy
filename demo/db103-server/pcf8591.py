"""
Read and show the 4 A/D inputs of a PCF8591
"""

import sys
sys.path.append( "../.." )
import hwpy

import time

i2c = hwpy.i2c_from_scl_sda( 
   hwpy.gpoc( hwpy.db103.scl ),
   hwpy.gpoc( hwpy.db103.sda ))
pcf = hwpy.pcf8591( i2c )
   
print( __doc__ )
while True:
   print( "" )
   for c in range( 0, 4 ):
     v = pcf.read( c )
     print( "%d %3d %s" % ( c, v, ( v // 3 ) * '=' ))
   time.sleep( 1.0 )   