from unittest import TestCase

from pycdi.core import Component, Inject, Producer
from pycdi.shortcuts import call


@Component()
class AnyComponent(object):

    def __init__(self):
        pass


@Component()
class ComponentWithProducers(object):

    def __init__(self):
        self.counter = 0

    @Producer(int)
    def next_int(self):
        self.counter += 1
        return self.counter


class ComponentTest(TestCase):

    def test_inject_component(self):
        @Inject(component=AnyComponent)
        def receive_component(component):
            self.assertIsInstance(component, AnyComponent)

        call(receive_component)

    def test_inject_from_component_method(self):
        expected = 1

        @Inject(number=int)
        def receive_component_product(number):
            self.assertIsInstance(number, int)
            self.assertEqual(number, expected)

        call(receive_component_product)
        expected = 2
        call(receive_component_product)
