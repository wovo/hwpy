# ===========================================================================
#
# hwpy: an OO hardware interface library
# - for the Raspberry Pi
# - for running native, connected to a GPIO server
#
# home: https://www.github.com/wovo/hwpy
#
# author: Wouter van Ooijen (wouter.vanooijen@hu.nl)
#
# uses http://domoticx.com/python-library-rpi-gpio/
# (which is pre-installed on the common RaPi Linux distributions)
#
# ToDo list
#
# pcf8591 a/d
# hd44780 direct demo
# serial backpack HD44780
# card reader
# HC595?
# https://bitbucket.org/MattHawkinsUK/rpispy-misc/src/master/
# graphics?
# most appropriate char output interface?
# 8x8 LED matrix
# generate documentation (interactive, web)
# Some tests (xy, xyz, maybe mocked gpio?)
# targets: remote; micro-python on due, esp8266 -> development cycle??
#
# ===========================================================================

import neopixel as adafruit_neopixel
import board
import time
from copy import copy

import typing

from bitstring import Bits

# ===========================================================================
#
# delays
#
# ===========================================================================
from enum import Enum


def wait_s(n):
    """Wait for n seconds.
    """

    time.sleep(n)


def wait_ms(n):
    """Wait for n milliseconds.
    """

    wait_s(n / 1000.0)


def wait_us(n):
    """Wait for n microseconds.
    """

    wait_ms(n / 1000.0)


# ===========================================================================
#
# xy class
#
# ===========================================================================

