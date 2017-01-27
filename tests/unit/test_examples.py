import os
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

examples = [
    os.path.join(BASE_DIR, 'examples', 'simple.py'),
]


class TestExamples(unittest.TestCase):
    def test_examples(self):
        for example in examples:
            with open(example) as code:
                exec (code.read(), {'__name__': '__main__'})
