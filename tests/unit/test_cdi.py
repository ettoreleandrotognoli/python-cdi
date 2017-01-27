# -*- encoding: utf-8 -*-
import unittest
from pycdi.core import CDIContainer, DEFAULT_CONTAINER
from pycdi import Producer, Inject
from pycdi.shortcuts import new, call

SOME_STRING = 'some_string'
ANOTHER_STRING = 'another_string'


@Producer(str)
def get_some_string():
    return SOME_STRING


@Producer(str, _context='another')
def get_another():
    return ANOTHER_STRING


@Inject(some_string=str)
def function_with_injection(some_string):
    return some_string


@Inject(some_string=str, _context='another')
def another_function_with_injection(some_string):
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
def get_subclass_a():
    return SubclassA()


@Producer(SubclassB, _context='another')
def get_subclass_b():
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


@Inject(some_string=str, a=BaseClass)
@Inject(another_string=str, b=BaseClass, _context='another')
class ComplexClass(object):
    def __init__(self, some_string, another_string, a, b):
        self.a = a
        self.b = b
        self.some_string = some_string
        self.another_string = another_string

    @Inject(test=unittest.TestCase)
    def method_with_injection(self, test):
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
        @Inject(container=CDIContainer)
        def function(container):
            self.assertIsNotNone(container)
            self.assertIsInstance(container, CDIContainer)

        DEFAULT_CONTAINER.call(function)

    def test_simple_class(self):
        @Inject(container=CDIContainer)
        class Class(object):
            def __init__(self, container):
                self.container = container

        obj = DEFAULT_CONTAINER.produce(Class)
        self.assertIsNotNone(obj.container)
        self.assertIsInstance(obj.container, CDIContainer)
        self.assertEqual(DEFAULT_CONTAINER, obj.container)

    def test_subclass(self):
        @Inject(container=CDIContainer)
        class WithContainer(object):
            def __init__(self, container):
                self.cdi = container

        class Subclass(WithContainer):
            def __init__(self, *args, **kwargs):
                super(Subclass, self).__init__(*args, **kwargs)

        obj = DEFAULT_CONTAINER.produce(Subclass)
        self.assertIsNotNone(obj.cdi)
        self.assertIsInstance(obj.cdi, CDIContainer)


class InjectArgsTest(unittest.TestCase):
    def test_common_args(self):
        DEFAULT_CONTAINER.register_instance(2, int)
        DEFAULT_CONTAINER.register_instance(4.0, float)

        @Inject(int)
        @Inject(float, int)
        def sum_func(*args):
            self.assertIsInstance(args[0], float)
            self.assertIsInstance(args[1], int)
            self.assertIsInstance(args[1], int)
            self.assertGreaterEqual(len(args), 3)
            return sum(args)

        self.assertEqual(8, call(sum_func))
        self.assertEqual(11, call(sum_func, 3))

    def test_with_context_args(self):
        DEFAULT_CONTAINER.register_instance(1, int, context='1')
        DEFAULT_CONTAINER.register_instance(2, int, context='2')
        DEFAULT_CONTAINER.register_instance(3, int, context='3')

        @Inject(int, _context='3')
        @Inject(int, _context='2')
        @Inject(int, _context='1')
        def sum_func(*args):
            for i, arg in zip(range(1, len(args) + 1), args):
                self.assertEqual(i, arg)
            return sum(args)

        self.assertEqual(6, call(sum_func))
        self.assertEqual(10, call(sum_func, 4))
