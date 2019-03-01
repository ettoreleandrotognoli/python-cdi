# -*- encoding: utf-8 -*-
from pycdi import Producer, Inject
from pycdi.core import DEFAULT_CONTAINER
from tests import TestCase

SOME_STRING = 'some_string'


@Producer(str)
def get_some_string():
    return SOME_STRING


class TestProducer(TestCase):
    def test_reference(self):
        self.assertIsNotNone(get_some_string)
        self.assertEqual(SOME_STRING, get_some_string())


@Producer(int, _priority=None)
def get_some_int():
    return 0


@Producer(int, _priority=0)
def get_another_int():
    return 1


class TestMultipleProducer(TestCase):
    def test_priority(self):
        self.assertEqual(DEFAULT_CONTAINER.produce(int), 0)
        self.assertEqual(list(DEFAULT_CONTAINER.produce([int])), [0, 1])

    def test_with_subcontainer(self):
        container = DEFAULT_CONTAINER.sub_container()
        container.register_instance(2, priority=0)
        self.assertEqual(list(container.produce([int])), [0, 2, 1])
        container.register_instance(-1)
        self.assertEqual(list(container.produce([int])), [-1, 0, 1])

    called = None

    def test_inject(self):
        @Inject(numbers=([int], 'default'))
        def function_with_injection(numbers):
            self.assertEqual(list(numbers), [0, 1])
            self.called = True

        DEFAULT_CONTAINER.call(function_with_injection)
        self.assertTrue(self.called)


class TestProducersInInstance(TestCase):

    def test_simple(self):
        class NewType:
            pass

        new_type = NewType()

        class WithProducer:

            @Producer(produce_type=NewType)
            def make_int(self):
                return new_type

        instance = WithProducer()
        self.container.register_instance(instance)
        produced = self.container.produce(NewType)
        self.assertIs(produced, new_type)
