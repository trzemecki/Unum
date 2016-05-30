"""
Main Unum module.
"""

import collections
from .exceptions import *


BASIC_UNIT = 0

UnitDefinition = collections.namedtuple('UnitDefinition', 'definition,level,name')


class UnitTable(dict):
    def reset(self, unitTable=None):
        self.clear()
        if unitTable is not None:
            self.update(unitTable)

    def get_definition(self, symbol):
        return self[symbol].definition

    def is_basic(self, symbol):
        return self[symbol].definition is None

    def is_derived(self, symbol):
        return not self.is_basic(symbol)

    def new_unit(self, symbol, definition, name):
        if symbol in self:
            raise NameConflictError(symbol)

        if definition == BASIC_UNIT:
            conv_unum = None
            level = 0
        else:
            conv_unum = Unum.uniform(definition)
            conv_unum._normal = True
            level = conv_unum.maxLevel() + 1

        self[symbol] = UnitDefinition(conv_unum, level, name)

        return Unum(1, {symbol: 1}, normal=True)


UNIT_TABLE = UnitTable()

new_unit = UNIT_TABLE.new_unit


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

        units = sorted(unit.items())

        formatted = (
            self._format_only_mul_separator(units) if not self._div else
            self._format_with_div_separator(units)
        )

        return '' if not formatted and self._hide_empty else self._unit_format % formatted

    def _format_only_mul_separator(self, units):
        return self._mul.join(self._format_exponent(u, exp) for u, exp in units)

    def _format_with_div_separator(self, units):
        return self._div.join([
            self._mul.join(self._format_exponent(u, exp) for u, exp in units if exp > 0) or '1',
            self._mul.join(self._format_exponent(u, -exp) for u, exp in units if exp < 0)
        ]).rstrip(self._div + '1')

    def _format_exponent(self, symbol, exp):
        return symbol + (str(exp) if exp != 1 else '')

    def format_value(self, value):
        return self._value_format % value

    def format(self, unum):
        """
        Return our string representation, normalized if applicable.

        Normalization occurs if Unum.AUTO_NORM is set.
        """
        if self._auto_norm and not unum._normal:
            unum.simplify_unit(True)
            unum._normal = True

        return self._indent.join([self.format_value(unum._value), self.format_unit(unum._unit)]).strip()


