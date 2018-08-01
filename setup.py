#!/usr/bin/env python3
#
# Copyright (c) 2018-present, ph0x0en1x (ph0en1x.net).
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

"""The setup package to install RRouter with it's dependencies."""


from setuptools import setup, find_packages
with open('requirements.txt') as f:
    required = f.read().splitlines()
    
setup(
    name = 'RRouter',
    version = '0.1',
    packages = find_packages(),

    description = "Raspberry Pi Router/Server control scripts.",
    long_description = 'Raspberry Pi Router/Server control scripts.',

    author='ph0en1x',
    author_email='ph0x0en1x@gmail.com',
    url = 'https://ph0en1x.net',
    
    license = "LICENSE.txt",
    keywords = "raspberry pi server router script linux",
    
    platforms = ['linux', 'Raspbian'],
    install_requires=required,
    )