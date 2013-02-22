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
    ZeroDivisionError: integer division or modulo by zero
    """
    return first / sec

