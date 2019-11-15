"""
Show the values resad from an mpu6050
"""

import hwpy, time

sda = hwpy.gpoc( 2 ) 
scl = hwpy.gpoc( 3 )
i2c = hwpy.i2c_from_scl_sda( scl, sda )
chip = hwpy.mpu6050( i2c )

while True:

   print( 
      "%d C " % (
      chip.temperature()
   )      
   time.sleep( 0.2 )