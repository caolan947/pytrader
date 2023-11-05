import unittest
from unittest.mock import patch, Mock

import asyncio

import app

class TestApp(unittest.TestCase):
    def setUp(self):
        pass

    @patch.object(asyncio, 'get_event_loop')
    @patch('pytrader.streamer.Streamer')
    def test_main(self, mock_s, mock_loop):

        mock_s.return_value = Mock(
            start_stream = Mock()
        )

        mock_loop.return_value = Mock(
            run_until_complete = Mock()
        )
        
        app.main('fake_pair', 'fake_timeframe')

        with self.subTest():
            self.assertTrue(mock_s.called)
            self.assertTrue(mock_s.return_value.start_stream.called)
            self.assertTrue(mock_loop.called)
            self.assertTrue(mock_loop.return_value.run_until_complete.called)

        mock_s.return_value = Mock(
            end_stream = Mock()
        )

        mock_loop.side_effect = KeyboardInterrupt()
        
        app.main('fake_pair', 'fake_timeframe')

        with self.subTest():
            self.assertTrue(mock_s.called)
            self.assertTrue(mock_s.return_value.end_stream.called)
            self.assertTrue(mock_loop.called)