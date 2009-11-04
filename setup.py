import ez_setup
ez_setup.use_setuptools()
from setuptools import setup

setup(name = "Unum",
      version = "4.1.0",
      description  = "Units in Python",
      author = "Chris MacLeod, Pierre Denis",
      author_email = "ChrisM6794@gmail.com",
      url = "http://bitbucket.org/kiv/unum/",
      license = "LGPL",
      setup_requires=['nose>=0.11'],
      test_suite = "nose.collector",
      packages = ('unum',
                  'unum.units',
                  'unum.units.custom',
                  'unum.units.others',
                  'unum.units.si',
      )
)
