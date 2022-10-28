Unum 5.0 (fork) - Units in Python 
==========================
&copy; 2000-2003 Pierre Denis<br/>
&copy; 2009-2010 Chris MacLeod<br/>
&copy; 2016-2017      Leszek Trzemecki<br/>

Version info
-------------------------------------------------------------------------

  - This repository is cloned from: http://bitbucket.org/kiv/unum/
  - Version is not compatible with previous `unum` (**no backward compatibility**)
  - Unicode using by default; units exponents are displaying using unicode superscript
  - New module function allowing using alternatively `float`, `int` or `Unum`  

License
--------

Library is distributed under **GNU LGPL** license (see `LICENSE.txt` file)

Installation
-------------------------------------------------------------------------
### Using pip
If you have not git yet, first install it from https://git-scm.com/downloads, and then run

```{r, engine='bash', count_lines}
    pip install git+https://github.com/trzemecki/Unum.git
```

### Alternatively
unzip Unum installation files to any directory.

```{r, engine='bash', count_lines}
    cd <install-directory>
    python setup.py install
```

this will install Unum packages in your Python site-packages directory
i.e. it will create the directory `<python-site-packages-dir>`/unum 
if the installation is successful (see below),
you can safely remove `<your-install-directory>`

Introduction
-------------------------------------------------------------------------

Unum stands for 'unit-numbers'. It is a Python module that allows you to define and manipulate quantities with units attached such as 60 seconds, 500 watts, 42 miles-per-hour, 100 kg per square meter, 14400 bits per second, 30 dollars, and so on. 

Features include:
- Exceptions for incorrect use of units.
- Automatic and manual conversion between compatible units.
- Easily extended to arbitrary units.
- Integration with any type supporting arithmetic operations, including Numpy arrays and standard library types like complex and fractions.Fraction.
- Customizable output formatting.

Example
-------------------------------------------------------------------------

For a simple example, let's can calculate Usain Bolt's average speed during his record-breaking performance in the 2008 Summer Olympics

    >>> from unum.units import * # Load a number of common units.
    >>> distance = 100*m
    >>> time = 9.683*s
    >>> speed = distance / time
    >>> speed
    10.3273778788 [m/s]
    >>> speed.asUnit(mile/h)
    23.1017437978 [mile/h]
    
If we do something dimensionally incorrect, we get an exception rather than silently computing a correct result. Let's try calculating his kinetic energy using an erroneous formula

    >>> KE = 86*kg * speed / 2 # Should be speed squared!
    >>> KE.cast_unit(J)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "unum\__init__.py", line 171, in asUnit
        s, o = self.matchUnits(other)
      File "unum\__init__.py", line 258, in matchUnits
        raise IncompatibleUnitsError(self, other)
    unum.IncompatibleUnitsError: [kg.m/s] can't be used with [J]
    
The exception pinpoints the problem, allowing us to examine the units and fix the formula

    >>> KE = 86*kg * speed**2 / 2
    >>> KE.cast_unit(J)
    4586.15355558 [J]

Unum will also report errors in attempting to add incompatible units

    >>> 1*s + 2*kg
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "unum\__init__.py", line 269, in __add__
        s, o = self.matchUnits(Unum.coerceToUnum(other))
      File "unum\__init__.py", line 258, in matchUnits
        raise IncompatibleUnitsError(self, other)
    unum.IncompatibleUnitsError: [s] can't be converted to [kg]

and when units are present in operations that don't expect them, such as the second part of an exponentiation

    >>> 2 ** (2*m)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "unum\__init__.py", line 398, in __rpow__
        return Unum.coerceToUnum(other).__pow__(self)
      File "unum\__init__.py", line 332, in __pow__
        other.checkNoUnit()
      File "unum\__init__.py", line 230, in checkNoUnit
        raise ShouldBeUnitlessError(self)
    unum.ShouldBeUnitlessError: expected unitless, got 2 [m]

