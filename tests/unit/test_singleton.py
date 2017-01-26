# -*- encoding: utf-8 -*-
import unittest

from pycdi.core import DEFAULT_CONTAINER
from pycdi.utils import Singleton, SequentialStrategy, random_strategy

SINGLETON_LIMIT = 10


@Singleton(limit=1)
class SingletonClass(object):
    counter = 0

    def __init__(self):
        self.index = SingletonClass.counter
        SingletonClass.counter += 1


@Singleton(limit=SINGLETON_LIMIT, strategy=SequentialStrategy)
class SequentialClass(object):
    counter = 0

    def __init__(self):
        self.index = SequentialClass.counter
        SequentialClass.counter += 1


@Singleton(limit=SINGLETON_LIMIT, strategy=random_strategy)
class RandomClass(object):
    counter = 0

    def __init__(self):
        self.index = SequentialClass.counter
        SequentialClass.counter += 1


class SingletonTest(unittest.TestCase):
    def test_unique(self):
        obj1 = DEFAULT_CONTAINER.produce(SingletonClass)
        obj2 = DEFAULT_CONTAINER.produce(SingletonClass)
        self.assertEqual(obj1, obj2)
        self.assertEqual(obj1.index, obj2.index)

    def test_sequential(self):
        singletons = [DEFAULT_CONTAINER.produce(SequentialClass) for x in range(SINGLETON_LIMIT)]
        self.assertEqual(len(singletons), len(set(singletons)))
        singletons += [DEFAULT_CONTAINER.produce(SequentialClass) for x in range(SINGLETON_LIMIT)]
        self.assertNotEqual(len(singletons), len(set(singletons)))
        self.assertEqual(len(set(singletons)), SINGLETON_LIMIT)

    def test_random(self):
        singletons = []
        for i in range(SINGLETON_LIMIT):
            singletons = list(singletons)
            singletons += [DEFAULT_CONTAINER.produce(RandomClass) for x in range(SINGLETON_LIMIT)]
            singletons = set(singletons)
            self.assertLessEqual(len(singletons), SINGLETON_LIMIT)

        self.assertAlmostEqual(len(singletons), SINGLETON_LIMIT)
