remote GPIO servers

These applications implement a GPIO server that can be used to control
its GPIO pins over a serial line nusing a simple but fast protocol.

The main purpose is to test Python code that manipulates GPIO pins
without having to run the Python code on an embedded system.
The python code runs on the (windows or linux) host, and
communicates over a serial interface with the server.

Additionally, it is easier to swap one Arduino dwith peripheral
hardware for anotrher one, than swapping the peripherals connected
to a Raspberry Pi.
  
Protocol:
- 115k2 baud
   - one-byte commands to the server:
   - high 3 bits == command, as per enum class command (check the code)
   - low 5 bits == pin, as per pin_table (check the code)
- digital read sends back '0' or '1'
- other commands are silent

Notes:
- a maximum of 32 pins can be used this way
- pin numbering for Arduino servers is the arduino dN numbering
- d0 & d1 can't be used (used by the serial communication), 
   pin value 0 => pin d2
- only GPIO supported (no A/D), but the analog pins are available as d14...)
- the server doesn't do any checking

You will need bmptk, hwlib, and an ARM GCC compiler to
build and download a server using

   bmptk-make run

For the Due 115200 baud works OK, for the Uno 19200
seems to be the limit.

A tricky point is that opening the serial port might reset the Arduino.
To cope with this, there is a 2 second wait after opening
the serial port (inside the python gpio class).