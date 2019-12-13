"""
Show the values resad from an mpu6050
"""

import hwpy, time

# sda = hwpy.gpoc( 2 )
# scl = hwpy.gpoc( 3 )
# i2c = hwpy.i2c_from_scl_sda( scl, sda )
i2c = hwpy.i2c_hardware()


chip = hwpy.mpu6050( i2c )



while True:
   val = chip.temperature()
   # print("%d\t" * 3 % (val.x, val.y, val.z))
   # time.sleep( 0.2 )