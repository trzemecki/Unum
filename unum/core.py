from __future__ import division, unicode_literals

import collections

import six

from .exceptions import *

BASIC_UNIT = 0

UnitDefinition = collections.namedtuple('UnitDefinition', ['definition', 'level', 'name'])


class UnitTable(dict):
    def reset(self, table=None):
        self.clear()

        if table is not None:
            self.update(table)

    def get_definition(self, symbol):
        return self[symbol].definition

    def is_basic(self, symbol):
        return self[symbol].definition is None

    def is_derived(self, symbol):
        return not self.is_basic(symbol)

    def new_unit(self, symbol, definition=BASIC_UNIT, name=''):
        if symbol in self:
            raise NameConflictError(symbol)

        if definition == BASIC_UNIT:
            equivalent = None
            level = 0
        else:
            equivalent = Unum.uniform(definition)
            equivalent._normal = True
            level = equivalent.max_level() + 1

        self[symbol] = UnitDefinition(equivalent, level, name)

        return Unum(1, {symbol: 1}, normal=True)


UNIT_TABLE = UnitTable()

new_unit = UNIT_TABLE.new_unit


_SUPERSCRIPT_NUMBERS = {
    '0': '\u2070',
    '1': '\u00B9',
    '2': '\u00B2',
    '3': '\u00B3',
    '4': '\u2074',
    '5': '\u2075',
    '6': '\u2076',
    '7': '\u2077',
    '8': '\u2078',
    '9': '\u2079',
    '-': '\u207B',
}

_DOT = '\u00B7'


