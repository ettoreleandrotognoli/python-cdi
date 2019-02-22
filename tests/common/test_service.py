from unittest import TestCase

from pycdi.core import Service, Inject, Producer
from pycdi.shortcuts import call


@Service()
class AnyService(object):

    def __init__(self):
        pass


@Service()
class ServiceWithProducers(object):

    def __init__(self):
        self.counter = 0

    @Producer(int)
    def next_int(self):
        self.counter += 1
        return self.counter


class ServiceTest(TestCase):

    def test_inject_service(self):
        @Inject(service=AnyService)
        def receive_service(service):
            self.assertIsInstance(service, AnyService)

        call(receive_service)

    def test_inject_from_service_method(self):
        expected = 1

        @Inject(number=int)
        def receive_service_product(number):
            self.assertIsInstance(number, int)
            self.assertEqual(number, expected)

        call(receive_service_product)
        expected = 2
        call(receive_service_product)
