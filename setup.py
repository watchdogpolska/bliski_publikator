#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import bliski_publikator
version = bliski_publikator.__version__

setup(
    name='bliski_publikator',
    version=version,
    author='Adam Dobrawy',
    author_email='naczelnik@jawnosc.tk',
    packages=[
        'bliski_publikator',
    ],
    include_package_data=True,
    url='https://github.com/watchdogpolska/bliski_publikator',
    install_requires=[
        'Django>=1.7.10',
    ],
    zip_safe=False,
    scripts=['manage.py'],
)
