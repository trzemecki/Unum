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
        value.match_units(unit)
    else:
        value = value * unit

    return value


def unitless(*values):
    unit = Unum(1, values[0]._unit)

    return (value.asNumber(unit) for value in values)


def as_unum(value):
    if isinstance(value, Unum):
        return value
    else:
        return Unum(value)


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
        value = with_unit(value, args[0])

    if isinstance(value, Unum):
        number = value.as_number(args[-1]) if len(args) > 0 else value.as_number()
    else:
        number = value

    try:
        number = round(number, kwargs['places'])
    except KeyError:
        pass

    return number
