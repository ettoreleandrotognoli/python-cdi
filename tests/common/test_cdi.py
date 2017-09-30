# -*- encoding: utf-8 -*-
import unittest

from pycdi import Inject
from pycdi.core import DEFAULT_CONTAINER
from pycdi.shortcuts import call


class NameAsContextTest(unittest.TestCase):
    def test_simple_func(self):
        @Inject(a=int, b=int, _name_as_context=True)
        def sub_func(a, b):
            return a - b

        DEFAULT_CONTAINER.register_instance(4, int, context='a')
        DEFAULT_CONTAINER.register_instance(2, int, context='b')
        self.assertEqual(2, call(sub_func))

        DEFAULT_CONTAINER.register_instance(2, int, context='a')
        DEFAULT_CONTAINER.register_instance(2, int, context='b')
        self.assertEqual(0, call(sub_func))

        DEFAULT_CONTAINER.register_instance(2, int, context='a')
        DEFAULT_CONTAINER.register_instance(4, int, context='b')
        self.assertEqual(-2, call(sub_func))
