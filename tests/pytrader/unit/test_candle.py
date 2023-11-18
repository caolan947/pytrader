import unittest
from unittest.mock import Mock, patch

from pytrader import candle

from datetime import datetime

class TestCandle(unittest.TestCase):

    @patch.object(candle.uuid, 'uuid4')
    def setUp(self, mock_uuid):
        self.fake_message = {
            'e': 'kline',
            'E': 1699043932482,
            's': 'BTCUSDT',
            'k': {
                't': 1699043880000,
                'T': 1699043939999, 
                's': 'BTCUSDT',
                'i': '1m',
                'f': 123456788,
                'L': 123456789,
                'o': '1.5',
                'c': '2.0',
                'h': '2.5',
                'l': '1.0',
                'v': '1.0',
                'n': 1,
                'x': False,
                'q': '1.0',
                'V': '1.0',
                'Q': '1.0',
                'B': '0'
            }
        }

        self.fake_db = Mock(db_write_closed_candle = Mock())
        self.fake_stream_id = '123456789'
        self.fake_id = '987654321'

        self.fake_candle = {
            'open': 1.5,
            'close': 2.0,
            'high': 2.5,
            'low': 1.0,
            'open_time': '2023-11-03T20:38:00',
            'close_time': '2023-11-03T20:38:59',
            'close_flag': False,
            'db': self.fake_db,
            'stream_id': self.fake_stream_id,
            'id': self.fake_id
        }
        mock_uuid.return_value = self.fake_id

        self.candle = candle.Candle(self.fake_message, self.fake_db, self.fake_stream_id)

    def test___init__(self):
        expected_result = self.fake_candle

        actual_result = self.candle

        with self.subTest():
            self.assertEqual(expected_result['open'], actual_result.open)
            self.assertEqual(expected_result['close'], actual_result.close)
            self.assertEqual(expected_result['high'], actual_result.high)
            self.assertEqual(expected_result['low'], actual_result.low)
            self.assertEqual(expected_result['open_time'], actual_result.open_time)
            self.assertEqual(expected_result['close_time'], actual_result.close_time)
            self.assertFalse(actual_result.close_flag)
            self.assertEqual(expected_result['db'], actual_result.db)
            self.assertEqual(expected_result['stream_id'], actual_result.stream_id)
            self.assertEqual(expected_result['id'], actual_result.id)

    def test_to_dict(self):
        expected_result = self.fake_candle

        actual_result = self.candle.to_dict()

        with self.subTest():
            self.assertEqual(expected_result, actual_result)

    def test_on_close(self):

        self.candle.on_close()

        with self.subTest():
            self.assertEqual(1, self.fake_db.db_write_closed_candle.call_count)