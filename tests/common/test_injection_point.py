# -*- encoding: utf-8 -*-
import unittest
from random import random, choice

from pycdi import Producer, Inject
from pycdi.core import InjectionPoint, PyCDIContainer


class InjectionPointTest(unittest.TestCase):
    float_injection_point = None
    str_injection_point = None

    def test_injection_points(self):
        container = PyCDIContainer()

        @Producer(produce_type=float, _container=container)
        @Inject(injection_point=InjectionPoint)
        def float_producer(injection_point):
            self.assertEqual(injection_point.type, float)
            self.assertIsNotNone(injection_point.member)
            self.assertIsNotNone(injection_point.name)
            self.assertIsNotNone(injection_point.context)
            self.float_injection_point = injection_point
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
