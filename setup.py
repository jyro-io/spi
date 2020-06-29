# Copyright 2020 Rory Linehan
# this code is distributed under the terms of the GNU General Public License

from setuptools import setup

setup(
    name='spi',
    version='0.3.1',
    packages=['spi',],
    license='GNU GPL',
    long_description=open('README.md').read(),
    # https://github.com/pypa/setuptools/issues/987#issuecomment-318349568
    install_requires=[
        'pytprint',
        'pymongo',
        'requests'
    ],
    dependency_links=[
        'git+https://github.com/rory-linehan/pytprint.git@0.2.1#egg=pytprint-0.2.1'
    ],
)
