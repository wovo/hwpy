"""
Demo for a hobby servo
"""

import sys, time
sys.path.append( "../.." )
import hwpy
print( __doc__ )

servo = hwpy.servo( hwpy.gpo( hwpy.arduino.d2 ))

while True:
   for x in range( 0, 100, 5 ):
      servo.write( x / 100.0 )
      time.sleep( 0.1 )   
   for x in range( 100, 0, -5 ):
      servo.write( x / 100.0 )
      time.sleep( 0.1 )