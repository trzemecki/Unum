"""
Main Unum module.
"""

from .exceptions import *

BASIC_UNIT = 0


def unit(symbol, definition=BASIC_UNIT, name=''):
    """
    Return a new unit represented by the string symbol.

    If conv is 0, the new unit is a base unit.
    If conv is a Unum, the new unit is a derived unit equal to conv.

    >>> KB = unit("kB", 0, "kilobyte")
    >>> MB = unit("MB", 1000*KB, "megabyte")
    """

    return Unit(symbol, definition, name)


class UnitTable(dict):
    def reset(self, unitTable=None):
        self.clear()
        if unitTable is not None:
            self.update(unitTable)

    def new_unit(self, symbol, definition, name):
        self[symbol] = Unit(symbol, definition, name)


UNIT_TABLE = UnitTable()


class Formatter(object):
    def __init__(
            self, mul_separator='.', div_separator='/',
            unit_format='[%s]', value_format='%s', indent=' ',
            hide_empty=False, auto_norm=True
    ):

        self._mul = mul_separator
        self._div = div_separator
        self._unit_format = unit_format
        self._value_format = value_format
        self._indent = indent
        self._auto_norm = auto_norm
        self._hide_empty = hide_empty

    def format_unit(self, unit):
        """
        Return a string representation of our unit.
        """

        def format_exponent(symbol, exp):
            return symbol + (str(exp) if exp != 1 else '')

        units = sorted(unit.items())

        if not self._div:
            return self._unit_format % self._mul.join(format_exponent(u, exp) for u, exp in units)

        result = self._div.join([
            self._mul.join(format_exponent(u, exp) for u, exp in units if exp > 0) or '1',
            self._mul.join(format_exponent(u, -exp) for u, exp in units if exp < 0)
        ]).rstrip(self._div + '1')

        return '' if not result and self._hide_empty else self._unit_format % result

    def format_value(self, value):
        return self._value_format % value

    def format(self, unum):
        """
        Return our string representation, normalized if applicable.

        Normalization occurs if Unum.AUTO_NORM is set.
        """
        if self._auto_norm and not unum._normal:
            unum.normalize(True)
            unum._normal = True

        return self._indent.join([self.format_value(unum._value), self.format_unit(unum._unit)]).strip()


