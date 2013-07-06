try:
    from ez_setup import use_setuptools
    use_setuptools()
except ImportError:
    pass

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__version_info__ = (4, 1, 3)
__version__ = '.'.join([str(v) for v in __version_info__])	
	
setup(name = "Unum",
      version = __version__,
      description  = "Units in Python",
      author = "Chris MacLeod, Pierre Denis",
      author_email = "ChrisM6794@gmail.com",
      url = "http://bitbucket.org/kiv/unum/",
      license = "LGPL",
      setup_requires=['nose>=0.11'],
	  py_modules=['ez_setup'],
      test_suite = "nose.collector",
      packages = ('unum',
                  'unum.units',
                  'unum.units.custom',
                  'unum.units.others',
                  'unum.units.si',
                  'tests',
      )
)
