from .core import Unum


def uarray(array_like, *args, **kwargs):
    """
    Convenience function to return a Unum containing a numpy array.
    With current versions of numpy, we have the following undesirable behavior:
    >>> array([5,6,7,8]) * M
    array([5 [m], 6 [m], 7 [m], 8 [m]], dtype=object)

    :param array_like: numpy array
    :param args: args given to numpy array
    :param kwargs: kwargs given to numpy
    :return: Unum containing numpy array
    """
    from numpy import array

    return Unum.uniform(array(array_like, *args, **kwargs))


def with_unit(value, unit):
    if isinstance(value, Unum):
        value.matchUnits(unit)
    else:
        value = value * unit

    return value


def unitless(*values):
    unit = Unum(1, values[0]._unit)

    return (value.asNumber(unit) for value in values)

