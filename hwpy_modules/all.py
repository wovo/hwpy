"""
all

part of hwpy: an OO hardware interface library

home: https://www.github.com/wovo/hwpy

"""

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