class Unum(object):
    """
    Encapsulates a value attached to a unit.

    Implements arithmetic operators, dynamic unit consistency checking, and
    string representation.
    """

    @staticmethod
    def uniform(value):
        """
        Return a unitless Unum if value is a number.

        If value is a Unum already, it is returned unmodified.
        """
        if isinstance(value, Unum):
            return value
        else:
            return Unum(value, Unum._NO_UNIT)

    formatter = Formatter()

    _NO_UNIT = {}

    _unitTable = UnitTable()

    __slots__ = ('_value', '_unit', '_normal')

    @classmethod
    def set_format(cls, **kwargs):
        cls.formatter = Formatter(**kwargs)

    @classmethod
    def reset_format(cls):
        cls.formatter = Formatter()

    def __init__(self, value, unit):
        """
        :param value: number or other object represents the mathematical value (e.g. numpy array)
        :param dict unit: {unit symbol : exponent} for example for 1 m/s2 should give {'m': 1, 's': -2}
        """

        self._value = value
        self._unit = dict(unit)
        self._normal = False

    @property
    def unit(self):
        return self.formatter.format_unit(self._unit)

    @classmethod
    def reset(cls, unitTable=None):
        """
        Clear the unit table, replacing it with the new one if provided.

        This is generally only useful when playing around with defining new
        units in the interpreter.

        """
        cls._unitTable.reset(unitTable)

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

        result = Unum(self._value, self._unit.copy())

        if normalized:
            result.normalize()

        return result

    def asUnit(self, other):
        """
        Return a Unum with this Unum's value and the units of the given Unum.

        Raises IncompatibleUnitsError if self can't be converted to other.
        Raises NonBasicUnitError if other isn't a basic unit.
        """

        other = Unum.uniform(other)

        if (other._value == 0) or (other != Unum(1, other._unit)):
            raise NonBasicUnitError(other)

        s, o = self.matchUnits(other)
        res = Unum(s._value / o._value, other._unit)
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
            if (other._value == 0) or (other != Unum(1, other._unit)):
                raise NonBasicUnitError(other)
            else:
                s, o = self.matchUnits(other)
                return s._value / o._value
        else:
            s = self.copy(True)
            s.checkNoUnit()
            return s._value / other

    def matchUnits(self, other):
        """
        Return (self, other) where both Unums have the same units.

        Raises IncompatibleUnitsError if there is no way to do this.
        If there are multiple ways to do this, the units of self, then other
        are preferred, and then by maximum level.
        """
        assert isinstance(other, Unum)

        if self._unit == other._unit:
            return self, other

        if self._value == 0:
            return Unum(self._value, other._unit), other

        if other._value == 0:
            return self, Unum(other._value, self._unit)

        s = self.copy()
        o = other.copy()

        s_length, o_length = len(s._unit), len(o._unit)

        revert = (s_length > o_length or
                  (s_length == o_length and s.maxLevel() < o.maxLevel()))

        if revert:
            s, o = o, s

        target_unum = Unum(1, s._unit)
        o /= target_unum
        o.normalize()

        if o._unit:
            raise IncompatibleUnitsError(self, other)

        o._unit = s._unit

        if revert:
            s, o = o, s

        return s, o

    def __add__(self, other):
        s, o = self.matchUnits(Unum.uniform(other))
        return Unum(s._value + o._value, s._unit)

    def __sub__(self, other):
        s, o = self.matchUnits(Unum.uniform(other))
        return Unum(s._value - o._value, s._unit)

    def __pos__(self):
        return Unum(self._value, self._unit)

    def __neg__(self):
        return Unum(-self._value, self._unit)

    def __mul__(self, other):
        other = Unum.uniform(other)
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
        return Unum(self._value * other._value, unit)

    def __div__(self, other):
        other = Unum.uniform(other)
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
        return Unum(self._value / other._value, unit)

    __truediv__ = __div__  # Python 3.0 compatibility.

    def __floordiv__(self, other):
        other = Unum.uniform(other)
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
        return Unum(self._value // other._value, unit)

    def __pow__(self, other):
        other = Unum.uniform(other)
        if other._value:
            other = other.copy(True)
            other.checkNoUnit()
            unit = self._unit.copy()
            for u in list(self._unit.keys()):
                unit[u] *= other._value
        else:
            unit = Unum._NO_UNIT
        return Unum(self._value ** other._value, unit)

    def __lt__(self, other):
        s, o = self.matchUnits(Unum.uniform(other))
        return s._value < o._value

    def __le__(self, other):
        s, o = self.matchUnits(Unum.uniform(other))
        return s._value <= o._value

    def __gt__(self, other):
        s, o = self.matchUnits(Unum.uniform(other))
        return s._value > o._value

    def __ge__(self, other):
        s, o = self.matchUnits(Unum.uniform(other))
        return s._value >= o._value

    def __eq__(self, other):
        s, o = self.matchUnits(Unum.uniform(other))
        return s._value == o._value

    def __ne__(self, other):
        s, o = self.matchUnits(Unum.uniform(other))
        return s._value != o._value

    def __abs__(self):
        return Unum(abs(self._value), self._unit)

    def __complex__(self):
        return complex(self.asNumber(1))

    def __int__(self):
        return int(self.asNumber(1))

    def __long__(self):
        return int(self.asNumber(1))

    def __float__(self):
        return float(self.asNumber(1))

    def __radd__(self, other):
        return Unum.uniform(other).__add__(self)

    def __rsub__(self, other):
        return Unum.uniform(other).__sub__(self)

    def __rmul__(self, other):
        return Unum.uniform(other).__mul__(self)

    def __rdiv__(self, other):
        return Unum.uniform(other).__div__(self)

    __rtruediv__ = __rdiv__  # Python 3.0 compatibility.

    def __rfloordiv__(self, other):
        return Unum.uniform(other).__floordiv__(self)

    def __rpow__(self, other):
        return Unum.uniform(other).__pow__(self)

    def __getitem__(self, index):
        return Unum(self._value[index], self._unit)

    def __setitem__(self, index, value):
        u = Unum.uniform(value)
        self._value[index] = u.asNumber(Unum(1, self._unit))

    def __len__(self):
        return len(self._value)

    def __str__(self):
        return self.formatter.format(self)

    __repr__ = __str__

    def __getstate__(self):
        return self._value, self._unit, self._normal

    def __setstate__(self, state):
        self._value, self._unit, self._normal = state


class Unit(Unum):
    def __init__(self, symbol, definition, name=''):
        """
        :param str symbol: symbolic presentation of unit, e.g. m, s, kg
        :param definition:
            0 if self represents a basic unit
            unum equivalent to self, expressed in other unit(s) if self represents a derived unit

        :param name: the unit full name if self represents a basic unit
        :raises UnumError: if definition is a unum although unit and value do not represent a basic unit

        """

        super(Unit, self).__init__(1, {symbol: 1})

        if symbol in Unum._unitTable:
            raise NameConflictError(symbol)

        self._normal = True

        if definition == BASIC_UNIT:
            conv_unum = None
            level = 0
        else:
            conv_unum = Unum.uniform(definition)
            level = conv_unum.maxLevel() + 1
            conv_unum._normal = True

        Unum._unitTable[symbol] = conv_unum, level, name
