import sys
try:
    from setuptools import setup
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup
    
extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True
    
setup(name = "Unum",
      version = "4.1.1",
      description  = "Units in Python",
      author = "Chris MacLeod, Pierre Denis",
      author_email = "ChrisM6794@gmail.com",
      url = "http://bitbucket.org/kiv/unum/",
      license = "LGPLv3",
      setup_requires=['nose>=0.11'],
      test_suite = "nose.collector",
      packages = ('unum',
                  'unum.units',
                  'unum.units.custom',
                  'unum.units.others',
                  'unum.units.si',
                  'tests',
                  ),
      **extra
      
)
