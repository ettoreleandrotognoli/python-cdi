from pycdi.core import Component, Inject, Producer
from pycdi.core import PyCDIContainer
from tests import TestCase

container = PyCDIContainer()


@Component(_container=container)
class AnyComponent(object):

    def __init__(self):
        pass


@Component(_container=container)
class ComponentWithProducers(object):

    def __init__(self):
        self.counter = 0

    @Producer(int, _container=container)
    def next_int(self):
        self.counter += 1
        return self.counter


class ComponentTest(TestCase):

    def test_inject_component(self):
        @Inject(component=AnyComponent, _container=container)
        def receive_component(component):
            self.assertIsInstance(component, AnyComponent)

        container.call(receive_component)

    def test_inject_from_component_method(self):
        expected = 1

        @Inject(number=int, _container=container)
        def receive_component_product(number):
            self.assertIsInstance(number, int)
            self.assertEqual(number, expected)

        container.call(receive_component_product)
        expected = 2
        container.call(receive_component_product)
