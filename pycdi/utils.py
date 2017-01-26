# -*- encoding: utf-8 -*-
from .core import CDIDecorator, DEFAULT_CONTAINER
import random

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
    def __init__(self, limit=1, strategy=SequentialStrategy, container=DEFAULT_CONTAINER):
        super(Singleton, self).__init__(container)
        self.limit = limit
        self.strategy = strategy() if isinstance(strategy, type) else strategy

    def __call__(self, clazz):
        def producer():
            instance = getattr(clazz, '_instance', None)
            if instance is None:
                instance = [self.container.call(clazz) for i in range(self.limit)]
                setattr(clazz, '_instance', instance)
            return self.strategy(instance)

        self.container.register_producer(producer, clazz)
        return clazz
