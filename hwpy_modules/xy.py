"""
xy and xyz classes

part of hwpy: an OO hardware interface library

home: https://www.github.com/wovo/hwpy
"""

from hwpy_modules.wait import *
import copy

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

        self.x = copy.copy(x)
        self.y = copy.copy(y)

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
