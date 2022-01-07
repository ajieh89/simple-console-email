import unittest
import os

from helpers.helpers import get_absolute_url
from utils.email import EmailClass


class TestEmailClass(unittest.TestCase):
    def setUp(self):
        self.test_dir = get_absolute_url('tests/utils/test_output/')

        if not os.path.isdir(self.test_dir):
            print(self.test_dir)
            os.mkdir(self.test_dir)

    def tearDown(self):
        os.removedirs(self.test_dir)

    def test_email_process_content(self):
        abs_path = get_absolute_url('__init__.py')
        self.assertTrue(os.path.isabs(abs_path))

    # def test_dget_absolute_path_with_abs_path(self):
    #     abs_path = get_absolute_url('/__init__.py')
    #     self.assertTrue(abs_path, '/__init__.py')