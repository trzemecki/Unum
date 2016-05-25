*************************************************************************
*                                                                       *
*                              Unum 4.2                                 *
*                           Units in Python                             *
*                                                                       *
*                      (c) 2000-2003 Pierre Denis                       *
*                      (c) 2009-2010 Chris MacLeod                      *
*                      (c) 2016      Leszek Trzemecki                   *
*                                                                       *
*************************************************************************

-------------------------------------------------------------------------
* Visible changes since Unum 4.0:
-------------------------------------------------------------------------

  - To support Python 2.5 and higher, the method Unum.as was renamed to
    Unum.asUnit; this was necessary since "as" became a reserved word.
    If you are still using old versions of Python, both names are
    available.

  - In addition to unit names in uppercase, unit names in the correct case
    are now available. So, both "kg" and "KG" refer to the kilogram Unum,
    and both "eV" and "EV" refer to the electron volt Unum.

  - Value types are no longer automatically coerced to floats. This allows
    the fractions.Fraction standard library type to be used, but may
    introduce incompatibilities with old code from integer vs. floating
    point division. In Python 3.x there is no problem.

  - Prefixed versions of the 7 base SI units are supplied. So you can use
    "cm", "ns", "kA", "mK", "pmol", "Mcd", and "g" out of the box.

-------------------------------------------------------------------------
* Prerequisites: 
-------------------------------------------------------------------------

  - Python 2.2 or higher. Python 3.x should work as well, but please
    report any bugs.

-------------------------------------------------------------------------
* To install Unum:
-------------------------------------------------------------------------
  Simple use:
  - pip install git+git://github.com/trzemecki/Unum.git

  Alternatively:
  - unzip Unum installation files to any directory.
  - cd <install-directory>
  - python setup.py install
    this will install Unum packages in your Python site-packages directory
    i.e. it will create the directory <python-site-packages-dir>/unum 
  - if the installation is successful (see below),
    you can safely remove <your-install-directory>

-------------------------------------------------------------------------
* To run the test cases:
-------------------------------------------------------------------------

  - cd <install-directory>
  - python setup.py test
    
-------------------------------------------------------------------------
* Other information :
-------------------------------------------------------------------------

  - Clone from: http://bitbucket.org/kiv/unum/


=========================================================================