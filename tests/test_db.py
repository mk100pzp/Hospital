
import unittest
import psycopg2
from unittest.mock import patch, Mock
from pathlib import Path
import sys, os

project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_folder)
from app.database.db import DbPostgresManager


class TestStringMethods(unittest.TestCase):
    mock_params = {
        'dbname': 'postgres',
        'user': 'postgres',
        'port': 5432,
        'host': 'localhost',
        'password': 'shima1993',
    }
    manager = DbPostgresManager(dbps_defult="database.ini", dbname='test_db', password=None, tables='None')

    def setUp(self):
        # Create a mock for psycopg2.connect
        self.manager.config = Mock()
        self.manager.config.return_value = self.mock_params
        print(self.manager.config.return_value)

    def test_connection_database(self):
        result = self.manager.connection_database()
        self.assertEqual(result["dbname"], 'test_db')
        self.manager.dbname = 'checkingtest_db'
        result = self.manager.connection_database()
        self.assertNotEqual(result["dbname"], 'test_db')
        result = self.manager.connection_database()
        self.assertEqual(result["dbname"], 'checkingtest_db')

    def test_db_connect(self):
        with unittest.mock.patch('psycopg2.connect') as mock_connect:
            mock_conn = Mock()
            mock_cur = Mock()
            mock_conn.cursor.return_value = mock_cur
            mock_connect.return_value = mock_conn
            result_conn, result_cur = self.manager._db_connect()
            self.assertEqual(result_conn, mock_conn)
            self.assertEqual(result_cur, mock_cur)

        # Test the case where psycopg2.connect returns None (error) and Check the exception message
        with unittest.mock.patch('psycopg2.connect') as mock_connect:
            mock_connect.return_value = None
            self.assertIsNone(self.manager._db_connect())
            self.assertRaises(TypeError, self.manager._db_connect())

    def test_drop_database(self):
        pass

    def test_create_table(self):
        # Test the excuting the query for creat table
        with unittest.mock.patch('psycopg2.connect') as mock_connect:
            mock_conn = Mock()
            mock_cur = Mock()
            mock_conn.cursor.return_value = mock_cur
            mock_connect.return_value = mock_conn
            self.manager.close = Mock()
            self.manager.reade_file = Mock()
            self.manager.config = Mock()
            self.manager.reade_file.sections.return_value = ["table1", "table2"]
            self.manager.config.return_value = [{'column1': 'int', 'column2': 'varchar(50)'},
                                                {'column3': 'text', 'column4': 'boolean'}]
            try:
                self.manager.create_table()
            except Exception as e:
                self.fail(f"Code execution resulted in an error: {e}")

    # @patch('psycopg2.connect')
    # def test_update_table(self):
    #     mock_cur = Mock()
    #     mock_cur.return_value = mock_cur

    @patch('psycopg2.connect')
    def test_update_table(self, mock_connect):
        # Mock the psycopg2.connect method

        # Create a mock cursor and execute method
        mock_cursor = Mock()
        mock_execute = Mock()
        mock_cursor.execute = mock_execute
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Mock the new_value dictionary and condition list
        new_value = {'user_name': 'shima', 'user_pass': '1234'}
        condition = [('user_id', '=', '2')]
        table_name = "users"

        # Call the method you want to test
        self.manager.update_table('users', new_value, condition)
        column, operator, value = condition[0]

        # Assertions
        mock_cursor.execute.assert_called_with(
            f"UPDATE {table_name} SET user_name = {new_value['user_name']} , user_pass = {new_value['user_pass']} "
            f"WHERE  AND {column} {operator} {value}"
        )

    def test_drop_table(self):
        pass

    def test_delete_from_table(self):
        pass

    def test_insert_table(self):
        pass

    def test_select(self):
        pass

    def test_show_table(self):
        pass

    def test_alter_table(self):
        pass

    def tearDown(self):
        self.manager.dbname = 'test_db'
        # self.manager.config.reset_mock()


if __name__ == '__main__':
    unittest.main()

