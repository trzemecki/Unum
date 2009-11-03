# Example of a custom units file. To use, just place in your path
# and type::
#    from my_units import *

from unum.units import *
from unum import Unum

SPAM = Unum.unit('spam')
KSPAM = Unum.unit('kilospam', 1000 * SPAM)
MSPAM = Unum.unit('millispam', 0.001 * SPAM)
SPS = Unum.unit('sps', SPAM / S)