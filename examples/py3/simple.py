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