class xy:
    """Transparent container for an (x,y) value pair.
    """

    def __init__(self, x, y):
        """Create an xy object from x and y values.
        """

        self.x = copy(x)
        self.y = copy(y)

    def __eq__(self, other: 'xy'):
        """Compare for equality
        """
        return (self.x == other.y) and (self.y == other.y)

    def __ne__(self, other: 'xy'):
        """Compare for inequality
        """
        return (self.x != other.y) or (self.y != other.y)

    def __abs__(self):
        """Return the absolute.
        """
        return xy(abs(self.x), abs(self.y))

    def __add__(self, other: 'xy'):
        """Add two xy
        """
        return xy(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'xy'):
        """Subtract two xy
        """
        return xy(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """Multiply an xy by a scalar
        """
        return xy(self.x * other, self.y * other)

    def __rmul__(self, other):
        """Multiply an xy by a scalar
        """
        return xy(self.x * other, self.y * other)

    def __truediv__(self, other):
        """Divide an xy by a scalar
        """
        return xy(self.x / other, self.y / other)


# ===========================================================================
#
# xyz class
#
# ===========================================================================

class xyz:
    """Transparent container for an (x,y,z) value set.
    """

    def __init__(self, x, y, z):
        """Create an xyz object from x, y and z values.
        """

        self.x = copy(x)
        self.y = copy(y)
        self.z = copy(z)

    def __eq__(self, other: 'xyz'):
        """Compare for equality
        """
        return (
                (self.x == other.y)
                and (self.y == other.y)
                and (self.z == other.z))

    def __ne__(self, other: 'xyz'):
        """Compare for inequality
        """
        return (
                (self.x != other.y)
                or (self.y != other.y)
                or (self.z != other.z))

    def __abs__(self):
        """Return the absolute.
        """
        return xyz(abs(self.x), abs(self.y), abs(self.z))

    def __add__(self, other: 'xyz'):
        """Add two xyz
        """
        return xyz(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'xyz'):
        """Subtract two xyz
        """
        return xyz(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        """Multiply an xyz by a scalar
        """
        return xyz(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        """Multiply an xyz by a scalar
        """
        return xyz(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        """Divide an xyz by a scalar
        """
        return xyz(self.x / other, self.y / other, self.z * other)


# ===========================================================================
#
# Raspberry Pi gpio implementation
#
# ===========================================================================


class _rapi_gpio:
    """A Raspberry Pi gpio (input and output) pin.
    """

    def __init__(self, pin: int):
        """Create a gpio pin from its pin (BCM) number.
        """
        import RPi.GPIO as _gpio
        self.GPIO = _gpio
        self._init()
        self._pin = pin

        self.GPIO.setup(self._pin, self.GPIO.OUT)

    def _init(self):
        """Internal function that initializes RPi.GPIO.
        """
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setwarnings(False)

    def make_input(self, pullup: bool = True, pulldown: bool = False):
        """Make the gpio an input, by default, the pullup is enabled
        """
        if pulldown:
            pull_mode = self.GPIO.PUD_DOWN
        elif pullup:
            pull_mode = self.GPIO.PUD_UP
        else:
            pull_mode = self.GPIO.PUD_OFF

        self.GPIO.setup(
            self._pin,
            self.GPIO.IN,
            pull_up_down=pull_mode)

    def make_output(self):
        """Make the gpio an output.
        """
        self.GPIO.setup(
            self._pin,
            self.GPIO.OUT)

    def write(self, v):
        """Write v (0 or 1) to the gpio.

        Note: the pin must be an output.
        """
        self.GPIO.output(self._pin, v & 0x01)

    def read(self) -> int:
        """Read the value (0 or 1) of the gpio.

        Note: the pin must be an input.
        """
        return self.GPIO.input(self._pin)


# ===========================================================================
#
# Host-server implementation of a gpio
#
# ===========================================================================

_serial_port = None
_serial_port_name = "COM3"
_serial_port_baudrate = 115200


class _host_gpio:
    """A remote GPIO pin.

    This is a GPIO pin that is provided by a GPIO server.
    It is used via serial connection.

    To use this class, you must isntall PySerial:
       python -m pip install pyserial
    """

    cmd_input = 0
    cmd_output = 1
    cmd_high = 2
    cmd_low = 3
    cmd_read = 4

    def __init__(self, nr: int):
        self.pin = nr - 2

        global _serial_port
        if _serial_port is None:
            try:
                import serial
            except ImportError:
                serial = None
                print("To use Host GPIO, you need the pyserial module, install it with \"pip install pyserial\"")
                print("Exiting...")
                exit()

            _serial_port = serial.Serial(
                _serial_port_name,
                _serial_port_baudrate,
                timeout=1,
                parity=serial.PARITY_NONE
            )
            time.sleep(1.0)

    def _command(self, cmd, pin):
        d = chr((cmd << 5) + pin).encode('utf-8')
        if cmd == self.cmd_read:
            _serial_port.read(timeout=0)
            _serial_port.write(d)
            return _serial_port.read(timeout=1)
        else:
            _serial_port.write(d)
            b = _serial_port.read(size=1000)
            print(b.decode("utf-8", errors="ignore"))

    def make_input(self):
        """Make the gpio an input, with pull-up
        """
        self._command(
            self.cmd_input,
            self.pin
        )

    def make_output(self):
        """Make the gpio an output
        """
        self._command(
            self.cmd_output,
            self.pin
        )

    def write(self, v):
        """Write v (0 or 1) to the gpio.

        Note: the gpio must be an output.
        """
        self._command(
            self.cmd_high if v else self.cmd_low,
            self.pin
        )

    def read(self) -> bool:
        """Read the value (0 or 1) of the gpio.

        Note: the gpio must be an input.
        """
        c = self._command(
            self.cmd_read,
            self.pin
        )
        return False if c == '0' else True


# ===========================================================================
#
# the actual gpio used by an application
#
# ===========================================================================

"""Create a gpio pin.
"""
import os

if os.name == 'nt':
    gpio = _host_gpio
else:
    gpio = _rapi_gpio


# ===========================================================================
#
# gpio, gpi, gpo, gpoc
#
# ===========================================================================

class gpi:
    """A gpi (input only) pin (with pull-up).
    """

    def __init__(self, pin: int, pullup: bool = True, pulldown: bool = False):
        """Create a gpi pin from its (BCM) pin number.
        """
        self._pin = gpio(pin)
        self._pin.make_input(pullup, pulldown)

    def read(self) -> int:
        """Read the value (0 or 1) of the gpio.
        """

        return self._pin.read()


class gpo:
    """A gpo (output only) pin.
    """

    def __init__(self, pin: int):
        """Create a gpo pin from its (BCM) pin number.
        """
        self._pin = gpio(pin)
        self._pin.make_output()

    def write(self, v: int):
        """Write v (0 or 1) to the gpio.
        """
        self._pin.write(v)


class gpoc:
    """A gpoc (open-collector input output) pin.
    """

    def __init__(self, pin: int):
        """Create a gpoc pin from its (BCM) pin number.
        """
        self._pin = gpio(pin)
        self._pin.make_input()

    def write(self, v: int):
        """Write v (0 or 1) to the gpio.
        """
        if v:
            self._pin.make_input()
        else:
            self._pin.make_output()
            self._pin.write(0)

    def read(self) -> int:
        """Read the value (0 or 1) of the gpio.
        """
        return self._pin.read()


# ===========================================================================
#
# port
#
# ===========================================================================

class port:
    """A port is a set of pins.

    port.n is the number of pins.
    port.pins are the pins themselves.
    """

    def __init__(self, pins: list):
        """Create a port from a list of pins.
        """
        self.pins = pins
        self.n = len(self.pins)

    def read(self) -> int:
        """Read from a port.

        The result is an integer,
           with in bit 0 the value read from the first pin,
           in bit 1 the value read from the 2nd pin, etc.
        The pins must support read().
        """
        result = 0
        mask = 1
        for pin in self.pins:
            if pin.read():
                result = result + mask
            mask = mask << 1
        return result

    def write(self, v: int):
        """Write to port.

        v must be an integer.
        The lowest bit in v is written to the first pin,
           the lowets-but-one is written to the second pin, etc.
        The pins must support write().
        """
        mask = 1
        for pin in self.pins:
            pin.write(v & mask)
            mask = mask << 1

    def make_input(self):
        """Make all pins inputs.

        Note: the pins must be gpio.
        """
        for pin in self.pins:
            pin.make_input()

    def make_output(self):
        """Make all pins outputs.

        Note: The pins must be gpio.
        """
        for pin in self.pins:
            pin.make_output()


# ===========================================================================
#
# invert
#
# ===========================================================================

class invert:
    """Invert a pin or port.

    This decorator inverts the value that is read or written
    to or from a pin or port.
    """

    def __init__(self, minion):
        """Create an invert from its minion.
        """
        self._minion = minion

        # the minion *might* be a port and hence have an n
        try:
            self.n = self._minion.n
        except:
            pass

    def write(self, v: int):
        """Write the inverse of v to the minion.

        Note: the minion must support write().
        """
        self._minion.write(~ v)

    def read(self) -> int:
        """Return the inverse of the value read from the minion.

        Note: the minion must support read().
        """
        return ~ self._minion.read()

    def make_input(self):
        """Make the minion an input.

        Note: The minion must suppoirt make_input().
        """
        self._minion.make_input()

    def make_output(self):
        """Make the minion an output.

        Note: The minion must support make_output().
        """
        self._minion.make_output()


# ===========================================================================
#
# all
#
# ===========================================================================

class all:
    """Write to all supplied pins

    This decorator writes to all its minions.
    """

    def __init__(self, minions):
        """Create an all from a list of minions.
        """
        self._minions = minions

    def write(self, v):
        """Write v to all minions.
        """
        for m in self._minions:
            m.write(v)


# ===========================================================================
#
# matrix keypad
#
# ===========================================================================

class keypad:
    """
    Interface for a matrix keypad."""

    def __init__(self, rows, columns, characters):
        """Create a matrix keypad interface.

        Create a matrix keypad from the rows and columns ports,
        and the list of characters to be returned for pressed keys.
        The characters list is by row.
        The length of the list must be the number of rows multiplied
        by the number of columns.
        The rows must be inputs or open-collector,
        the columns must be outputs or open-collector.
        """
        self._rows = rows
        self._columns = columns
        self._characters = characters
        self._last = None

        # in case the rows are open collector, they must be made high
        try:
            self._rows.write(~ 0)
        except:
            pass

        if (self._rows.n * self._columns.n) != len(self._characters):
            raise ("keypad error %dsn rows %dsn columns %dn characters" %
                   (self._rows.n, self._columns.n, len(self._characters)))

    def is_pressed(self, key) -> bool:
        """Test whether a key is pressed.

        Return true if and only if the specified key is pressed.
        """
        i = self._characters.find(key)
        self._columns.write(~ (1 << (i / self._rows.n)))
        return (self._rows.read() & (1 << i % self._rows.n)) == 0

    def read_pressed_nonblocking(self, default):
        """Return a pressed key (non-blocking).

        Scan the keys until one is found that is pressed.
        When found, return the pressed key.
        When none is found, return the default.
        """
        for c in self._characters:
            if self.is_pressed(c):
                return c
        return default

    def read_pressed_blocking(self):
        """Return a pressed key (blocking).

        Scan the keyboard until a key is found pressed.
        Return that key.
        """
        while True:
            key = self.read_pressed_nonblocking(None)
            if key != None:
                return key

    def read(self, t: float = 0.050):
        """Read a newly pressed key.

        Scan the keyboard until a key is found newly pressed.
        Return that key.
        Wait t seconds between keypad scans
        to prevent lock-up of the system.
        """
        while True:
            key = self.read_pressed_nonblocking(None)
            if (key != None) and (key != self._last):
                self._last = key
                return key
            self._last = key
            time.sleep(t)


# ===========================================================================
#
# simple pin and port demos
#
# ===========================================================================

def blink(pin: gpo, t: float = 0.5):
    """Blink a LED on the pin.

    t is the period.
    The pin must be an output.
    """
    while True:
        pin.write(0)
        time.sleep(1.0 * t / 2)
        pin.write(1)
        time.sleep(1.0 * t / 2)


def kitt(kitt_port, t=0.5):
    """Kitt display on the pins in the port.

    t is the sweep time.
    The pins must be outputs.
    """
    while True:
        for p in range(0, kitt_port.n):
            kitt_port.write(1 << p)
            time.sleep(1.0 * t / kitt_port.n)
        for p in range(kitt_port.n - 1, 1, -1):
            kitt_port.write(1 << p)
            time.sleep(1.0 * t / kitt_port.n)


# ===========================================================================
#
# sr04 ultra-sonic distance sensor
#
# ===========================================================================

class sr04:
    """SR04 ultrasonic distance sensor interface.

    The HC-SR04 is an ultrasonic distance sensor.
    It runs at 5 Volt. The Pi runs at 3.3V.
    The trigger output to the sr04 is no problem, the sr04 will
    recognise the 3.3V from the Pi as a valid signal.
    The 5V echo from the sr04 to the Pi must be reduced
    to 3.3V, for instance by a two-resistor (330 Ohm and 470 Ohm)
    divider.
    """

    def __init__(self, trigger, echo, temperature=20):
        """Create an sr04 interface object.

        Create an sr04 object from the trigger (output to sr04)
        and echo (input from sr04, via resistors) pins.

        The speed of sound is somewhat dependant on the temperature.
        By default a temperature of 20 degrees is assumed, but you
        can specify a different temperature.
        """
        self._trigger = trigger
        self._echo = echo
        self._speed_of_sound = 33100 + (0.6 * temperature)
        self._trigger.write(0)

    def read(self) -> float:
        """Measure and return the distance in cm.

        When the sr04 is not connected properly or malfunctions
        this call might block (never return).
        """
        # 10 us pulse
        self._trigger.write(1)
        wait_us(10)
        self._trigger.write(0)

        # wait for start of the pulse
        while self._echo.read() == 0:
            pass
        start = time.time()

        # wait for end of the pulse
        while self._echo.read() != 0:
            pass
        end = time.time()

        return ((end - start) * self._speed_of_sound) / 2


# ===========================================================================
#
# Raspberry Pi hardware i2c
#
# ===========================================================================


class _i2c_implementation:
    """
    I2C implementation interface
    Implementations for i2c buses should implement at least the following methods
    """

    def read_command(self, address: int, command: int, n: int) -> list:
        raise NotImplementedError

    def write_command(self, address: int, command: int, data: list):
        raise NotImplementedError

    def write(self, address: int, data: list):
        raise NotImplementedError

    def read(self, address: int, count: int) -> list:
        raise NotImplementedError


class _rapi_i2c_hardware(_i2c_implementation):
    """Hardware i2c interface.

    This is the hardware i2c interface.
    It is much faster than the bit banged (software) version,
    but it must be enabled
    (sudo raspi-config; select 5 Interfacing Options; enable i2c),
    and it can only use the hardware i2c pins.
    """

    def __init__(self, interface: int = 1):
        """Create an interface to the hardware i2c.

        Recent Pi's use interface 1, which is the default.
        For older Pi's, if you get the error
        'IOError: [Errno 2] No such file or directory'
        try with interface=0.
        """
        import smbus
        self._bus = smbus.SMBus(interface)

    def write(self, address: int, data: list):
        """An i2c write transaction.

        Perform an i2c write transaction, writing the values
        in the data list to the device at the specified address.
        """
        self._bus.write_i2c_block_data(address, data[0], data[1:])

    def read(self, address: int, n: int) -> list:
        """An i2c read transaction.

        Perform an i2c read transaction, reading and returning
        n bytes from the device at the specified address.
        """
        return self._bus.read_i2c_block_data(address, 0, n)

    def read_command(self, address: int, command: int, n: int) -> list:
        return self._bus.read_i2c_block_data(address, command, n)

    def write_command(self, address: int, command: int, data: list):
        self._bus.write_i2c_block_data(address, command, data)


# ===========================================================================
#
# hardware i2c
#
# ===========================================================================

"""Hardware i2c interface.
   
This is the hardware i2c interface supported by the target.
"""
i2c_hardware = _rapi_i2c_hardware


# ===========================================================================
#
# bit-banged i2c
#
# ===========================================================================

class i2c_from_scl_sda(_i2c_implementation):
    """Software i2c interface.

    This is a bit-banged i2c interface.
    This interface is slow, but can be used on any pin pair.
    """

    def __init__(self, scl: gpoc, sda: gpoc):
        """Create a bit-banged i2c from the scl and sda pins.
        """
        self._scl = scl
        self._sda = sda
        self._scl.write(1)
        self._sda.write(1)

    def _wait(self):
        """Internal function that waits half a bit-cell.

        Currently this function does nothing,
        because bit-banged i2c is already slow.
        """
        pass

    def _write_one_bit(self, v: int):
        """Write a single bit.
        """
        self._scl.write(0)
        self._wait()
        self._sda.write(v)
        self._scl.write(1)

        while not self._scl.read():
            self._wait()

    def _read_one_bit(self) -> int:
        """Read and return a single bit.
        """
        self._scl.write(0)
        self._sda.write(1)
        self._wait()
        self._scl.write(1)

        while not self._scl.read():
            self._wait()

        b = self._sda.read()
        self._wait()
        return b

    def _write_ack(self):
        """Write an i2c ACK.
        """
        self._write_one_bit(0)

    def _write_nack(self):
        """Write an i2c NACK
        """
        self._write_one_bit(1)

    def _write_start(self):
        """Write an i2c START condition.
        """
        self._sda.write(0)
        self._wait()
        self._scl.write(0)
        self._wait()

    def _write_stop(self):
        """Write an i2c STOP condition.
        """
        self._scl.write(0)
        self._wait()
        self._sda.write(0)
        self._wait()
        self._scl.write(1)
        self._wait()
        self._sda.write(1)
        self._wait()

    def _read_ack(self) -> bool:
        """Read and return an i2c ACK bit.
        """
        return not self._read_one_bit()

    def _read_one_byte(self) -> int:
        """Read an return a single byte (as part of an i2c transaction).
        """
        result = 0
        mask = 0x80
        for i in range(0, 8):
            if self._read_one_bit():
                result = result | mask
            mask = mask >> 1
        return result

    def _write_one_byte(self, byte: int):
        """Write a single byte (as part of an i2c transaction).
        """
        mask = 0x80
        for i in range(0, 8):
            self._write_one_bit(byte & mask)
            mask = mask >> 1

    def write(self, address: int, data: list):
        """An i2c write transaction

        Perform an i2c write transaction:
        write the bytes to the chip with
        the (7-bit) address.
        """
        self._write_start()
        self._write_one_byte((address << 1) + 0x00)
        self._read_ack()

        for b in data:
            self._write_one_byte(b)
            self._read_ack()

        self._write_stop()

    def read(self, address: int, n: int) -> list:
        """An i2c read transaction.

        Perform an i2c read transaction:
        read and return n bytes from the chip with
        the (7-bit) address.
        """
        self._write_start()
        self._write_one_byte((address << 1) + 0x01)
        self._read_ack()

        result = []
        first = 1
        for i in range(0, n):
            if not first:
                self._write_ack()
            first = 0
            result.append(self._read_one_byte())

        self._write_nack()
        self._write_stop()
        return result

    def read_command(self, address: int, command: int, n: int) -> list:
        """An i2c read transaction, with an 8 bit address

        Writes the command byte, then reads and returns the next n bytes from the i2c bus"""
        self.write(address, [command])
        return self.read(address, n)

    def write_command(self, address: int, command: int, data: list):
        """An i2c write transaction, with an 8 bit address

        Writes the command byte, then the data bytes to the i2c bus
        """
        self.write(address, [command])
        self.write(address, data)


# ===========================================================================
#
# i2c_registers
#
# ===========================================================================

class i2c_registers:
    """Access to registers in an i2c peripheral chip.

    This class implements access to registers of an i2c peripheral,
    addressed in the customary i2c style: a first byte written is
    the register address for subsequent written bytes (in the same
    transaction) or read bytes (in the next transaction).
    Word (2 byte) values are assumed to be high-byte-first.
    """

    def __init__(self, i2c: _i2c_implementation, address: int):
        """Create a register access object.

        A register access object is created from an i2c bus
        and the i2c address of the peripheral.
        """
        self._i2c = i2c
        self._address = address

    def write_byte(self, register: int, value: int):
        """Write the specified byte to the specified register.
        """
        self._i2c.write_command(self._address, register, [value])

    def write_word(self, register: int, value: int):
        """Write the specified word (2 bytes) to the specified register.
        """
        self._i2c.write_command(self._address, register, [value >> 8, value & 0xFF])
        # self._i2c.write(self._address, [register, value >> 8, value & 0xFF])

    def read_byte(self, register: int) -> int:
        """Read and return a byte from the specified register.
        """
        return self._i2c.read_command(self._address, register, 1)[0]

    def read_word(self, register: int) -> int:
        """Read and return a word (2 bytes) from the specified register.
        """
        result = self._i2c.read_command(self._address, register, 2)
        return (result[0] << 8) + result[1]


# ===========================================================================
#
# buffered pin
#
# ===========================================================================

class _buffered_pin:
    """A buffered GPIO pin.

    A buffered GPIO pin performs GPIO read operations via a read_buffer
    that can be refreshed, and write operations via a write_buffer
    that can be flushed.
    """

    def __init__(self, master, nr: int):
        """Create a buffered pin from its master and it bit number.
        """
        self._master = master
        self._mask = 1 << nr

    def write(self, v: int):
        """Write the bit via the master.

        The bit value v is put in the master.write_buffer at the
        bit position nr (as specified to the constructor)
        and master.flush() is called.
        """
        if v:
            self._master._write_buffer |= self._mask
        else:
            self._master._write_buffer &= ~ self._mask
        self._master._flush()

    def read(self) -> bool:
        """Read the bit via the master and return it.

        The master.refresh() is called and the bit at position nr
        (as specified to the constructor) from the master.read_buffer
        is returned.
        """
        self._master._refresh()
        return (self._master._read_buffer & self._mask) != 0


# ===========================================================================
#
# pcf8574(a)
#
# ===========================================================================

class _pcf8574x:
    """Interface to pcf8754(a) i2c I/O extenders.

    The pcf8574 and pcf8574a are 8-bit i2c I/O extenders.
    The two chips differ only in the i2c (base) slave address.
    The 8 I/O pins provided by these chips are open-collector
    with built-in weak (think 100 kOhm) pull-ups.

    The I/O pins of a chip object can be used
       - as a port: chip.write( 0x55 )
       - as a single pin within the port: chip.pins[ 2 ].write( 0 )
       - as a single named pin: chip.p2.write( 0 )
    """

    def __init__(self, i2c: _i2c_implementation, address: int):
        """A pcf8574(a) interface from an i2c port and the slave address.

        Note: the address is the 7-bit i2c address.
        """
        self._i2c = i2c
        self._address = address
        self.pins = []
        self._read_buffer = 0
        self._write_buffer = 0
        self.n = 8
        for i in range(0, 8):
            self.pins.append(_buffered_pin(self, i))
        self.p0, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7 = self.pins

    def _flush(self):
        """Flush (write) the _write_buffer to the chip.
        """
        self._i2c.write(self._address, [self._write_buffer])

    def _refresh(self):
        """Refresh (read) the _read_buffer from the chip.
        """
        self._read_buffer = self._i2c.read(self._address, 1)[0]

    def write(self, value: int):
        """Write the value to the chips pins.
        """
        self._write_buffer = value
        self._flush()

    def read(self) -> int:
        """Read and return the chip pins.
        """
        self._refresh()
        return self._read_buffer


def pcf8574(i2c: _i2c_implementation, address: int = 0) -> _pcf8574x:
    """pcf8574 I/O extender interface

    Create a pcf8574 interface from the i2c port and the
    (3-bit) address configured on the 3 address pins a0-a1-a2.
    """
    return _pcf8574x(i2c, 0x20 + address)


def pcf8574a(i2c: _i2c_implementation, address: int = 0) -> _pcf8574x:
    """pcf8574a I/O extender interface

    Create a pcf8574a interface from the i2c port and the
    (3-bit) address configured on the 3 address pins a0-a1-a2.
    """
    return _pcf8574x(i2c, 0x28 + address)


# ===========================================================================
#
# mpu6050
#
# ===========================================================================

class mpu6050:
    """A simple interface to the mpu6050 accelerometer.
    """

    # registers
    PWR_MGMT_1 = 0x6B
    PWR_MGMT_2 = 0x6C
    ACCEL_XOUT0 = 0x3B
    ACCEL_YOUT0 = 0x3D
    ACCEL_ZOUT0 = 0x3F
    TEMP_OUT0 = 0x41
    GYRO_XOUT0 = 0x43
    GYRO_YOUT0 = 0x45
    GYRO_ZOUT0 = 0x47
    ACCEL_CONFIG = 0x1C
    GYRO_CONFIG = 0x1B

    def __init__(self, i2c: _i2c_implementation, address=0x68):
        """Create an mpu6050 interface from an i2c bus and the chip address.
        """
        self.registers = i2c_registers(i2c, address)
        self.registers.write_byte(self.PWR_MGMT_1, 0x00)

    def temperature(self) -> float:
        """Read and return the temperature, in degrees Celcius.
        """
        raw_temp = Bits(uint=self.registers.read_word(self.TEMP_OUT0), length=16).int
        actual_temp = (raw_temp / 340.0) + 36.53
        return actual_temp

    def gyroscopes(self) -> xyz:
        """Read and return the gyroscope readings.
        """
        return xyz(
            Bits(uint=self.registers.read_word(self.GYRO_XOUT0), length=16).int / 131,
            Bits(uint=self.registers.read_word(self.GYRO_YOUT0), length=16).int / 131,
            Bits(uint=self.registers.read_word(self.GYRO_ZOUT0), length=16).int / 131)

    def acceleration(self) -> xyz:
        """Read and return the acceleration readings.
        """
        return xyz(
            Bits(uint=self.registers.read_word(self.ACCEL_XOUT0), length=16).int / 16384.0,
            Bits(uint=self.registers.read_word(self.ACCEL_YOUT0), length=16).int / 16384.0,
            Bits(uint=self.registers.read_word(self.ACCEL_ZOUT0), length=16).int / 16384.0)


# ===========================================================================
#
# servo
#
# ===========================================================================

class servo:
    """Interface to a (hobby) servo.

    Python threading is used to create the actual servo pulses.
    One thread is created per servo.

    The common hobby servo's must be powered with 5V.
    One small (9G) servo can probably be powered directly from the Pi's 5V,
    for more or larger servo's you should use a separate 5V power.
    The PWM pulse to the servo should be 5V, but in practice the
    3.3V pulse from a Pi GPIO seems tgo work fine.

    Servo connectors vary. This seems to be the most common one:
    image: images/servo-pinout.png
    """

    def __init__(self, pin: gpo, min: int = 1000, max: int = 2000):
        """A servo interface

        A servo interface is created from the output pin to the servo.

        The min and max values are the pulse duration for the minimum
        (write(0)) and maximum (write(1)) settings.
        The 1000 and 2000 microseconds are the pulse lengths
        for the 'extreme' angles of a typical servo.
        """
        self._pin = pin
        self._min = min
        self._max = max
        self._value = 0
        # threading.start_new_thread(lambda: self._thread(), ()) TODO python3-ify this

    def write(self, value: int):
        """Write a new setting to the servo.

        The setting must be in the range 0.0 .. 1.0.
        """
        self._value = value

    def _thread(self):
        """The thread that outputs the PWM pulses to the servo.
        """
        while True:
            wait_ms(50)
            self._pin.write(1)
            wait_us(self._min + self._value * (self._max - self._min))
            self._pin.write(0)


# ===========================================================================
#
# hd44780
#
# ===========================================================================

class hd44780:
    """4-bit interface to an HD44780 (character) LCD.

    Some characters are treated special:
      - '\\n' puts the cursor at the first position of the next line
      - '\\r' puts the cursor at the start of the current line
      - '\\f' puts the cursor at the top-left position and clears the lcd
      - '\\txxyy' puts the cursor at the position (xx,yy)
    """

    @classmethod
    def from_pcf8574(cls, pcf_port: _pcf8574x, size: xy) -> 'hd44780':
        """Create an HD44780 instance from an i2c bus

        This should be used when using a pcf8574 i2c backpack with the lcd"""
        pcf_port.p3.write(True)
        port_4bit = port([pcf_port.pins[i] for i in range(4, 8)])
        return hd44780(pcf_port.p0, pcf_port.p2, port_4bit, size)

    def __init__(self, pin_rs: gpo, pin_e: gpo, port_data: port, size: xy):
        """Interface to a hd44780.

        Construct an interface to an LCD controlled by an hd44780 chip
        from the RS and E pins, the 4-bit port to the D4..D8 pins,
        and the size (number of characters per line, and number of lines),
        and initializes the controller.
        """
        self._rs = pin_rs
        self._e = pin_e
        self._data = port_data
        self.size = size
        self._position = xy(0, 0)

        self._e.write(0)
        self._rs.write(0)
        wait_ms(100)

        # interface initialization: make sure the LCD is in 4 bit mode
        # (magical sequence, taken from the HD44780 data-sheet)
        self._write4(0x03)
        wait_ms(15)
        self._write4(0x03)
        wait_us(100)
        self._write4(0x03)
        self._write4(0x02)  # 4 bit mode

        # functional initialization
        self.command(0x28)  # 4 bit mode, 2 lines, 5x8 font
        self.command(0x0C)  # display on, no cursor, no blink
        self.clear()  # clear display, 'cursor' home
        self.command(0x06)  # Set mode left-to-right
        self._goto_state = 0

    def _write4(self, nibble: int):
        """Write a nibble (4 bits) to the chip.
        """
        wait_us(10)
        self._data.write(nibble)
        wait_us(20)
        self._e.write(1)
        wait_us(20)
        self._e.write(0)
        wait_us(100)

    def _write8(self, is_data: int, byte: int):
        """Write a byte (two nibbles) as command or data.
        """
        self._rs.write(is_data)
        self._write4((byte >> 4))
        self._write4(byte)

    def command(self, cmd: int):
        """Write a command byte to the LCD

        Use this function only for features that are not
        provided by the console interface, like the definition
        of the user-defined characters.
        """
        self._write8(0, cmd)

    def data(self, char: typing.Union[str, bytes]):
        """Write a data byte to the LCD

        Use this function only for features that are not
        provided by the console interface, like the definition
        of the user-defined characters.
        """
        self._write8(1, ord(char))

    def clear(self):
        """Clear the display and put the cursor at (0,0).
        """
        self.command(0x01)
        wait_ms(5)
        self.cursor(xy(0, 0))

    def cursor(self, position: xy):
        """Place the cursor at the position.
        """
        self._position = position

        if self.size.y == 1:
            if self._position.x < 8:
                self.command(0x80 + self._position.x)
            else:
                self.command(0x80 + 0x40 + (self._position.x - 8))
        else:
            if self.size.y == 2:
                self.command(
                    0x80
                    + (0x40 if (self._position.y > 0) else 0x00)
                    + self._position.x)
            else:
                self.command(
                    0x80
                    + (0x40 if (self._position.y & 0x01) else 0x00)
                    + (0x14 if (self._position.y & 0x02) else 0x00))

    def write_char(self, char):
        """Write a single char.
        """
        if self._goto_state == 0:
            pass
        elif self._goto_state == 1:
            self._position.x = 10 * (char - '0')
            self._goto_state += 1
            return
        elif self._goto_state == 2:
            self._position.x += (char - '0')
            self._goto_state += 1
            return
        elif self._goto_state == 3:
            self._position.y = 10 * (char - '0')
            self._goto_state += 1
            return

        elif self._goto_state == 4:
            self._position.y += (char - '0')
            self._goto_state = 0
            self.cursor(self._position)
            return

        if (char == '\n'):
            self.cursor(xy(0, self._position.y + 1))

        elif (char == '\r'):
            self.cursor(xy(0, self._position.y))

        elif (char == '\v'):
            self.cursor(xy(0, 0))

        elif (char == '\f'):
            self.clear()

        elif (char == '\t'):
            self._goto_state = 1

        elif (
                (self._position.x >= 0)
                and (self._position.x < self.size.x)
                and (self._position.y >= 0)
                and (self._position.y < self.size.y)
        ):

            # handle the gap for 1-line displays
            if (self.size.x == 1) and (self._position.x == 8):
                self.cursor(self._position)
            self.cursor(self._position)
            self.data(char)

            self._position.x += 1

    def write(self, text: str):
        """Write a string.
        """
        for c in text:
            self.write_char(c)


class neopixel:
    def __init__(self, pixel_count: int):
        self.pixel_count = pixel_count
        self.pixels = adafruit_neopixel.NeoPixel(board.D18, pixel_count)

    def set_pixel(self, pixel: int, color: tuple):
        self.pixels[pixel] = color
        self.pixels.show()

    def clear(self):
        for i in range(self.pixel_count):
            self.pixels[i] = (0, 0, 0)
        self.pixels.show()

    def gradient(self, start: tuple, start_pixel: int, end: tuple, end_pixel: int):
        size = end_pixel - start_pixel
        diff = []
        for i in range(3):
            diff.append((end[i] - start[i]) / size)

        current_color = list(start)
        for i in range(start_pixel, end_pixel + 1):
            self.set_pixel(i, tuple(int(comp) for comp in current_color))
            for i in range(3):
                current_color[i] += diff[i]
        self.pixels.show()

    def __del__(self):
        self.pixels.deinit()


class _rapi_spi_hardware:
    class SPEED(Enum):
        M125 = 125000000
        M62_5 = 62500000
        M32_2 = 31200000
        M15_6 = 15600000
        M7_8 = 7800000
        M3_9 = 3900000
        K1953 = 1953000
        K976 = 976000
        K488 = 488000
        K244 = 244000
        K122 = 122000
        K61 = 61000
        K30_5 = 30500
        K15_2 = 15200
        K7_629 = 7629

    def __init__(self, bus: int, device: int, clock_polarity: bool = False, clock_phase: bool = False,
                 speed: SPEED = SPEED.K976):
        """
        Create a hardware SPI interface.
        The speed is set to 1M by default so the bus is easily debuggable with a simple logic analyzer
        See https://en.wikipedia.org/wiki/Serial_Peripheral_Interface#Clock_polarity_and_phase for information about clock phase and polarity
        On a raspberry pi, bus should be 0 most of the time,
        Device can either be 0 or 1, depending on the chip select line you are using
        """
        import spidev
        self.bus = spidev.SpiDev()
        self.bus.open(bus, device)
        self.bus.mode = (clock_polarity << 1) | clock_phase
        self.bus.max_speed_hz = speed.value

    def write_read(self, data_bytes, cs_pin: gpo = None):
        """
        Write and read on the SPI bus

        When passing a cs_pin, the given pin will be used instead of the raspberry Pi's CS0 or CS1,
        Use this if CS0 and CS1 are unavailable for your design
        """
        if cs_pin is not None:
            self.bus.no_cs = True
            cs_pin.write(self.bus.mode & 1)
        data = self.bus.xfer3(data_bytes)
        if cs_pin is not None:
            self.bus.no_cs = False
            cs_pin.write((~self.bus.mode) & 1)
        return data