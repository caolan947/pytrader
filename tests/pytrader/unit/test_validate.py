import unittest
from unittest.mock import Mock, patch

import json

from pytrader import validate

class TestValidate(unittest.TestCase):

    @patch('pytrader.validate.pd')
    def setUp(self, mock_df):
        import pandas as pd

        self.test_data = [
            {
                "symbol": "PAIR1USDT",
                "price": "0.123"
            },
            {
                "symbol": "PAIR2GBPC",
                "price": "456.0"
            },
            {
                "symbol": "PAIR3USDT",
                "price": "7.89"
            }
        ]
        self.test_df = pd.DataFrame(self.test_data)

        self.df_drop = Mock(drop=pd.DataFrame([
            {
                "symbol": "PAIR1USDT",
                "price": "0.123"
            }
        ])
        )
        self.valid_pair = 'PAIR1USDT'
        self.invalid_pair = 'PAIR2GBPC'
        self.valid_timeframe = '1m'
        self.invalid_timeframe = '2m'
        self.valid_pairs = ['PAIR1USDT', 'PAIR3USDT']
        self.valid_timeframes = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

    @patch('pytrader.validate.pd')
    @patch('pytrader.validate.requests')
    def test___init__(self, mock_r, mock_df):
        mock_r.get.return_value.json.return_value = self.test_data
        mock_df.DataFrame.return_value = self.test_df

        expected_result = Mock(
            _valid_pairs = self.valid_pairs,
            _valid_timeframes = self.valid_timeframes,
            _pair = self.valid_pair,
            _timeframe = self.valid_timeframe
        )

        with self.subTest():
            actual_result = validate.Validater(self.valid_pair, self.valid_timeframe)
            self.assertEqual(expected_result._valid_timeframes, actual_result._valid_timeframes)
            self.assertEqual(expected_result._valid_pairs, actual_result._valid_pairs)
            self.assertEqual(expected_result._pair, actual_result._pair)
            self.assertEqual(expected_result._timeframe, actual_result._timeframe)

        with self.assertRaises(ValueError) as e:
            validate.Validater(self.invalid_pair, self.valid_timeframe)
        self.assertTrue(f"Validating provided trading pair. {self.invalid_pair} is an invalid pair. Ensure the provided pair is a valid USDT pair from the following list: {self.valid_pairs}" in str(e.exception))

        with self.assertRaises(ValueError) as e:
            validate.Validater(self.valid_pair, self.invalid_timeframe)
        self.assertTrue(f"Validating provided trading timeframe. {self.invalid_timeframe} is an invalid timeframe. Ensure the provided timeframe is selected from the following list: {self.valid_timeframes}" in str(e.exception))

        with self.assertRaises(ValueError) as e:
            validate.Validater(self.invalid_pair, self.invalid_timeframe)
        self.assertTrue(f"Validating provided trading pair. {self.invalid_pair} is an invalid pair. Ensure the provided pair is a valid USDT pair from the following list: {self.valid_pairs}" in str(e.exception))
