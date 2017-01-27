# -*- encoding: utf-8 -*-
import unittest

from pycdi.core import CDIContainer, CDIDecorator


class InterfaceCDITest(unittest.TestCase):
    def test_methods(self):
        container = CDIContainer()
        with self.assertRaises(NotImplementedError):
            container.call(None)
        with self.assertRaises(NotImplementedError):
            container.produce(None)
        with self.assertRaises(NotImplementedError):
            container.get_producer()
        with self.assertRaises(NotImplementedError):
            container.register_instance(None)
        with self.assertRaises(NotImplementedError):
            container.register_producer(None)

    def test_decorator(self):
        with self.assertRaises(NotImplementedError):
            CDIDecorator()()
