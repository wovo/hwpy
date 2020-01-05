"""
Demo for the sr04 ultra-sonic distance sensor
controlling a servo
"""

import sys, time
sys.path.append( "../.." )
import hwpy
print( __doc__)

sr04 = hwpy.sr04( hwpy.gpo( 19 ), hwpy.gpi( 26 ) )
servo = hwpy.servo( hwpy.gpo( 18 ))

while True:
   cm = sr04.read()
   if cm < 5: cm = 5
   if cm > 25: cm = 25
   t = 1000 + 1000 * ( cm - 5 ) / 25
   print( cm, t )
   servo.write( t )
   time.sleep( 0.5 )