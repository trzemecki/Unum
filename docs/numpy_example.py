from numpy import array
from unum.units import *

lengths = array([5,6,7,8])

print(lengths * M)
print(M * lengths)