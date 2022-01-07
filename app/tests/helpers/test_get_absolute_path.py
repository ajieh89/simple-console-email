import unittest
import os

from helpers.helpers import get_absolute_url


class TestGetAbsolutePath(unittest.TestCase):
    def test_get_absolute_path_with_file_name(self):
        abs_path = get_absolute_url('__init__.py')
        self.assertTrue(os.path.isabs(abs_path))

    def test_get_absolute_path_with_abs_path(self):
        abs_path = get_absolute_url('/__init__.py')
        self.assertTrue(abs_path, '/__init__.py')



