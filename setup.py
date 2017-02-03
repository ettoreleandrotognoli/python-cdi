# -*- encoding: utf-8 -*-
__author__ = 'ettore'

import os

from setuptools import setup, find_packages

from pycdi import __version__


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


requirements = []
str_version = '.'.join(map(str, __version__))

setup(
    name='pycdi',
    version=str_version,
    description='Python Code Dependency Injection',
    long_description=read('README.rst'),
    url='https://github.com/ettoreleandrotognoli/python-cdi',
    download_url='https://github.com/ettoreleandrotognoli/python-cdi/tree/%s/' % str_version,
    license='BSD',
    author=u'Éttore Leandro Tognoli',
    author_email='ettore.leandro.tognoli@gmail.com',
    packages=find_packages(exclude=['tests','examples']),
    include_package_data=True,
    keywords=['cdi','di','code dependency injection','dependency injection'],
    classifiers=[
        'Operating System :: OS Independent',        
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: BSD License',
    ],
    install_requires=[
        'six',
    ],
    # tests_require=[],
)
