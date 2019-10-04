# -*- encoding: utf-8 -*-
import unittest
from pycdi.core import CDIContainer, DEFAULT_CONTAINER
from pycdi import Producer, Inject
from pycdi.shortcuts import new, call

SOME_STRING = 'some_string'
ANOTHER_STRING = 'another_string'


@Producer()
def get_some_string() -> str:
    return SOME_STRING


@Producer(_context='another')
def get_another() -> str:
    return ANOTHER_STRING


@Inject()
def function_with_injection(some_string: str) -> str:
    return some_string


@Inject(some_string='another')
def another_function_with_injection(some_string: str) -> str:
    return some_string


class SimpleCDITest(unittest.TestCase):
    def test_default_str_producer(self):
        expected = SOME_STRING
        result = new(str)
        self.assertEqual(expected, result)

    def test_another_str_producer(self):
        expected = ANOTHER_STRING
        result = new(str, context='another')
        self.assertEqual(expected, result)

    def test_injected_string(self):
        expected = SOME_STRING
        result = call(function_with_injection)
        self.assertEqual(expected, result)

    def test_another_injected_string(self):
        expected = ANOTHER_STRING
        result = call(another_function_with_injection)
        self.assertEqual(expected, result)


class BaseClass(object):
    def do_something(self):
        raise NotImplementedError()


class SubclassA(BaseClass):
    def do_something(self):
        pass


class SubclassB(BaseClass):
    def do_something(self):
        pass


@Producer(BaseClass)
def get_subclass_a() -> SubclassA:
    return SubclassA()


@Producer(_context='another')
def get_subclass_b() -> SubclassB:
    return SubclassB()


class CDITest(unittest.TestCase):
    def test_base_class(self):
        with self.assertRaises(NotImplementedError):
            base = BaseClass()
            base.do_something()

    def test_default_subclass(self):
        expected = SubclassA
        result = type(new(BaseClass))
        self.assertEqual(expected, result)

    def test_another_subclass(self):
        expected = SubclassB
        result = type(new(BaseClass, context='another'))
        self.assertEqual(expected, result)


@Inject(another_string='another', b='another')
class ComplexClass(object):
    def __init__(self, some_string: str, another_string: str, a: BaseClass, b: BaseClass):
        self.a = a
        self.b = b
        self.some_string = some_string
        self.another_string = another_string

    @Inject()
    def method_with_injection(self, test: unittest.TestCase):
        test.assertEqual(self.some_string, SOME_STRING)
        test.assertEqual(self.another_string, ANOTHER_STRING)


class ClassInjectTest(unittest.TestCase):
    def test_init_complex_class(self):
        complex_class = new(ComplexClass)
        self.assertIsInstance(complex_class, ComplexClass)
        self.assertIsNotNone(complex_class)
        self.assertEqual(type(complex_class.a), SubclassA)
        self.assertEqual(type(complex_class.b), SubclassB)
        self.assertEqual(complex_class.some_string, SOME_STRING)
        self.assertEqual(complex_class.another_string, ANOTHER_STRING)
        complex_class.a.do_something()
        complex_class.b.do_something()

    def test_method_with_injection(self):
        DEFAULT_CONTAINER.register_instance(self)
        complex_class = new(ComplexClass)
        call(complex_class.method_with_injection)


class SelfInjectTest(unittest.TestCase):
    def test_simple_function(self):
        @Inject()
        def function(container: CDIContainer):
            self.assertIsNotNone(container)
            self.assertIsInstance(container, CDIContainer)

        DEFAULT_CONTAINER.call(function)

    def test_simple_class(self):
        @Inject()
        class Class(object):
            def __init__(self, container: CDIContainer):
                self.container = container

        obj = DEFAULT_CONTAINER.produce(Class)
        self.assertIsNotNone(obj.container)
        self.assertIsInstance(obj.container, CDIContainer)
        self.assertEqual(DEFAULT_CONTAINER, obj.container)

    def test_subclass(self):
        @Inject()
        class WithContainer(object):
            def __init__(self, container: CDIContainer):
                self.cdi = container

        class Subclass(WithContainer):
            def __init__(self, *args, **kwargs):
                super(Subclass, self).__init__(*args, **kwargs)

        obj = DEFAULT_CONTAINER.produce(Subclass)
        self.assertIsNotNone(obj.cdi)
        self.assertIsInstance(obj.cdi, CDIContainer)
