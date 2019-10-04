# -*- encoding: utf-8 -*-
from pycdi import Inject
from pycdi.core import CDIContainer, CDIDecorator
from pycdi.shortcuts import call
from tests import TestCase


class InterfaceCDITest(TestCase):
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
        with self.assertRaises(NotImplementedError):
            container.sub_container()
        with self.assertRaises(NotImplementedError):
            container.resolve(None)
        with self.assertRaises(NotImplementedError):
            container.get_producers()
        with self.assertRaises(NotImplementedError):
            container.clear()

    def test_decorator(self):
        with self.assertRaises(NotImplementedError):
            CDIDecorator()()


class InjectInterfaceTest(TestCase):
    def test_error(self):
        def method(*args, **kwargs):
            pass

        method()

        with self.assertRaises(Exception):
            Inject(param=1)(method)

    def test_with_tuple(self):
        @Inject((object, 'default'), param=(object, 'default'))
        def method(*args, **kwargs):
            self.assertIsNotNone(args[0])
            self.assertIsNotNone(kwargs.get('param'))

        call(method)

    def test_with_str(self):
        @Inject('default', param='default')
        def method(*args, **kwargs):
            self.assertIsNotNone(args[0])
            self.assertIsNotNone(kwargs.get('param'))

        call(method)

    def test_with_type(self):
        @Inject(object, param=object)
        def method(*args, **kwargs):
            self.assertIsNotNone(args[0])
            self.assertIsNotNone(kwargs.get('param'))

        call(method)
