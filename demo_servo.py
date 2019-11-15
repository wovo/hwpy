"""
Demo for a hobby servo
"""

import time, hwpy
sr04 = hwpy.servo( hwpy.gpo( 5 ))

while True:
   for x in range( 0, 100, 1 ):
      servo.write( x / 1200.0 )
      time.sleep( 0.05 )   
   for x in range( 100, 0, -1 ):
      servo.write( x / 100.0 )
      time.sleep( 0.05 )