Unums are automatically coerced back to regular numbers where legal and desirable. Here log10 expects a plain integer or float

    >>> math.log10((1000 * m) / (10 * m)) # Units cancel, so it's ok.
    2.0

Usage
-------------------------------------------------------------------------

Unums are ordinary Python objects and support all the mathematical operations available in Python using the same syntax as usual

    >>> 1*m + 2*m
    3 [m]
    >>> 3*m * 4*m
    12 [m2]
    >>> abs(-5*m)
    5 [m]
    >>> 6*m > 5*m
    True 
    >>> 5*m ** 3
    5 [m3]   
    >>> (5*m) ** 3
    125 [m3]

Note how the parentheses in the last example makes the exponentiation apply to the whole number rather than just the "m".

If you are using Python 2.x, be very careful with the way division works

    >>> 1 / 3 * (m/s)
    0 [m/s]
    >>> 1.0 / 3 * (m/s)
    0.333333333333 [m/s]

Dividing two integers truncates the remainder to produce another integer, while dividing two floats produces another float. In Python 3.x, division with the / operator always produces a float, and the // operator always performs integer division.

It's possible to have Unums where all the units have cancelled; these are conceptually the same as a raw number, and can be used accordingly

    >>> two = (2 * m) / m
    >>> two
    2 []
    >>> 5**two
    25 []
    >>> import math
    >>> math.log(two)
    0.69314718055994529

What's happening here is that when math.log wants a plain number, it coerces (converts) the Unum into a plain number. You can do this manually using Python's builtin functions

    >>> int(two)
    2
    >>> float(two)
    2.0
       
Another way to get at the value inside the Unum is with the `number` method, which allows you to do a conversion at the same time

    >>> speed.number(mile/h) # Get the value in mile/h
    23.101743797879877
    >>> speed.number() # Get the value in the current units
    10.3273778788

Standard library integration
-------------------------------------------------------------------------

The standard library types complex and Fraction can be used with Unum transparently

    >>> length = 1j * m # One imaginary meter.
    >>> length
    1j [m]
    >>> length ** 2 # j * j == -1
    (-1+0j) [m2]

    >>> from fractions import Fraction
    >>> Fraction(1, 3) * S
    1/3 [s]
    >>> Fraction(1,2) * S + Fraction(1,3) * S
    5/6 [s]

Unums are picklable, so you can store them into files or databases as usual; see the "pickle" and "shelve" modules in the Python standard library for more details.

Numpy integration
-------------------------------------------------------------------------

Unum works with Numpy with a couple caveats. First, there is a difference between left-multiplying and right-multiplying with an Unum

    >>> from numpy import array
    >>> array([2,3,4]) * m  # note that meters is on the right here
    array([2 [m], 3 [m], 4 [m]], dtype=object)
    >>> m * array([2,3,4])  # this time meters is on the left
    [2 3 4] [m]
    
Right-multiplying produces an array of Unum objects, which is often undesirable since each Unum object takes up more memory than a simple number does. However, this does allow the objects to be different types, if you so desire.

Generally, a better idea is to use left-multiplication, which produces a single Unum object containing the array as its value. This is memory-efficient, but constrains all the objects in the array to be the same type.
  
Another way to get the effect of left-multiplication is to use the provided unum.uarray helper function, which turns an array-like object into a unitless Unum, which you can then multiply on the right as normal

    >>> from unum import uarray
    >>> uarray([2,3,4])
    [2 3 4] []
    >>> uarray([2,3,4]) * m
    [2 3 4] [m]

The second caveat is most of NumPy's universal functions don't work on Unums, even if they are unitless. Arithmetic operators work, but trigonometric functions do not

    >>> lengths = m * [2,3,4]
    >>> lengths
    [2, 3, 4] [m]
    >>> length + 1
    [3, 4, 5] [m]
    >>> cos(lengths)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: cos    

