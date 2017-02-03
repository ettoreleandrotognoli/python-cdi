=====
PyCDI
=====

.. image:: https://travis-ci.org/ettoreleandrotognoli/python-cdi.svg?branch=master
    :target: https://travis-ci.org/ettoreleandrotognoli/python-cdi

.. image:: https://codecov.io/gh/ettoreleandrotognoli/python-cdi/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ettoreleandrotognoli/python-cdi

.. image:: https://badge.fury.io/py/pycdi.svg
    :target: https://badge.fury.io/py/pycdi

.. image:: https://img.shields.io/pypi/dm/pycdi.svg
    :target: https://pypi.python.org/pypi/pycdi#downloads

A simple Python CDI ( Code Dependency Injection) Library.

The decorators of Python2 define the types and the contexts of the injections.
In the Python3 the types are defined with type-hints ( __annotations__ ) and the decorators defines the contexts.
The contexts are like the scopes (@Scope) of Java.

Install
-------

Install stable pycdi

.. code-block:: shell

    pip install pycdi

Install latest pycdi

.. code-block:: shell

    pip install git+https://github.com/ettoreleandrotognoli/python-cdi
    
Usage
-----



Python 2
~~~~~~~~

You can see more examples in the examples folder( examples/py2/ ).

.. code-block:: python

    import logging
    from logging import Logger
    
    from pycdi import Inject, Singleton, Producer
    from pycdi.shortcuts import call
    
    
    @Producer(str, _context='app_name')
    def get_app_name():
        return 'PyCDI'
    
    
    @Singleton(produce_type=Logger)
    @Inject(app_name=str, _context='app_name')
    def get_logger(app_name):
        return logging.getLogger(app_name)
    
    
    @Inject(logger=Logger)
    @Inject(name=str, _context='app_name')
    def main(name, logger):
        logger.info('I\'m starting...')
        print('Hello World!!!\nI\'m a example of %s' % name)
        logger.debug('I\'m finishing...')
    
    
    call(main)


Python 3
~~~~~~~~

You can see more examples in the examples folder( examples/py3/ ).

.. code-block:: python

    import logging
    from logging import Logger
    
    from pycdi import Inject, Singleton, Producer
    from pycdi.shortcuts import call
    
    
    @Producer(_context='app_name')
    def get_app_name() -> str:
        return 'PyCDI'
    
    
    @Singleton()
    @Inject(logger_name='app_name')
    def get_logger(logger_name: str) -> Logger:
        return logging.getLogger(logger_name)
    
    
    @Inject(name='app_name')
    def main(name: str, logger: Logger):
        logger.info('I\'m starting...')
        print('Hello World!!!\nI\'m a example of %s' % name)
        logger.debug('I\'m finishing...')
    
    
    call(main)





