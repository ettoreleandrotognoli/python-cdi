# -*- encoding: utf-8 -*-
import unittest
from pycdi import Producer, Inject
from pycdi.shortcuts import new, call


SOME_STRING = 'some_string'
ANOTHER_STRING = 'another_string'

@Producer(str)
def get_some_string():
    return SOME_STRING

@Producer(str,context='another')
def get_another():
    return ANOTHER_STRING


@Inject(some_string=str)
def function_with_injection(some_string):
    return some_string

@Inject(some_string=str,context='another')
def another_function_with_injection(some_string):
    return some_string


class SimpleCDITest(unittest.TestCase):

    def test_default_str_producer(self):
        expected = SOME_STRING
        result = new(str)
        self.assertEqual(expected,result)

    def test_another_str_producer(self):
        expected = ANOTHER_STRING
        result = new(str,context='another')
        self.assertEqual(expected,result)

    def test_injected_string(self):
        expected = SOME_STRING
        result = call(function_with_injection)
        self.assertEqual(expected,result)

    def test_another_injected_string(self):
        expected = ANOTHER_STRING
        result = call(another_function_with_injection)
        self.assertEqual(expected,result)


class BaseClass(object):

    def do_something(self):
        raise NotImplementedError

class SubclassA(BaseClass):

    def do_something(self):
        pass

class SubclassB(BaseClass):

    def do_somthing(self):
        pass

@Producer(BaseClass)
def get_subclass_a():
    return SubclassA()

@Producer(SubclassB,context='another')
def get_subclass_b():
    return SubclassB()


class CDITest(unittest.TestCase):
    

    def test_default_subclass(self):
        expected = SubclassA
        result = type(new(BaseClass))
        self.assertEqual(expected,result)

    def test_another_subclass(self):
        expected = SubclassB
        result = type(new(BaseClass,context='another'))
        self.assertEqual(expected,result)


@Inject(some_string=str,a=BaseClass)
@Inject(another_string=str,b=BaseClass,context='another')
class ComplexClass(object):

    def __init__(self,some_string,another_string,a,b):
        self.a = a
        self.b = b
        self.some_string = some_string
        self.another_string = another_string


class ClassInjectTest(unittest.TestCase):

    def test_init_complex_class(self):
        complex_class = new(ComplexClass)
        self.assertIsInstance(complex_class,ComplexClass)
        self.assertIsNotNone(complex_class)
        self.assertEqual(type(complex_class.a),SubclassA)
        self.assertEqual(type(complex_class.b),SubclassB)
        self.assertEqual(complex_class.some_string,SOME_STRING)
        self.assertEqual(complex_class.another_string,ANOTHER_STRING)

