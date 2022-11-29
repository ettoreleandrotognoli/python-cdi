import glob
import random
import sys

import os

from .core import CDIDecorator, DEFAULT_CONTAINER

random_strategy = random.choice


class SequentialStrategy(object):
    def __init__(self):
        self.last_index = -1

    def __call__(self, options):
        self.last_index += 1
        self.last_index %= len(options)
        return options[self.last_index]


sequential_strategy = SequentialStrategy


class Singleton(CDIDecorator):
    def __init__(self, limit=1, produce_type=None, strategy=SequentialStrategy, container=DEFAULT_CONTAINER):
        super(Singleton, self).__init__(container)
        self.limit = limit
        self.strategy = strategy() if isinstance(strategy, type) else strategy
        self.produce_type = produce_type

    def __call__(self, decorated):
        def producer():
            instance = getattr(decorated, '_instance', None)
            if instance is None:
                instance = [self.container.call(decorated) for i in range(self.limit)]
                setattr(decorated, '_instance', instance)
            return self.strategy(instance)

        if self.produce_type is not None:
            produce_type = self.produce_type
        elif isinstance(decorated, type):
            produce_type = decorated
        elif hasattr(decorated, '__annotations__'):
            produce_type = decorated.__annotations__.get('return', object)
        else:
            produce_type = object
        self.container.register_producer(producer, produce_type)
        return decorated


class Provide(CDIDecorator):
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            return self.container.call(func, *args, **kwargs)

        return wrapper


def boot_cdi(paths=('*_cdi.py',), root=None):
    root = sys.path if root is None else root
    if isinstance(root, str):
        root = [root]
    libs = []
    for base_path in root:
        for path in paths:
            search_rule = os.path.join(base_path, path)
            for file_name in list(glob.iglob(search_rule)):
                file_name, ext = os.path.splitext(file_name)
                lib = '.'.join(filter(None, file_name[len(base_path):].split(os.sep)))
                libs.append(lib)
    return list(map(__import__, libs))
