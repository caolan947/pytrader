import unittest
from unittest.mock import patch, Mock

import asyncio

import app

import pytrader.logger
import argparse

class TestApp(unittest.TestCase):
    def setUp(self):
        self.fake_log = Mock()
        self.fake_file_name = 'fake_file_name'
        self.fake_arg_parser = Mock()
        self.fake_args = Mock()
        self.fake_s = Mock(
            start_stream = Mock(),
            end_stream = Mock()
        )
        self.fake_loop = Mock(
            run_until_complete = Mock()
        )

    @patch.object(asyncio, 'get_event_loop')
    @patch('pytrader.streamer.Streamer')
    @patch.object(argparse.ArgumentParser, 'parse_args')
    @patch.object(argparse.ArgumentParser, 'add_argument')
    @patch.object(pytrader.logger, 'config_logger')
    def test_main(self, mock_log, mock_arg_parser, mock_args, mock_s, mock_loop):

        mock_log.return_value = (self.fake_log, self.fake_file_name)
        mock_arg_parser.return_value = self.fake_arg_parser
        mock_args.return_value = self.fake_args
        mock_s.return_value = self.fake_s
        mock_loop.return_value = self.fake_loop
        
        app.main()

        with self.subTest():
            self.assertTrue(mock_log.called)
            self.assertTrue(mock_arg_parser.call_count)
            self.assertTrue(mock_args.call_count)
            self.assertTrue(mock_s.called)
            self.assertTrue(mock_s.return_value.start_stream.called)
            self.assertTrue(mock_loop.called)
            self.assertTrue(mock_loop.return_value.run_until_complete.called)

        mock_loop.side_effect = KeyboardInterrupt()
        
        app.main()

        with self.subTest():
            self.assertTrue(mock_s.called)
            self.assertTrue(mock_s.return_value.end_stream.called)
            self.assertTrue(mock_loop.called)