from .core import Unum
from .exceptions import NonBasicUnitError


def uarray(array_like, *args, **kwargs):
    """
    Convenience function to return a Unum containing a numpy array.
    With current versions of numpy, we have the following undesirable behavior:
    >>> from unum.units import M
    >>> array([5,6,7,8]) * M
    array([5 [m], 6 [m], 7 [m], 8 [m]], dtype=object)

    :param array_like: numpy array
    :param args: args given to numpy array
    :param kwargs: kwargs given to numpy
    :return: Unum containing numpy array
    """
    from numpy import array

    return Unum.uniform(array(array_like, *args, **kwargs))


def unitless(*values):
    unit = Unum(1, values[0]._unit)

    return (value.asNumber(unit) for value in values)


def is_unit(value):
    return isinstance(value, Unum) and value.is_basic()


def as_unum(value, unit=None):
    if unit is not None and not is_unit(unit):
        raise NonBasicUnitError(unit)

    if isinstance(value, Unum):
        if unit is not None:
            value = value.cast_unit(unit)

        return value

    return Unum(value) if unit is None else value * unit


def as_unit(value):
    return value.unit() if isinstance(value, Unum) else Unum(1)


def as_number(value, *args, **kwargs):
    """
    Using:
    as_number(value, [places=])
    as_number(value, to_unit, [places=])
    as_number(value, from_unit, to_unit, [places=])

    :param value: float or unum value to conversion
    :param from_unit: unit which value has when is given as float or int
    :param to_unit: unit for which numeric value is getting
    :param places: round argument
    :return: evaluated float value
    """
    assert len(args) <= 2

    if len(args) == 2:
        value = as_unum(value, args[0])

    if isinstance(value, Unum):
        number = value.number(args[-1]) if len(args) > 0 else value.number()
    else:
        number = value

    try:
        number = round(number, kwargs['places'])
    except KeyError:
        pass

    return number


def encode(number):
    if isinstance(number, Unum):
        value, unit, normal = number.__getstate__()
        return [value, unit]
    else:
        return number


def decode(number):
    if isinstance(number, (list, tuple)):
        value, unit = number
        result = Unum(value, unit)
        return result
    else:
        return number
