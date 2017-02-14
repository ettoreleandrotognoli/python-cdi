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


@Inject(name=(str, 'app_name'), logger=Logger)
def main(name, logger):
    logger.info('I\'m starting...')
    print('Hello World!!!\nI\'m a example of %s' % name)
    logger.debug('I\'m finishing...')


call(main)
