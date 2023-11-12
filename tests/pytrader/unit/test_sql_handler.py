import unittest
from unittest.mock import patch, Mock

import io

from pytrader import sql_handler

class TestSqlHandler(unittest.TestCase):
    
    @patch('pytrader.sql_handler.pyodbc')
    def setUp(self, mock_conn):
        self.fake_log = Mock()
        self.fake_cursor = Mock(execute = Mock(), commit = Mock(), close = Mock())
        self.fake_conn = Mock()
    
        mock_conn.connect.return_value = self.fake_conn
        mock_conn.connect.return_value.cursor.return_value = self.fake_cursor

        self.fake_sql_controller = Mock(
            driver = 'fake_driver',
            server = 'fake_server',
            database = 'fake_database',
            username = 'fake_username',
            password = 'fake_password',
            pair = 'fake_pair',
            timeframe = 'fake_timeframe',
            file_name = 'fake_file_name',
            log = self.fake_log,
            conn_string = 'DRIVER={fake_driver};SERVER=fake_server;DATABASE=fake_database;UID=fake_username;PWD=fake_password',
            conn = self.fake_conn,
            cursor = self.fake_cursor
        )

        self.sql_controller = sql_handler.SqlController(
            'fake_driver',
            'fake_server',
            'fake_database',
            'fake_username',
            'fake_password',
            'fake_pair',
            'fake_timeframe',
            'fake_file_name',
            self.fake_log
        )

        self.generic_exception = Exception("Some error")

    def test___init__(self):
        expected_result = self.fake_sql_controller

        actual_result = self.sql_controller

        with self.subTest():
            self.assertEqual(expected_result.driver, actual_result.driver)
            self.assertEqual(expected_result.server, actual_result.server)
            self.assertEqual(expected_result.database, actual_result.database)
            self.assertEqual(expected_result.username, actual_result.username)
            self.assertEqual(expected_result.password, actual_result.password)
            self.assertEqual(expected_result.pair, actual_result.pair)
            self.assertEqual(expected_result.timeframe, actual_result.timeframe)
            self.assertEqual(expected_result.file_name, actual_result.file_name)
            self.assertEqual(expected_result.log, actual_result.log)    
            self.assertEqual(expected_result.conn_string, actual_result.conn_string)
            self.assertEqual(expected_result.conn, actual_result.conn)
            self.assertEqual(expected_result.cursor, actual_result.cursor)

    def test_form_insert_statement(self):
        expected_result = 'INSERT INTO fake_table (attr1, attr2) VALUES ("val1", "val2")'

        actual_result = self.sql_controller.form_insert_statement('fake_table', 'attr1, attr2', '"val1", "val2"')

        with self.subTest():
            self.assertEqual(expected_result, actual_result)

    def test_form_update_statement(self):
        expected_result = "UPDATE fake_table SET attr1='val1', attr2='val2' WHERE id = 'fake_id'"

        actual_result = self.sql_controller.form_update_statement("fake_table", "attr1='val1', attr2='val2'", "fake_id")

        with self.subTest():
            self.assertEqual(expected_result, actual_result)

    def test_execute_statement(self):
        self.sql_controller.execute_statement('INSERT INTO fake_table (attr1, attr2) VALUES ("val1", "val2")')

        with self.subTest():
            self.assertEqual(self.fake_cursor.execute.call_count, 1)    
            self.assertEqual(self.fake_cursor.commit.call_count, 1)    

    def test_close_cursor(self):
        self.sql_controller.close_cursor()

        with self.subTest():
            self.assertEqual(self.fake_cursor.close.call_count, 1)  
    
    @patch('builtins.print')
    @patch.object(sql_handler.SqlController, 'execute_statement')
    @patch.object(sql_handler.SqlController, 'form_insert_statement')
    def test_db_write_start_stream(self, mock_statement, mock_execute, mock_print):
        mock_statement.return_value = 'INSERT INTO fake_table (attr1, attr2) VALUES ("val1", "val2")'
        mock_execute.return_value = Mock()

        self.sql_controller.db_write_start_stream('fake_id')

        with self.subTest():
            self.assertEqual(mock_statement.called, 1)
            self.assertEqual(mock_execute.called, 1)

        mock_execute.side_effect = self.generic_exception
        self.sql_controller.db_write_start_stream('fake_id')

        with self.subTest():
            mock_print.assert_called_with(f"Failed to write start stream to database and caught exception Exception('Some error')") 
    
    @patch('builtins.print')
    @patch.object(sql_handler.SqlController, 'execute_statement')
    @patch.object(sql_handler.SqlController, 'form_update_statement')
    def test_db_write_end_stream(self, mock_statement, mock_execute, mock_print):
        mock_statement.return_value = "UPDATE fake_table SET attr1='val1', attr2='val2' WHERE id = 'fake_id'"
        mock_execute.return_value = Mock()

        self.sql_controller.db_write_end_stream('fake_id')

        with self.subTest():
            self.assertEqual(mock_statement.called, 1)
            self.assertEqual(mock_execute.called, 1)

        mock_execute.side_effect = self.generic_exception
        self.sql_controller.db_write_end_stream('fake_id')

        with self.subTest():
            mock_print.assert_called_with(f"Failed to write end stream to database and caught exception Exception('Some error')") 
    