def uniform_unum(func):
    def decorator(self, value):
        return func(self, Unum.uniform(value))

    return decorator


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

    __slots__ = ('_value', '_unit', '_normal')

    @classmethod
    def set_format(cls, **kwargs):
        cls.formatter = Formatter(**kwargs)

    @classmethod
    def reset_format(cls):
        cls.formatter = Formatter()

    def __init__(self, value, unit, normal=False):
        """
        :param value: number or other object represents the mathematical value (e.g. numpy array)
        :param dict unit: {unit symbol : exponent} for example for 1 m/s2 should give {'m': 1, 's': -2}
        """

        self._value = value
        self._unit = dict(unit)
        self._normal = normal

    @property
    def unit(self):
        return self.formatter.format_unit(self._unit)

    def copy(self, normalized=False):
        """
        Return a copy of this Unum, normalizing the copy if specified.
        """

        result = Unum(self._value, self._unit.copy())

        if normalized:
            result.simplify_unit()

        return result

    @uniform_unum
    def cast_unit(self, other):
        """
        Return a Unum with this Unum's value and the units of the given Unum.

        Raises IncompatibleUnitsError if self can't be converted to other.
        Raises NonBasicUnitError if other isn't a basic unit.
        """

        if not other.is_basic():
            raise NonBasicUnitError(other)

        s, o = self.matchUnits(other)
        res = Unum(s._value / o._value, other._unit)
        res._normal = True

        return res

    def is_basic(self):
        return self._value == 1

    def replaced(self, symbol, definition):
        """
        Return a Unum with the string u replaced by the Unum conv_unum.

        If u is absent from self, a copy of self is returned.
        """

        exponent = self._unit[symbol]

        res = self.copy() * definition ** exponent
        del res._unit[symbol]
        return res

    def simplify_unit(self, forDisplay=False):
        """
        Normalize our units IN PLACE and return self.

        Substitutions may be applied to reduce the number of different units,
        while making the fewest substitutions.

        If forDisplay is True, then prefer a single unit to no unit.
        """
        
        # TODO: example of forDisplay.
        # TODO: simplify normalize so it fits in 80 columns...

        previous_length = len(self._unit)
        new_subst_unums = [({}, self.copy())]

        while new_subst_unums:
            subst_unums, new_subst_unums = new_subst_unums, []
            for subst_dict, subst_unum in subst_unums:
                for symbol, exponent in subst_unum._derived_units():
                    new_subst_dict = subst_dict.copy()
                    new_subst_dict[symbol] = exponent + new_subst_dict.get(symbol, 0)

                    if all(new_subst_dict != subst_dict2 for subst_dict2, subst_unum2 in new_subst_unums):
                        reduced = subst_unum.replaced(symbol, UNIT_TABLE.get_definition(symbol)) # replace by definition
                        new_subst_unums.append((new_subst_dict, reduced))

                        new_length = len(reduced._unit)
                        if new_length < previous_length and not (forDisplay and new_length == 0 and previous_length == 1):
                            self._value, self._unit = reduced._value, reduced._unit
                            previous_length = new_length
        return self

    def _derived_units(self):
        return [(symbol, self._unit[symbol]) for symbol in self._unit if UNIT_TABLE.is_derived(symbol)]

    def assert_no_unit(self):
        """
        :raises ShouldBeUnitlessError: if self has a unit
        """

        if self._unit:
            raise ShouldBeUnitlessError(self)  # TODO consider other way to signalize it

    def maxLevel(self):
        """
        :return: the maximum level of self's units
        """
        
        return max([0] + [UNIT_TABLE[symbol].level for symbol in self._unit])

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
            s.assert_no_unit()
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
        o.simplify_unit()

        if o._unit:
            raise IncompatibleUnitsError(self, other)

        o._unit = s._unit

        if revert:
            s, o = o, s

        return s, o

    @uniform_unum
    def __add__(self, other):
        s, o = self.matchUnits(other)
        return Unum(s._value + o._value, s._unit)

    @uniform_unum
    def __sub__(self, other):
        s, o = self.matchUnits(other)
        return Unum(s._value - o._value, s._unit)

    def __pos__(self):
        return self

    def __neg__(self):
        return Unum(-self._value, self._unit)

    @uniform_unum
    def __mul__(self, other):
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

    @uniform_unum
    def __div__(self, other):
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

    @uniform_unum
    def __floordiv__(self, other):
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

    @uniform_unum
    def __pow__(self, other):
        if other._value:
            other = other.copy(True)
            other.assert_no_unit()
            unit = self._unit.copy()
            for u in list(self._unit.keys()):
                unit[u] *= other._value
        else:
            unit = Unum._NO_UNIT
        return Unum(self._value ** other._value, unit)

    @uniform_unum
    def __lt__(self, other):
        s, o = self.matchUnits(other)
        return s._value < o._value

    @uniform_unum
    def __le__(self, other):
        s, o = self.matchUnits(other)
        return s._value <= o._value

    @uniform_unum
    def __gt__(self, other):
        s, o = self.matchUnits(other)
        return s._value > o._value

    @uniform_unum
    def __ge__(self, other):
        s, o = self.matchUnits(other)
        return s._value >= o._value

    @uniform_unum
    def __eq__(self, other):
        s, o = self.matchUnits(other)
        return s._value == o._value

    @uniform_unum
    def __ne__(self, other):
        s, o = self.matchUnits(other)
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

    @uniform_unum
    def __radd__(self, other):
        return other.__add__(self)

    @uniform_unum
    def __rsub__(self, other):
        return other.__sub__(self)

    @uniform_unum
    def __rmul__(self, other):
        return other.__mul__(self)

    @uniform_unum
    def __rdiv__(self, other):
        return other.__div__(self)

    __rtruediv__ = __rdiv__  # Python 3.0 compatibility.

    @uniform_unum
    def __rfloordiv__(self, other):
        return other.__floordiv__(self)

    @uniform_unum
    def __rpow__(self, other):
        return other.__pow__(self)

    def __getitem__(self, index):
        return Unum(self._value[index], self._unit)

    def __setitem__(self, index, value):
        self._value[index] = Unum.uniform(value).asNumber(Unum(1, self._unit))

    def __len__(self):
        return len(self._value)

    def __str__(self):
        return self.formatter.format(self)

    __repr__ = __str__

    def __getstate__(self):
        return self._value, self._unit, self._normal

    def __setstate__(self, state):
        self._value, self._unit, self._normal = state
