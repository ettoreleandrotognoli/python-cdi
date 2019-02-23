from tests import TestCase

import os

from pycdi.shortcuts import new
from pycdi.utils import boot_cdi

DIR = os.path.dirname(__file__)


class BootTest(TestCase):
    def test_boot_with_root(self):
        expected = [
            'boot.load_me_cdi',
            'boot.deep.me_too_cdi',
        ]
        boot_cdi(paths=['boot/*_cdi.py', 'boot/deep/*_cdi.py'], root=DIR)
        result = [
            new(str, 'load_me'),
            new(str, 'me_too')
        ]
        self.assertEqual(expected, result)

    def test_boot_without_root(self):
        expected = [
            'boot.load_me_cdi',
            'boot.deep.me_too_cdi',
        ]
        boot_cdi(paths=['boot/*_cdi.py', 'boot/deep/*_cdi.py'])
        result = [
            new(str, 'load_me'),
            new(str, 'me_too')
        ]
        self.assertEqual(expected, result)
