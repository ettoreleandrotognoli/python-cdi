# -*- encoding: utf-8 -*-
import unittest
from pycdi.utils import Provide
from pycdi.core import CDIContainer
from pycdi import Inject


class ProvideTest(unittest.TestCase):
    def test_django_view(self):
        expected_request = 'the request'
        expected_pk = 1
        expected_response = 'the response'

        @Provide()
        @Inject(container=CDIContainer)
        def django_view_style(request, pk, container):
            self.assertEqual(request, expected_request)
            self.assertEqual(pk, expected_pk)
            self.assertIsNotNone(container)
            self.assertIsInstance(container, CDIContainer)
            return expected_response

        response = django_view_style(expected_request, expected_pk)
        self.assertEqual(response, expected_response)
