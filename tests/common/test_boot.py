from unittest import TestCase
import os

from pycdi.utils import boot_cdi

DIR = os.path.dirname(__file__)


class BootTest(TestCase):
    def test_boot(self):
        expected = [
            os.path.join(DIR, 'boot/load_me_cdi.py'),
            os.path.join(DIR, 'boot/deep/me_too_cdi.py')
        ]
        loaded = boot_cdi(paths=['boot/*_cdi.py', 'boot/deep/*_cdi.py'], root=DIR)
        self.assertEqual(set(expected), set(loaded))
