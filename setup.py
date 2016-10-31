'''
crowdfunding: Module for webscraping crowd funding websites such as CrowdCube and KickStarter

Note that "python setup.py test" invokes pytest on the package. With appropriately
configured setup.cfg, this will check both xxx_test modules and docstrings.

Copyright 2016, Kieran Roberts.
Licensed under MIT.
'''
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest  # import here, because outside the required eggs aren't loaded yet
        sys.exit(pytest.main(self.test_args))


version = "0.1"

setup(name="crowdfunding",
      version=version,
      description="Module for webscraping crowd funding websites such as CrowdCube and KickStarter",
      long_description=open("README.rst").read(),
      classifiers=[ # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        'Programming Language :: Python'
      ],
      keywords="webscrape, mongdfunding", # Separate with spaces
      author="Kieran Roberts",
      author_email="kroberts012@gmail.com",
      url="http://github.com/kieranroberts/crowdfunding",
      license="MIT",
      packages=find_packages(exclude=['examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      tests_require=['pytest'],
      cmdclass={'test': PyTest}, 
      install_requires=['pymongo>=3.3.0', 'beautifulsoup4>=4.5.1', 'requests>=2.11.1'],
      entry_points={
        'console_scripts': 
            ['crowdfunding=crowdfunding:main']
      }
)
