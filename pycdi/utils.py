# -*- encoding: utf-8 -*-
import random

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
