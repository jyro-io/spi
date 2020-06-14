# Copyright 2020 Rory Linehan
# this code is distributed under the terms of the GNU General Public License

from distutils.core import setup

setup(
    name='pytprint',
    py_modules=['pytprint.py',],
    license='GNU GPL',
    long_description=open('README.md').read(),
    dependency_links=['http://github.com/user/repo/tarball/master#egg=package-1.0'],
)
