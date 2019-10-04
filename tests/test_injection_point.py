# -*- encoding: utf-8 -*-
from tests import TestCase
from random import random, choice

from pycdi import Producer, Inject
from pycdi.core import InjectionPoint, PyCDIContainer


class InjectionPointTest(TestCase):
    float_injection_point = None
    str_injection_point = None

    def test_injection_points(self):
        container = PyCDIContainer()

        @Producer(produce_type=float, _container=container)
        @Inject(ip=InjectionPoint)
        def float_producer(ip):
            self.assertEqual(ip.type, float)
            self.assertIsNotNone(ip.member)
            self.assertIsNotNone(ip.name)
            self.assertIsNotNone(ip.context)
            self.float_injection_point = ip
            return random()

        @Producer(produce_type=str, _container=container)
        @Inject(injection_point=InjectionPoint)
        def float_producer(injection_point):
            self.assertEqual(injection_point.type, str)
            self.assertIsNotNone(injection_point.member)
            self.assertIsNotNone(injection_point.name)
            self.assertIsNotNone(injection_point.context)
            self.str_injection_point = injection_point
            letters = [chr(i) for i in range(97, 97 + 26)]
            return choice(letters)

        @Inject(random_float=float)
        def receive_float(random_float):
            self.assertIsNotNone(random_float)

        container.call(receive_float)

        @Inject(random_str=str)
        def receive_str(random_str):
            self.assertIsNotNone(random_str)

        container.call(receive_str)

        self.assertIsNotNone(self.float_injection_point)
        self.assertIsNotNone(self.str_injection_point)
