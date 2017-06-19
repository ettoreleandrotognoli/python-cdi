# -*- encoding: utf-8 -*-
import unittest
from pycdi.core import CDIContainer, DEFAULT_CONTAINER
from pycdi import Producer, Inject
from pycdi.shortcuts import new, call

SOME_STRING = 'some_string'


@Producer(str)
def get_some_string():
    return SOME_STRING



class TestProducer(unittest.TestCase):
    def test_reference(self):
        self.assertIsNotNone(get_some_string)
        self.assertEqual(SOME_STRING, get_some_string())
