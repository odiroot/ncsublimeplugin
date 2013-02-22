"""
Sample doctests.
"""


def mul(first, sec):
    """ Multiplies input values and returns the result

    >>> mul(1,1)
    1
    >>> mul(10, 2)
    20
    """
    return first * sec


def div(first, sec):
    """ Divides input values and returns the result

    >>> div(1,1)
    1
    >>> div(10, 2)
    5
    >>> div(2, 0)
    Traceback (most recent call last):
        ...
    ZeoDivisionError: integer division or modulo by zero
    """
    return first / sec



class Test(object):
    def mul(self, a, b):
        """ Multiplies input values and returns the result

        >>> a=Test()
        >>> a.mul(1,1)
        1
        >>> a.mul(10, 2)
        21
        """
        return a * b
