from unittest import TestCase

from pycdi.core import Service, Inject
from pycdi.shortcuts import call


@Service()
class AnyService(object):

    def __init__(self):
        pass


class ServiceTest(TestCase):

    def test_inject_service(self):
        @Inject(service=AnyService)
        def receive_service(service):
            self.assertIsInstance(service, AnyService)

        call(receive_service)
