"""
Main Unum module.
"""

from .exceptions import *

BASE_UNIT = 0


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

    return Unum.coerceToUnum(array(array_like, *args, **kwargs))


def with_unit(value, unit):
    if isinstance(value, Unum):
        value.matchUnits(unit)
    else:
        value = value * unit

    return value


def unitless(*values):
    unit = Unum(values[0]._unit, 1)

    return (value.asNumber(unit) for value in values)


def unit(symbol, definiton=BASE_UNIT, name=''):
    """
    Return a new unit represented by the string symbol.

    If conv is 0, the new unit is a base unit.
    If conv is a Unum, the new unit is a derived unit equal to conv.

    >>> KB = unit("kB", 0, "kilobyte")
    >>> MB = unit("MB", 1000*KB, "megabyte")
    """

    return Unum({symbol: 1}, 1, definiton, name)


class Unum(object):
    """
    Encapsulates a value attached to a unit.

    Implements arithmetic operators, dynamic unit consistency checking, and
    string representation.
    """

    # TODO consider move it to other class "Formatter"
    UNIT_SEP = "."
    """Separator between multiple units: e.g. "5 N.m". """

    UNIT_DIV_SEP = "/"
    """Separator between numerator and denominator.

    If set to None, negative exponents are used instead.
    """

    UNIT_FORMAT = "[%s]"
    """Format string for attached unit."""

    UNIT_INDENT = " "
    """Separator between value and unit."""

    UNIT_HIDE_EMPTY = False
    """If True, unitless unums are displayed as raw numbers."""

    UNIT_SORTING = True
    """If True, units are sorted alphabetically for display."""

    VALUE_FORMAT = "%s"
    """Format string for value."""

    AUTO_NORM = True
    """If True, normalize unums for their string representation."""

    # -- internal constants ------------------------------------------
    _NO_UNIT = {}

    # -- internal working storage ------------------------------------
    # unit dictionary :
    #  the key is the unit string
    #  the value is a tuple (conversion unum, level, name)
    _unitTable = {}

    __slots__ = ('_value', '_unit', '_normal')

    def __init__(self, unit, value=1, definition=None, name=''):
        """
        :param unit: a dictionary of {unit symbol : exponent}
        :param value: number
        :param definition:
            None if self does not represent a unit (default),
            0 if self represents a basic unit
            unum equivalent to self, expressed in other unit(s) if self represents a derived unit

        :param name: the unit full name if self represents a basic unit
        :raises UnumError: if definition is a unum although unit and value do not represent a basic unit
        """

        self._value = value
        self._unit = unit

        if definition is None:
            self._normal = False
        else:
            unit_key = list(unit.keys())[0]
            if unit_key in Unum._unitTable:
                raise NameConflictError(unit_key)
            self._normal = True
            if isinstance(definition, int) and definition == 0:
                conv_unum = None
                level = 0
            else:
                if value == 0 or len(unit) != 1 or list(unit.values())[0] != 1:
                    raise NonBasicUnitError(self)
                conv_unum = Unum.coerceToUnum(definition) / value
                level = conv_unum.maxLevel() + 1
                conv_unum._normal = True
            Unum._unitTable[unit_key] = conv_unum, level, name

    unit = staticmethod(unit)

    @classmethod
    def reset(cls, unitTable=None):
        """
        Clear the unit table, replacing it with the new one if provided.

        This is generally only useful when playing around with defining new
        units in the interpreter.

        """

        cls._unitTable = {} if unitTable is None else unitTable

    @classmethod
    def getUnitTable(cls):
        """
        Return a copy of the unit table.
        """

        return cls._unitTable.copy()

    def copy(self, normalized=False):
        """
        Return a copy of this Unum, normalizing the copy if specified.
        """

        result = Unum(self._unit.copy(), self._value)

        if normalized:
            result.normalize()

        return result

    def asUnit(self, other):
        """
        Return a Unum with this Unum's value and the units of the given Unum.

        Raises IncompatibleUnitsError if self can't be converted to other.
        Raises NonBasicUnitError if other isn't a basic unit.
        """

        other = Unum.coerceToUnum(other)

        if (other._value == 0) or (other != Unum(other._unit, 1)):
            raise NonBasicUnitError(other)

        s, o = self.matchUnits(other)
        res = Unum(other._unit, s._value / o._value)
        res._normal = True

        return res

    def replaced(self, u, conv_unum):
        """
        Return a Unum with the string u replaced by the Unum conv_unum.

        If u is absent from self, a copy of self is returned.
        """

        res = self.copy() * conv_unum ** self._unit[u]
        del res._unit[u]
        return res

    def normalize(self, forDisplay=False):
        """
        Normalize our units IN PLACE and return self.

        Substitutions may be applied to reduce the number of different units,
        while making the fewest substitutions.

        If forDisplay is True, then prefer a single unit to no unit.
        """
        # TODO: example of forDisplay.
        # TODO: simplify normalize so it fits in 80 columns...

        best_l = len(self._unit)
        new_subst_unums = [({}, +self)]
        while new_subst_unums:
            subst_unums, new_subst_unums = new_subst_unums, []
            for subst_dict, subst_unum in subst_unums:
                for u, exp in list(subst_unum._unit.items()):
                    conv_unum = Unum._unitTable[u][0]
                    if conv_unum is not None:
                        new_subst_dict = subst_dict.copy()
                        new_subst_dict[u] = exp + new_subst_dict.get(u, 0)
                        is_new = True
                        for subst_dict2, subst_unum2 in new_subst_unums:
                            if new_subst_dict == subst_dict2:
                                is_new = False
                                break
                        if is_new:
                            s = subst_unum.replaced(u, conv_unum)
                            new_subst_unums.append((new_subst_dict, s))
                            new_l = len(s._unit)
                            if new_l < best_l and not (forDisplay and new_l == 0 and best_l == 1):
                                self._value, self._unit = s._value, s._unit
                                best_l = new_l
        return self

    def checkNoUnit(self):
        """
        :raises ShouldBeUnitlessError: if self has a unit
        """

        if self._unit:
            raise ShouldBeUnitlessError(self)  # TODO consider other way to signalize it

    def maxLevel(self):
        """
        :return: the maximum level of self's units
        """
        return max([0] + [Unum._unitTable[u][1] for u in self._unit.keys()])

    def matchUnits(self, other):
        """
        Return (self, other) where both Unums have the same units.

        Raises IncompatibleUnitsError if there is no way to do this.
        If there are multiple ways to do this, the units of self, then other
        are preferred, and then by maximum level.
        """

        if self._unit == other._unit:
            return self, other

        if self._value == 0:
            return Unum(other._unit, self._value), other

        if other._value == 0:
            return self, Unum(self._unit, other._value)

        s = self.copy()
        o = other.copy()
        s_length, o_length = len(s._unit), len(o._unit)
        revert = (s_length > o_length or
                  (s_length == o_length and s.maxLevel() < o.maxLevel()))
        if revert:
            s, o = o, s
        target_unum = Unum(s._unit, 1)
        o /= target_unum
        o.normalize()
        if o._unit:
            raise IncompatibleUnitsError(self, other)
        o._unit = s._unit
        if revert:
            s, o = o, s
        return s, o

    # TODO: could support in-place operators for 2.5 and higher.

    # Arithmetic operations.
    # These raise IncompatibleUnitsError if the operands have incompatible units.
    def __add__(self, other):
        s, o = self.matchUnits(Unum.coerceToUnum(other))
        return Unum(s._unit, s._value + o._value)

    def __sub__(self, other):
        s, o = self.matchUnits(Unum.coerceToUnum(other))
        return Unum(s._unit, s._value - o._value)

    def __pos__(self):
        # TODO: is it really beneficial to share the unit dictionary?
        return Unum(self._unit.copy(), self._value)

    def __neg__(self):
        return Unum(self._unit.copy(), -self._value)

    def __mul__(self, other):
        other = Unum.coerceToUnum(other)
        if not self._unit:
            unit = other._unit
        elif not other._unit:
            unit = self._unit
        else:
            unit = self._unit.copy()
            for u, exp in other._unit.items():
                exp += unit.get(u, 0)
                if exp:
                    unit[u] = exp
                else:
                    del unit[u]
        return Unum(unit, self._value * other._value)

    def __div__(self, other):
        other = Unum.coerceToUnum(other)
        if not other._unit:
            unit = self._unit
        else:
            unit = self._unit.copy()
            for u, exp in list(other._unit.items()):
                exp -= unit.get(u, 0)
                if exp:
                    unit[u] = -exp
                else:
                    del unit[u]
        return Unum(unit, self._value / other._value)

    __truediv__ = __div__  # Python 3.0 compatibility.

    def __floordiv__(self, other):
        other = Unum.coerceToUnum(other)
        if not other._unit:
            unit = self._unit
        else:
            unit = self._unit.copy()
            for u, exp in list(other._unit.items()):
                exp -= unit.get(u, 0)
                if exp:
                    unit[u] = -exp
                else:
                    del unit[u]
        return Unum(unit, self._value // other._value)

    def __pow__(self, other):
        other = Unum.coerceToUnum(other)
        if other._value:
            other = other.copy(True)
            other.checkNoUnit()
            unit = self._unit.copy()
            for u in list(self._unit.keys()):
                unit[u] *= other._value
        else:
            unit = Unum._NO_UNIT
        return Unum(unit, self._value ** other._value)

    def __lt__(self, other):
        s, o = self.matchUnits(Unum.coerceToUnum(other))
        return s._value < o._value

    def __le__(self, other):
        s, o = self.matchUnits(Unum.coerceToUnum(other))
        return s._value <= o._value

    def __gt__(self, other):
        s, o = self.matchUnits(Unum.coerceToUnum(other))
        return s._value > o._value

    def __ge__(self, other):
        s, o = self.matchUnits(Unum.coerceToUnum(other))
        return s._value >= o._value

    def __eq__(self, other):
        s, o = self.matchUnits(Unum.coerceToUnum(other))
        return s._value == o._value

    def __ne__(self, other):
        s, o = self.matchUnits(Unum.coerceToUnum(other))
        return s._value != o._value

    def __abs__(self):
        return Unum(self._unit.copy(), abs(self._value))

    def asNumber(self, other=None):
        """
        Return the (normalized) raw value of self.

        If other is supplied, first convert to other's units before returning
        the raw value.

        Raises NonBasicUnitError if other is supplied, but has a value other
        than 1. (e.g., kg.asNumber(2*g) is an error, but kg.asNumber(g) is ok.)
        """

        if other is None:
            return self.copy(True)._value

        if isinstance(other, Unum):
            if (other._value == 0) or (other != Unum(other._unit, 1)):
                raise NonBasicUnitError(other)
            else:
                s, o = self.matchUnits(other)
                return s._value / o._value
        else:
            s = self.copy(True)
            s.checkNoUnit()
            return s._value / other

    def __complex__(self):
        return complex(self.asNumber(1))

    def __int__(self):
        return int(self.asNumber(1))

    def __long__(self):
        return int(self.asNumber(1))

    def __float__(self):
        return float(self.asNumber(1))

    def __radd__(self, other):
        return Unum.coerceToUnum(other).__add__(self)

    def __rsub__(self, other):
        return Unum.coerceToUnum(other).__sub__(self)

    def __rmul__(self, other):
        return Unum.coerceToUnum(other).__mul__(self)

    def __rdiv__(self, other):
        return Unum.coerceToUnum(other).__div__(self)

    __rtruediv__ = __rdiv__  # Python 3.0 compatibility.

    def __rfloordiv__(self, other):
        return Unum.coerceToUnum(other).__floordiv__(self)

    def __rpow__(self, other):
        return Unum.coerceToUnum(other).__pow__(self)

    def __getitem__(self, index):
        return Unum(self._unit, self._value[index])

    def __setitem__(self, index, value):
        u = Unum.coerceToUnum(value)
        self._value[index] = u.asNumber(Unum(self._unit, 1))

    def __len__(self):
        return len(self._value)

    # -- String representation methods -------------------------------
    def strUnit(self):
        """Return a string representation of our unit."""

        def fmt(exp):
            f = ''
            if exp != 1:
                f = str(exp)
            return f

        numer, denom = '', ''
        units = list(self._unit.items())
        if Unum.UNIT_SORTING:
            units.sort()
        for u, exp in units:
            if exp > 0 or not Unum.UNIT_DIV_SEP:
                if numer:
                    numer += Unum.UNIT_SEP
                numer += u + fmt(exp)
            else:
                if denom:
                    denom += Unum.UNIT_SEP
                denom += u + fmt(-exp)
        if denom:
            denom = Unum.UNIT_DIV_SEP + denom
            if not numer:
                numer = '1'
        if not numer and Unum.UNIT_HIDE_EMPTY:
            result = ''
        else:
            result = Unum.UNIT_FORMAT % (numer + denom)
        return result

    def __str__(self):
        """Return our string representation, normalized if applicable.

        Normalization occurs if Unum.AUTO_NORM is set.
        """
        if Unum.AUTO_NORM and not self._normal:
            self.normalize(True)
            self._normal = True
        return (Unum.VALUE_FORMAT % self._value +
                Unum.UNIT_INDENT +
                self.strUnit())

    __repr__ = __str__

    @staticmethod
    def coerceToUnum(value):
        """
        Return a unitless Unum if value is a number.

        If value is a Unum already, it is returned unmodified.
        """
        if isinstance(value, Unum):
            return value
        else:
            return Unum(Unum._NO_UNIT, value)

    def __getstate__(self):
        return self._value, self._unit, self._normal

    def __setstate__(self, state):
        self._value, self._unit, self._normal = state
