import hwpy

from demo.rapi.neopixel_ring import neopixel_demo

i2c_bus_lcd = hwpy.i2c_hardware()
lcd = hwpy.i2c_lcd(i2c_bus_lcd)

left, last_left = hwpy.gpi(22, pulldown=True), False
ok, last_ok = hwpy.gpi(27, pulldown=True), False
right, last_right = hwpy.gpi(17, pulldown=True), False

led_ring = hwpy.neopixel(8)

demos = [
    ("Neopixel demo", neopixel_demo),
    ("MPU6050 Demo", neopixel_demo)

]
current_demo = 0

lcd.lcd_display_string(demos[current_demo][0], 1)

test = hwpy.xy(0,0)
test2 = test / 4


while True:
    left_val = left.read()
    right_val = right.read()
    ok_val = ok.read()

    if left_val and not last_left:
        current_demo = (current_demo - 1) % len(demos)
        lcd.lcd_clear()
        lcd.lcd_display_string(demos[current_demo][0], 0)

    if right_val and not last_right:
        current_demo = (current_demo + 1) % len(demos)
        lcd.lcd_clear()
        lcd.lcd_display_string(demos[current_demo][0], 0)

    if ok_val and not last_ok:
        while ok.read():
            pass

        demos[current_demo][1](led_ring, lambda: ok.read())

    last_left = left_val
    last_right = right_val
    last_ok = ok_val
    hwpy.wait_ms(10)