class Formatter(object):
    DEFAULT_CONFIG = dict(
        mul_separator=_DOT,
        div_separator='/',
        unit_format='[%s]',
        value_format='%s',
        indent=' ',
        unitless='[-]',
        auto_norm=False,
        unit=None,
        superscript=True,
        always_display_number=False,
    )

    def __init__(self, **kwargs):
        self._config = self.DEFAULT_CONFIG.copy()
        self.configure(**kwargs)

    def configure(self, **kwargs):
        not_allowed_keywords = set(kwargs) - set(self._config)

        if not_allowed_keywords:
            raise TypeError("Not allowed keywords: %s" % ', '.join(not_allowed_keywords))

        self._config.update(kwargs)

    def __getitem__(self, item):
        return self._config[item]

    def format_unit(self, value):
        return value.format_unit(self._format_unit)

    def _format_unit(self, unit):
        """
        Return a string representation of our unit.
        """

        units = sorted(unit.items())

        formatted = (
            self._format_only_mul_separator(units) if not self['div_separator'] else
            self._format_with_div_separator(units)
        )

        return self['unitless'] if not formatted else self['unit_format'] % formatted

    def _format_only_mul_separator(self, units):
        return self['mul_separator'].join(self._format_exponent(u, exp) for u, exp in units)

    def _format_with_div_separator(self, units):
        return self['div_separator'].join([
            self['mul_separator'].join(self._format_exponent(u, exp) for u, exp in units if exp > 0) or '1',
            self['mul_separator'].join(self._format_exponent(u, -exp) for u, exp in units if exp < 0)
        ]).rstrip(self['div_separator'] + '1')

    def _format_exponent(self, symbol, exp):
        if exp != 1:
            exp_text = six.text_type(exp)

            if self['superscript']:
                exp_text = ''.join([_SUPERSCRIPT_NUMBERS.get(c, c) for c in exp_text])
        else:
            exp_text = ''

        return symbol + exp_text

    def format_number(self, value):
        return value.format_number(self._format_number)

    def _format_number(self, value):
        return self['value_format'] % value

    def format(self, value):
        """
        Return our string representation, normalized if applicable.

        Normalization occurs if Unum.AUTO_NORM is set.
        """
        value = Unum.uniform(value)

        if self['auto_norm'] and not value._normal:
            value.simplify_unit(True)
            value._normal = True

        if self['unit'] is not None:
            value = value.cast_unit(self['unit'])

        if not self['always_display_number'] and value.is_unit():
            return self.format_unit(value)

        return self['indent'].join([self.format_number(value), self.format_unit(value)]).strip()

    __call__ = format


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

    __slots__ = ('_value', '_unit', '_normal')

    @staticmethod
    def uniform(value):
        """
        Return a unitless Unum if value is a number.

        If value is a Unum already, it is returned unmodified.
        """
        if isinstance(value, Unum):
            return value
        else:
            return Unum(value)

    formatter = Formatter()

    @classmethod
    def set_format(cls, **kwargs):
        cls.formatter = Formatter(**kwargs)

    @classmethod
    def reset_format(cls):
        cls.formatter = Formatter()

    def __init__(self, value, unit=None, normal=False):
        """
        :param value: number or other object represents the mathematical value (e.g. numpy array)
        :param dict unit: {unit symbol : exponent} for example for 1 m/s2 should give {'m': 1, 's': -2}
        """

        self._value = value
        self._unit = {} if unit is None else dict(unit)
        self._normal = normal

    def unit(self):
        return Unum(1, self._unit.copy())

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

        s, o = self.match_units(other)
        res = Unum(s._value / o._value, other._unit)
        res._normal = True

        return res

    def is_basic(self):
        return self._value == 1

    is_unit = is_basic

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

    def max_level(self):
        """
        :return: the maximum level of self's units
        """

        return max([0] + [UNIT_TABLE[symbol].level for symbol in self._unit])

    def number(self, unit=None):
        """
        Return the (normalized) raw value of self.

        If other is supplied, first convert to other's units before returning
        the raw value.

        Raises NonBasicUnitError if other is supplied, but has a value other
        than 1. (e.g., kg.number(2*g) is an error, but kg.number(g) is ok.)
        """

        if unit is None:
            return self.copy(True)._value

        if isinstance(unit, Unum):
            if not unit.is_unit():
                raise NonBasicUnitError(unit)

            s, o = self.match_units(unit)
            return s._value / o._value
        else:
            s = self.copy(True)
            s.assert_no_unit()
            return s._value / unit

    def match_units(self, other):
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
                  (s_length == o_length and s.max_level() < o.max_level()))

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

    def format_number(self, func):
        return func(self._value)

    def format_unit(self, func):
        return func(self._unit)

    @uniform_unum
    def __add__(self, other):
        s, o = self.match_units(other)
        return Unum(s._value + o._value, s._unit)

    @uniform_unum
    def __sub__(self, other):
        s, o = self.match_units(other)
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
            unit = None
        return Unum(self._value ** other._value, unit)

    @uniform_unum
    def __lt__(self, other):
        s, o = self.match_units(other)
        return s._value < o._value

    @uniform_unum
    def __le__(self, other):
        s, o = self.match_units(other)
        return s._value <= o._value

    @uniform_unum
    def __gt__(self, other):
        s, o = self.match_units(other)
        return s._value > o._value

    @uniform_unum
    def __ge__(self, other):
        s, o = self.match_units(other)
        return s._value >= o._value

    @uniform_unum
    def __eq__(self, other):
        try:
            s, o = self.match_units(other)
        except IncompatibleUnitsError:
            return False

        return s._value == o._value

    @uniform_unum
    def __ne__(self, other):
        try:
            s, o = self.match_units(other)
        except IncompatibleUnitsError:
            return True
        return s._value != o._value

    def __abs__(self):
        return Unum(abs(self._value), self._unit)

    def __complex__(self):
        return complex(self.number(1))

    def __int__(self):
        return int(self.number(1))

    def __long__(self):
        return int(self.number(1))

    def __float__(self):
        return float(self.number(1))

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
        self._value[index] = Unum.uniform(value).number(self.unit())

    def __len__(self):
        return len(self._value)

    def __bool__(self):
        return bool(self._value)

    __nonzero__ = __bool__

    def __str__(self):
        return self.formatter.format(self)

    __repr__ = __str__

    def __getstate__(self):
        return self._value, self._unit.copy(), self._normal

    def __setstate__(self, state):
        self._value, self._unit, self._normal = state
