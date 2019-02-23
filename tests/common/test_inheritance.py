# -*- encoding: utf-8 -*-

from tests import TestCase

from pycdi import Inject
from pycdi.core import DEFAULT_CONTAINER


class InheritanceTest(TestCase):
    def test_inheritance(self):
        test_case = self
        DEFAULT_CONTAINER.register_instance('inheritance', str)
        DEFAULT_CONTAINER.register_instance({}, dict)
        DEFAULT_CONTAINER.register_instance([], list)

        @Inject(str, some_object=object)
        class A(object):
            def __init__(self, some_str, some_object):
                test_case.assertIsInstance(some_str, str)
                test_case.assertIsInstance(some_object, object)

        @Inject(some_object=object, some_dict=dict)
        class B(A):
            def __init__(self, some_str, some_object, some_dict):
                test_case.assertIsInstance(some_str, str)
                test_case.assertIsInstance(some_object, object)
                test_case.assertIsInstance(some_dict, dict)

        @Inject(some_object=object, some_list=list)
        class C(A):
            def __init__(self, some_str, some_object, some_list):
                test_case.assertIsInstance(some_str, str)
                test_case.assertIsInstance(some_object, object)
                test_case.assertIsInstance(some_list, list)

        DEFAULT_CONTAINER.call(A)
        DEFAULT_CONTAINER.call(B)
        DEFAULT_CONTAINER.call(C)

    def test_inheritance_with_override(self):
        test_case = self
        DEFAULT_CONTAINER.register_instance('inheritance', str)
        DEFAULT_CONTAINER.register_instance({}, dict)
        DEFAULT_CONTAINER.register_instance([], list)

        @Inject(str, some_object=object)
        class A(object):
            def __init__(self, some_str, some_object):
                test_case.assertIsInstance(some_str, str)
                test_case.assertIsInstance(some_object, object)

        @Inject(some_dict=dict, _override=True)
        class B(A):
            def __init__(self, some_dict):
                test_case.assertIsInstance(some_dict, dict)

        @Inject(some_list=list, _override=True)
        class C(A):
            def __init__(self, some_list):
                test_case.assertIsInstance(some_list, list)

        DEFAULT_CONTAINER.call(A)
        DEFAULT_CONTAINER.call(B)
        DEFAULT_CONTAINER.call(C)
