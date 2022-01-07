import unittest

from helpers.helpers import multiple_replace


class TestMultipleReplace(unittest.TestCase):
    def setUp(self):
        self.string = 'Hello {{NAME}}, I am {{AGE}} year old.'

    def test_multiple_replace_empty_replace_dict(self):
        replace_dict = {}

        self.assertEqual(multiple_replace(self.string, replace_dict), 'Hello {{NAME}}, I am {{AGE}} year old.')

    def test_multiple_replace_provided_replace_dict(self):
        replace_dict = {
            'NAME': 'ALEX',
            'AGE': 25
        }

        self.assertEqual(multiple_replace(self.string, replace_dict), 'Hello ALEX, I am 25 year old.')