Luckily, you can extract the value of any Unum using the `number` method, allowing you to use the array inside

    >>> cos(lengths.number())
    array([-0.41614684, -0.9899925 , -0.65364362])  

If anyone has ideas on improving integration with Unum, I'd love to hear from you.

Defining New Units
-------------------------------------------------------------------------

Creating new units is done with a single function call. Imagine you want to define a new unit called 'spam', with derived units 'kilospam', 'millispam', and 'sps' (spam per second)

    >>> from unum import new_unit
    >>> SPAM = new_unit('spam')

Now the variable SPAM refers to a Unum representing one 'spam'. The name of the variable is arbitrary, and the same Unum can have multiple names

    >>> spam = SPAM
    >>> spam
    1 [spam]

Here both spam and SPAM can be used interchangeably to refer to the same thing.
Derived units are defined in relation to this base unit
    
    >>> KSPAM = new_unit('kilospam', 1000 * SPAM)
    >>> MSPAM = new_unit('millispam', 0.001 * SPAM)
    >>> SPS = new_unit('sps', SPAM / S)
    
The second argument provided is the definition of the derived unit in terms of previously defined units. Note that the variable name is arbitrary and independent of the longer symbol used. Now you can work with 'spammed' quantities.

    >>> (500 * MSPAM).cast_unit(SPAM)
    0.5 [spam]
    >>> (5000 * MSPAM).cast_unit(SPAM)
    5.0 [spam]
    >>> SPS.cast_unit(MSPAM/S)
    1000.0 [millispam/s]
    >>> 5*SPS * 20*S
    100 [spam]
    >>> (10*SPS)**2
    100 [sps2]

Importing units
-------------------------------------------------------------------------

You can keep your favorite units in a normal Python module, and then import that module to have them available anywhere. A module containing your 'spam' units could be as simple as

    # my_spam.py
    from unum.units import *
    from unum import new_unit

    SPAM = new_unit('spam')
    KSPAM = new_unit('kilospam', 1000 * SPAM)
    MSPAM = new_unit('millispam', 0.001 * SPAM)
    SPS = new_unit('sps', SPAM / S)

Placing this module anywhere on your Python path will allow you to do

    >>> from my_spam import *

and have your units available.

Predefined units
-------------------------------------------------------------------------

Unum comes with the standard SI units as well as some other widely used units. You can browse the "units" folder in the "unum" folder to see what's available. If you want to contribute more units, feel free to submit them.

Advanced usage
-------------------------------------------------------------------------

### Custom formatting

The string representation of Unums can be configured by modifying the variables of the Unum class:

    >>> Unum.set_format(
    ...     mul_separator=' ',
    ...     div_separator='',
    ...     unit_format='%s',
    ...     value_format='%15.7f',
    ...     unitless='', # hide empty
    ...     superscript=False)
    
    >>> M
    1.0000000 m
    >>> 25 * KG*M/S**2
    25.0000000 kg m s-2
    >>> M/ANGSTROM
    10000000000.0000000
    >>>
    
See the docstrings in the class for more detail.    
  
### Normalization

By default, Unum will find the shortest unit representation among equivalent expressions, by applying the known unit conversion rules. This is called normalization. For example a pressure given in Pascal multiplied by a surface will give a force in Newton, since one Pascal is equal, by definition, to a Newton per square meter

    >>> Pa * m**2
    1 [N]
    
This behavior can be controlled by a flag on the Unum class

    >>> Unum.set_format(auto_norm=False)
    >>> Pa * m**2
    1 [Pa.m2]
    
Then you must manually normalize by calling the normalize method

    >>> x = Pa * m**2
    >>> x
    1 [Pa.m2]
    >>> x.simplify_unit()
    1 [N]
    >>> x
    1 [N]
    
Note that normalize permanently modifies the instance itself as a side-effect.

Running tests
-------------------------------------------------------------------------
```{r, engine='bash', count_lines}
  cd <install-directory>
  python setup.py test
```
