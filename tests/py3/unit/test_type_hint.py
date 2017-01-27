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
