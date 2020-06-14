# Copyright 2020 Rory Linehan
# this code is distributed under the terms of the GNU General Public License

from distutils.core import setup

setup(
    name='spi',
    version='0.2.0',
    packages=['spi',],
    license='GNU GPL',
    long_description=open('README.md').read(),
    dependency_links=['git+https://github.com/rory-linehan/pytprint'],
    install_requires=[
        'pymongo',
    ],
)
