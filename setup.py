#!/usr/bin/env python

from distutils.core import setup

setup(
    name         = 'opentestrobot',
    version      = '0.0',
    description  = 'Robot APIs for platform independent automated testing',
    author       = 'Antti Kervinen',
    author_email = 'antti.kervinen@intel.com',
    packages     = ['opentestrobot'],
    package_data = {'opentestrobot': ['__init__.py',
                                      'gesture.py',
                                      'vision.py',
                                      'interaction.py']})
