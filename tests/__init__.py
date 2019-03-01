import unittest

from pycdi.core import DEFAULT_CONTAINER


class TestCase(unittest.TestCase):
    container = None

    def setUp(self):
        self.container = DEFAULT_CONTAINER.sub_container()
