# -*- coding: utf-8 -*-
"""
ldrop - Data Recording Open-source Project library.
This setup.py is based on:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
https://github.com/infant-cognition-tampere/drop/blob/master/setup.py
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import platform

# Path to here to find README
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ldrop',
    version='0.0.1',
    description='Data Recording Open-source Project library',
    long_description=long_description,
    url='https://github.com/infant-cognition-tampere/ldrop',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Information Analysis',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent',
    ],

    # What does your project relate to?
    keywords='eye-tracking data sensor data-collection',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # TODO: Add proper dependencies
    #install_requires=['numpy==1.15.4',
    #install_requires=['numpy'
                      #'scipy',
                      #'pyee',
                      # FIXME: Maybe remove this later if PsychoPy developers
                      # fix their broken packaging. Newest PsychoPy requires
                      # Mac OS X specific packages on all operating systems
                      # ffs.
                      #'PsychoPy==1.85.3' if platform.system() == 'Linux' \
                      #'PsychoPy' if platform.system() == 'Linux' \
                      #        else 'PsychoPy',
                      #'pyglet',
                      #'pillow',
                      #'pygame',
                      #'moviepy',
                      #'yapsy',
                      #'configobj',
                      #'json_tricks'],
    install_requires=[],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={},

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        # Entry point for drop main
        #'console_scripts': [
        #    'drop = drop.Drop:main'
        #]
    },

    # To use nose2 to run your package???s tests, add the following
    tests_require=['nose2',
                   'unittest2',
                   'pep8',
                   'flake8'],  # TODO: Add flake8_docstring here
    test_suite='nose2.collector.collector',
)
