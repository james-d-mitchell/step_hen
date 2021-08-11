# -*- coding: utf-8 -*-

# Copyright (c) 2021, J. D. Mitchell + Maria Tsalakou
#
# Distributed under the terms of the GPL license version 3.
#
# The full license is in the file LICENSE, distributed with this software.

"""
A rudimentary implementation of Stephen's procedure for inverse monoids.
"""

from setuptools import find_packages, setup

setup(
    name="step_hen",
    version="0.0.1",
    url="https://github.com/james-d-mitchell/step_hen",
    license="GPL3",
    author="James D. Mitchell, Maria Tsalakou",
    author_email="jdm3@st-andrews.ac.uk, mt200@st-andrews.ac.uk",
    description=(
        "A rudimentary implementation of Stephen's procedure for inverse monoids."
    ),
    long_description=open("README.rst").read(),
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
