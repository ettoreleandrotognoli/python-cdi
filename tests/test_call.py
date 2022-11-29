from tests import TestCase

from pycdi import Inject
from pycdi.core import PyCDIContainer, CDIContainer


class CallTest(TestCase):
    container = None

    def setUp(self):
        self.container = PyCDIContainer()

    def test_call_with_args(self):
        @Inject(cdi=CDIContainer)
        def django_view(request, cdi):
            self.assertIsNotNone(request)
            self.assertIsNotNone(cdi)

        self.container.call(django_view, object())

    def test_call_with_kwargs(self):
        @Inject(cdi=CDIContainer)
        def django_view(pk, cdi):
            self.assertIsNotNone(pk)
            self.assertIsNotNone(cdi)

        self.container.call(django_view, pk=1)

    def test_call_with_args_and_kwargs(self):
        @Inject(cdi=CDIContainer)
        def django_view(request, pk, cdi):
            self.assertIsNotNone(request)
            self.assertIsNotNone(pk)
            self.assertIsNotNone(cdi)

        self.container.call(django_view, object(), pk=1)

    def test_override_cdi(self):
        @Inject(cdi=CDIContainer)
        def django_view(request, pk, cdi):
            self.assertIsNotNone(request)
            self.assertIsNotNone(pk)
            self.assertIsNotNone(cdi)
            self.assertEqual(cdi, 'fuu')

        self.container.call(django_view, object(), pk=1, cdi='fuu')
