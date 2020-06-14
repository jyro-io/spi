# Copyright 2020 Rory Linehan
# this code is distributed under the terms of the GNU General Public License

from distutils.core import setup

setup(
    name='spi',
    py_modules=['socrates_python_interface.py',],
    license='GNU GPL',
    long_description=open('README.md').read(),
    dependency_links=['git+https://github.com/rory-linehan/pytprint'],
    install_requires=[
        'pymongo',
    ],
)
