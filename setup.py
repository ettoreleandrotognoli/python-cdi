__version__ = '0.1.devSNAPSHOT'

import os

from setuptools import setup, find_packages


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()



setup(
    name='pycdi',
    version=__version__,
    description='Python Code Dependency Injection',
    long_description=read('README.rst'),
    url='https://github.com/ettoreleandrotognoli/python-cdi',
    download_url='https://github.com/ettoreleandrotognoli/python-cdi/tree/%s/' % __version__,
    license='BSD',
    author='Éttore Leandro Tognoli',
    author_email='ettore.leandro.tognoli@gmail.com',
    packages=find_packages(exclude=['tests', 'examples']),
    include_package_data=True,
    keywords=[
        'cdi',
        'di',
        'code dependency injection',
        'dependency injection'
    ],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: BSD License',
    ],
    install_requires=[
    ],
    tests_require=[
    ],
)
