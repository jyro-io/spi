from setuptools import setup

setup(
    name='spi',
    version='2.1.0',
    packages=['spi',],
    license='GPLv3',
    long_description=open('README.md').read(),
    # https://github.com/pypa/setuptools/issues/987#issuecomment-318349568
    install_requires=[
        'pytprint',
        'pymongo',
        'requests',
        'pysimdjson'
    ],
    dependency_links=[
        'git+https://github.com/rory-linehan/pytprint.git@0.2.5#egg=pytprint-0.2.5'
    ],
)
