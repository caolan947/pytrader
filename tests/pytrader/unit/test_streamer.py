import unittest
from unittest.mock import patch, Mock

from pytrader import streamer

class TestStreamer(unittest.TestCase):
    def setUp(self):
        self.fake_log = Mock()
        self.fake_client = Mock()
        self.fake_ks = Mock()
        self.fake_bm = Mock()

    @patch('pytrader.streamer.BinanceSocketManager')
    @patch('pytrader.streamer.Client')
    @patch('pytrader.streamer.logger')
    def test___init__(self, mock_log, mock_client, mock_bm):
        mock_client.return_value = self.fake_client
        mock_client.KLINE_INTERVAL_1MINUTE = '1m'
        mock_bm.return_value = self.fake_bm
        mock_bm.return_value.kline_socket.return_value = self.fake_ks
        fake_streamer = Mock(
            pair = 'BTCUSDT',
            timeframe = '1m',
            log = self.fake_log,
            run = True,
            client = self.fake_client,
            bm = self.fake_bm,
            ks = self.fake_ks
        )
        mock_log.config_logger.return_value = self.fake_log

        expected_result = fake_streamer
        actual_result = streamer.Streamer()

        with self.subTest():
            self.assertEqual(expected_result.pair, actual_result.pair)
            self.assertEqual(expected_result.timeframe, actual_result.timeframe)
            self.assertEqual(expected_result.log, actual_result.log)
            self.assertEqual(expected_result.run, actual_result.run)
            self.assertEqual(expected_result.client, actual_result.client)
            self.assertEqual(expected_result.bm, actual_result.bm)
            self.assertEqual(expected_result.ks, actual_result.ks)

    def test_start_stream(self):
        pass

    def test_end_stream(self):
        pass