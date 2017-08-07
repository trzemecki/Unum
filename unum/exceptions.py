class UnumError(Exception):
    """
    A Unum error occurred that was unrelated to dimensional errors.
    """

    pass


class ShouldBeUnitlessError(TypeError):
    """
    An operation on a Unum failed because it had units unexpectedly.
    """

    def __init__(self, u):
        TypeError.__init__(self, "expected unitless, got %s" % u)


class IncompatibleUnitsError(TypeError):
    """
    An operation on two Unums failed because the units were incompatible.
    """

    def __init__(self, unit1, unit2):
        TypeError.__init__(
            self, "%s can't be converted to %s" % (unit1.unit(), unit2.unit())
        )


class ConversionError(UnumError):
    """
    Failed to convert a unit to the desired type.
    """

    def __init__(self, u):
        UnumError.__init__(self, "%s has no conversion" % u)


class NameConflictError(UnumError):
    """
    Tried to define a symbol that was already defined.
    """

    def __init__(self, unit_key):
        UnumError.__init__(self, "%s is already defined." % unit_key)


class NonBasicUnitError(UnumError):
    """
    Expected a basic unit but got a non-basic unit.
    """

    def __init__(self, u):
        UnumError.__init__(self, "%s not a basic unit" % u)