"""
Demo for a hobby servo
"""

import time, hwpy
servo = hwpy.servo( hwpy.gpo( 18 ))

while True:
   for x in range( 0, 100, 5 ):
      servo.write( x / 100.0 )
      time.sleep( 0.1 )   
   for x in range( 100, 0, -5 ):
      servo.write( x / 100.0 )
      time.sleep( 0.1 )