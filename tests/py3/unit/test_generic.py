from typing import List
from typing import Tuple
from unittest import TestCase

from pycdi import Inject
from pycdi import Producer
from pycdi.core import PyCDIContainer


class GenericTest(TestCase):
    def test_int_list(self):
        container = PyCDIContainer()
        expected = [1, 2, 3, 4]
        container.register_instance(expected, List[int])
        result = container.produce(List[int])
        self.assertEqual(expected, result)

    def test_heterogeneous_tuple(self):
        container = PyCDIContainer()
        expected = ('string', 1,)
        container.register_instance(expected, Tuple[str, int])
        result = container.produce(Tuple[str, int])
        self.assertEqual(expected, result)

    def test_common_generic(self):
        container = PyCDIContainer()
        int_list = [1, 2, 3, 4]
        float_list = [1., 2., 3., 4.]
        string_list = ['1', '2', '3', '4']
        container.register_instance(int_list, List[int])
        container.register_instance(float_list, List[float])
        container.register_instance(string_list, List[str])
        self.assertEqual(int_list, container.produce(List[int]))
        self.assertEqual(float_list, container.produce(List[float]))
        self.assertEqual(string_list, container.produce(List[str]))

    def test_with_decorator(self):
        container = PyCDIContainer()

        @Producer(_container=container)
        def build_int_list() -> List[int]:
            return [1, 2, 3, 4]

        @Producer(_container=container)
        @Inject()
        def build_float_list(origin: List[int]) -> List[float]:
            return list(map(float, origin))

        @Producer(_container=container)
        @Inject()
        def build_str_list(origin: List[int]) -> List[str]:
            return list(map(str, origin))

        @Inject()
        def test(int_list: List[int],
                 float_list: List[float],
                 str_list: List[str]) -> bool:
            self.assertEqual(int_list, [1, 2, 3, 4])
            self.assertEqual(float_list, [1., 2., 3., 4.])
            self.assertEqual(str_list, ['1', '2', '3', '4'])
            return True

        self.assertEqual(container.call(test), True)
