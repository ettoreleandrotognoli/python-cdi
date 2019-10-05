import unittest


class BaseTestCase(unittest.TestCase):
    pass


class TestCase(BaseTestCase):

    def setUp(self):
        # DEFAULT_CONTAINER.clear()
        pass

    def tearDown(self):
        # DEFAULT_CONTAINER.clear()
        pass


class PersistContextTestCase(BaseTestCase):
    pass
