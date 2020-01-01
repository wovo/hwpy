# ===========================================================================
#
# part of hwpy: an OO hardware interface library
#
# home: https://www.github.com/wovo/hwpy
#
# ===========================================================================

import time

# ===========================================================================
#
# delays
#
# ===========================================================================

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


