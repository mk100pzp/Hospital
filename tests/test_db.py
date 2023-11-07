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
    manager=DbPostgresManager(dbps_defult="database.ini", dbname='test_db', password=None, tables='None')
    def test_connection_database(self):
           result=self.manager.connection_database()
           self.assertEqual(result["dbname"], 'test_db') 
           psycopg2.connect= Mock()
           cur=psycopg2.connect.cursor
           self.manager.dbname='checkingtest_db'
           result=self.manager.connection_database()
           self.assertNotEqual(result["dbname"], 'test_db') 
    
    def tearDown(self):
        pass


    def test_db_connect(self):
        pass

    def test_drop_database(self):
        pass

    def test_create_table(self):
        pass

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


