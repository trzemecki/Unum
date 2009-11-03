from unum.units import *
from unum import Unum

# Defined units
KM   = Unum.unit('km' , 1000. * M )
CM   = Unum.unit('cm' ,   .01 * M )
GRAM = Unum.unit('g'  ,  .001 * KG)

# Constants
G            = 6.6720E-11 * N*M**2/KG**2
earth_mass   = 5.980E24 * KG
c            = 299792458 * M/S
earth_radius = 6.37E+06 * M

# Input data
distances = (5*CM, earth_radius, c * 365*24*H)
masses    = (5*GRAM, earth_mass, 1000*earth_mass)

# -- Processing and display

print "G            = %s" % G

print "Earth mass   = %s" % earth_mass

print "Earth radius = %s" % earth_radius.asUnit(KM)

print "distances    = %s" % str(distances)

print "masses       = %s" % str(masses)

print

for m1 in masses:

    for m2 in masses:

        if m1 >= m2:

           for d in distances:

               force = G*m1*m2/d**2

               a1 = force/m1

               a2 = force/m2

               print "m1 = %s, m2 = %s, d = %s" % (m1, m2, d)

               print "f = %s, a1 = %s, a2 = %s\n"

                     % (force.as(N), a1.as(M/S**2), a2.as(M/S**2))