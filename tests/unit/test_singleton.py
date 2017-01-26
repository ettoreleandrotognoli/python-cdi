# -*- encoding: utf-8 -*-
import unittest

from pycdi.core import DEFAULT_CONTAINER
from pycdi.utils import Singleton


@Singleton(limit=1)
class SingletonClass(object):
    counter = 0

    def __init__(self):
        self.index = SingletonClass.counter
        SingletonClass.counter += 1


class SingletonTest(unittest.TestCase):
    def test_unique(self):
        obj1 = DEFAULT_CONTAINER.produce(SingletonClass)
        obj2 = DEFAULT_CONTAINER.produce(SingletonClass)
        self.assertEqual(obj1, obj2)
        self.assertEqual(obj1.index, obj2.index)
