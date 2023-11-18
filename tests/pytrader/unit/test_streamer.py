import unittest
from unittest.mock import patch, Mock
import asynctest

from pytrader import streamer

import asyncio

class TestStreamer(asynctest.TestCase):

    @patch('pytrader.streamer.sql_handler')
    @patch('pytrader.streamer.BinanceSocketManager')
    @patch('pytrader.streamer.Client')
    @patch('pytrader.streamer.uuid')
    def setUp(self, mock_stream_id, mock_client, mock_bm, mock_db):
        self.fake_log = Mock()
        self.fake_client = Mock()
        self.fake_ks = Mock()
        self.fake_bm = Mock()
        self.fake_db = Mock(db_write_end_stream = Mock(), close_cursor = Mock())
        self.fake_streamer = Mock(
            pair = 'fake_pair',
            timeframe = 'fake_timeframe',
            log = self.fake_log,
            file_name = 'fake_file_name',
            run = True,
            stream_id = 'fake_uuid',
            db = self.fake_db,
            client = self.fake_client,
            bm = self.fake_bm,
            ks = self.fake_ks
        )

        mock_stream_id.uuid4.return_value = 'fake_uuid'
        mock_db.SqlController.return_value = self.fake_db
        mock_client.return_value = self.fake_client
        mock_client.KLINE_INTERVAL_1MINUTE = '1m'
        mock_bm.return_value = self.fake_bm
        mock_bm.return_value.kline_socket.return_value = self.fake_ks
        self.streamer = streamer.Streamer('fake_pair', 'fake_timeframe', self.fake_log, 'fake_file_name', True, True)

    def test___init__(self):
        expected_result = self.fake_streamer
        actual_result = self.streamer

        with self.subTest():
            self.assertEqual(expected_result.pair, actual_result.pair)
            self.assertEqual(expected_result.timeframe, actual_result.timeframe)
            self.assertEqual(expected_result.log, actual_result.log)
            self.assertEqual(expected_result.file_name, actual_result.file_name)
            self.assertEqual(expected_result.run, actual_result.run)
            self.assertEqual(expected_result.stream_id, actual_result.stream_id)
            self.assertEqual(expected_result.db, actual_result.db)
            self.assertEqual(expected_result.client, actual_result.client)
            self.assertEqual(expected_result.bm, actual_result.bm)
            self.assertEqual(expected_result.ks, actual_result.ks)

    @unittest.skip
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
        self.streamer.end_stream()

        with self.subTest():
            self.assertFalse(self.streamer.run)