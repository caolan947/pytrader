import unittest
from unittest.mock import patch, Mock

from pytrader import logger

from datetime import datetime

class TestLogger(unittest.TestCase):
    def setUp(self):
        pass

    @patch('pytrader.logger.datetime')
    @patch('pytrader.logger.logging')
    def test_config_logger(self, mock_handler, mock_datetime):

        mock_datetime.now.return_value = datetime(2023, 1, 1, 0, 0, 0, 0)
        fake_logger = Mock(setLevel=Mock(), addHandler=Mock())
        fake_formatter = Mock(setFormatter=Mock())

        mock_handler.FileHandler.return_value = fake_formatter
        mock_handler.getLogger.return_value = fake_logger

        expected_result = (fake_logger, '2023-01-01_00-00-00.log')

        actual_result = logger.config_logger()

        with self.subTest():
            self.assertEqual(expected_result, actual_result)
            self.assertEqual(1, fake_formatter.setFormatter.call_count)
            self.assertEqual(1, fake_logger.setLevel.call_count)
            self.assertEqual(1, fake_logger.addHandler.call_count)
            self.assertTrue(mock_handler.FileHandler.called_once_with('pytrader/logs/2023-01-01_00-00-00.log'))