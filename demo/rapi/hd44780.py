import hwpy

# This demo shows how to implement a scrolling line on an HD44780 LCD


# Initialize an i2c hardware bus (by default pins BCM2(SDA1) and BCM3(SCL1) are used
i2c = hwpy.i2c_hardware()
# When these pins are already in use:
# i2c = hwpy.i2c_hardware(2) BCM0(SDA2) and BCM1(SCL2)
# When these are also not available, you can create 2 gpoc's and use hwpy.i2c_from_scl_sda

# Initialize a PCF8574 (The address is usually 0x07)
port = hwpy.pcf8574(i2c, 0x07)


# Initialize an HD44780 from the PCF, 16X12 is the size of the LCD in characters
lcd = hwpy.hd44780.from_pcf8574(port, hwpy.xy(16,2))

string = "This is a pretty long text to display"
current_start = 0
counter = 0
i = 0
while True:
    # Return the cursor to the top left
    lcd.cursor(hwpy.xy(0,0))

    # Clear the first row and return to the top left
    lcd.write(" " * 16 + "\r")

    # Write the current part of the string
    lcd.write(string[current_start:min(len(string), current_start + 16)] + "\n")


    # Move the start of the display 1 character, resetting it to 0 when the end is reached
    current_start = (current_start + 1) % len(string)

    # Roughly every second, increment the counter and show it
    i += 1
    if i % 4 == 0:
        counter += 1
        # Write the counter to the second row
        lcd.write(str(counter))

    hwpy.wait_ms(200)

