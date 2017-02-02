# -*- encoding: utf-8 -*-
import unittest

from pycdi.core import PyCDIContainer


class ContainerTest(unittest.TestCase):
    def test_simple_sub_container(self):
        container = PyCDIContainer()
        container.register_instance(1)
        self.assertEqual(container.produce(int), 1)
        sub_container = container.sub_container(2)
        self.assertEqual(container.produce(int), 1)
        self.assertEqual(sub_container.produce(int), 2)

    def test_complex_sub_container(self):
        container = PyCDIContainer()
        container.register_instance(0)
        container.register_instance(1, context='one')
        container.register_instance(2, context='two')
        self.assertEqual(container.produce(int), 0)
        self.assertEqual(container.produce(int, context='one'), 1)
        self.assertEqual(container.produce(int, context='two'), 2)
        sub_container = container.sub_container(1, one=[10, 1.0], three=3, four='four', five=[5, '5'])
        self.assertEqual(container.produce(int), 0)
        self.assertEqual(container.produce(int, context='one'), 1)
        self.assertEqual(container.produce(int, context='two'), 2)
        self.assertEqual(sub_container.produce(int), 1)
        self.assertEqual(sub_container.produce(int, context='one'), 10)
        self.assertEqual(sub_container.produce(float, context='one'), 1.0)
        self.assertEqual(sub_container.produce(int, context='two'), 2)
        self.assertEqual(sub_container.produce(int, context='three'), 3)
        self.assertEqual(sub_container.produce(str, context='four'), 'four')
        self.assertEqual(sub_container.produce(int, context='five'), 5)
        self.assertEqual(sub_container.produce(str, context='five'), '5')
