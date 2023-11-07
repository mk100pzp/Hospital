import unittest
import psycopg2
from unittest.mock import patch,Mock
from pathlib import Path
import sys,os

project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_folder)
from app.database.db import DbPostgresManager

class TestStringMethods(unittest.TestCase): 
    mock_params = {
            'dbname': 'postgres',
            'user': 'postgres',
            'port': 5432,
            'host': 'localhost',
            'password': 'Shad_M72770',
    }
    manager=DbPostgresManager(dbps_defult="database.ini", dbname='test_db', password=None, tables='None')
    def setUp(self):
        # Create a mock for psycopg2.connect
        self.manager.config=Mock()
        self.manager.config.return_value=self.mock_params 
    def test_connection_database(self):
           result=self.manager.connection_database()
           self.assertEqual(result["dbname"], 'test_db') 
           self.manager.dbname='checkingtest_db'
           result=self.manager.connection_database()
           self.assertNotEqual(result["dbname"], 'test_db') 

    def tearDown(self):
        self.manager.dbname='test_db'
    
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
            self.assertRaises(TypeError,self.manager._db_connect()) 

    def test_drop_database(self):
        pass

    def test_create_table(self):
    # Test the excuting the query for creat table 
        with unittest.mock.patch('psycopg2.connect') as mock_connect:
            mock_conn = Mock()
            mock_cur = Mock()
            mock_conn.cursor.return_value = mock_cur
            mock_connect.return_value = mock_conn 
            self.manager._close = Mock()
            self.manager.reade_file=Mock()
            self.manager.config=Mock()
            self.manager.reade_file.sections.return_value=["table1","table2"]
            self.manager.config.return_value=[{'column1': 'int', 'column2': 'varchar(50)'},
                {'column3': 'text', 'column4': 'boolean'}]
            try:
                self.manager.create_table()    
            except Exception as e:
                self.fail(f"Code execution resulted in an error: {e}")
            
        

    def test_drop_table(self):
        pass

    def test_update_table(self):
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




if __name__ == '__main__':
    unittest.main()


