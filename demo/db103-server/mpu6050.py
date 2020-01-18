"""
Show the values read from an mpu6050
"""

import sys, time
sys.path.append( "../.." )
import hwpy
print( __doc__)

def mpu6050_demo(mpu: hwpy.mpu6050, abort_when=lambda: False):
    while not abort_when():
        gyro = mpu.gyroscopes()
        accel = mpu.acceleration()
        print("%10d %s %s" % (
            mpu.temperature(),
            str( gyro ),
            str( accel )
        ))
        time.sleep( 0.5 )


if __name__ == '__main__':
    i2c = hwpy.i2c_from_scl_sda(hwpy.gpoc(hwpy.db103.scl), hwpy.gpoc(hwpy.db103.sda))
    chip = hwpy.mpu6050(i2c)
    mpu6050_demo(chip)
