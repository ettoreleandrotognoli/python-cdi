# -*- encoding: utf-8 -*-
from tests import TestCase

from pycdi import Inject
from pycdi.core import DEFAULT_CONTAINER, DEFAULT_CONTEXT
from pycdi.shortcuts import call


class NameAsContextTest(TestCase):
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


class WithForwardReferenceClass(object):
    @Inject(another_me=('WithForwardReferenceClass', DEFAULT_CONTEXT))
    def kwargs_inject(self, another_me):
        return another_me

    @Inject(('WithForwardReferenceClass', DEFAULT_CONTEXT))
    def args_inject(self, another_me):
        return another_me


class ForwardReferenceTest(TestCase):
    def test_simple_class(self):
        wfrc = WithForwardReferenceClass()
        DEFAULT_CONTAINER.register_instance(wfrc)
        self.assertIs(wfrc, call(wfrc.kwargs_inject))
        self.assertIs(wfrc, call(wfrc.args_inject))
