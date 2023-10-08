import unittest
from unittest.mock import Mock

class TestLogger(unittest.TestCase):
    def setUp(self):
        pass

    def config_logger(self,):
        expected_result = 1
        
        actual_result = 1

        with self.subTest():
            self.assertEqual(expected_result, 2)