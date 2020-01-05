"""
Show the pcf8574 pins as inputs
"""

import hwpy, time

sda = hwpy.gpoc( 2 ) 
scl = hwpy.gpoc( 3 )
i2c = hwpy.i2c_from_scl_sda( scl, sda )
chip = hwpy.pcf8574( i2c )
chip.write( ~ 0 )

print( __doc__ )
while True:
   x = chip.read()
   y = x
   s = ""
   for i in range( 0, 8 ):
      s += "-X" if ( x % 2 ) == 1 else "-0" 
      x = x >> 1
   print( "%3d : %s " % ( y, s[ 1 : ] ))
   time.sleep( 0.2 )