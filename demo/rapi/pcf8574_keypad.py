"""
Read a 4x4 matrix keypad connected to a pcf8574
"""

import hwpy, time

sda = hwpy.gpoc( 2 ) 
scl = hwpy.gpoc( 3 )
i2c = hwpy.i2c_from_scl_sda( scl, sda )
chip = hwpy.pcf8574( i2c )
keypad = hwpy.keypad( 
   hwpy.port( [ chip.pins[ 0 ], chip.pins[ 1 ], chip.pins[ 2 ], chip.pins[ 3 ] ] ),
   hwpy.port( [ chip.pins[ 4 ], chip.pins[ 5 ], chip.pins[ 6 ], chip.pins[ 7 ] ] ),
   "D#0*C987B654A321")

print( __doc__ )
while True:
   print( keypad.read() )