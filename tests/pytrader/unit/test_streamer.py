from unittest.mock import patch, Mock
import asynctest

from pytrader import streamer

import asyncio

class TestStreamer(asynctest.TestCase):
    def setUp(self):
        self.fake_log = Mock()
        self.fake_client = Mock()
        self.fake_ks = Mock()
        self.fake_bm = Mock()
        self.fake_streamer = Mock(
            pair = 'BTCUSDT',
            timeframe = '1m',
            log = self.fake_log,
            run = True,
            client = self.fake_client,
            bm = self.fake_bm,
            ks = self.fake_ks
        )
        self.streamer = streamer.Streamer()

    @patch('pytrader.streamer.BinanceSocketManager')
    @patch('pytrader.streamer.Client')
    @patch('pytrader.streamer.logger')
    def test___init__(self, mock_log, mock_client, mock_bm):
        mock_client.return_value = self.fake_client
        mock_client.KLINE_INTERVAL_1MINUTE = '1m'
        mock_bm.return_value = self.fake_bm
        mock_bm.return_value.kline_socket.return_value = self.fake_ks
        mock_log.config_logger.return_value = self.fake_log

        expected_result = self.fake_streamer
        actual_result = streamer.Streamer()

        with self.subTest():
            self.assertEqual(expected_result.pair, actual_result.pair)
            self.assertEqual(expected_result.timeframe, actual_result.timeframe)
            self.assertEqual(expected_result.log, actual_result.log)
            self.assertEqual(expected_result.run, actual_result.run)
            self.assertEqual(expected_result.client, actual_result.client)
            self.assertEqual(expected_result.bm, actual_result.bm)
            self.assertEqual(expected_result.ks, actual_result.ks)

    @patch('pytrader.streamer.Candle')
    @patch.object(streamer.BinanceSocketManager, 'kline_socket')
    def test_start_stream(self, mock_self, mock_c):
        mock_self.return_value.__enter__.return_value = Mock()
        mock_c.return_value = Mock()

        s = streamer.Streamer()
        my_loop = asyncio.new_event_loop()

        try:
            my_loop.run_until_complete(s.start_stream())         

        finally:
            my_loop.close()

        with self.subTest():
            self.assertTrue(mock_c.is_called)

    def test_end_stream(self):
        actual_result = self.streamer.end_stream()

        with self.subTest():
            self.assertFalse(self.streamer.run)