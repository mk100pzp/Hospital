import unittest
import os
import sys

project_root = os.path.abspath(os.path.dirname(__file__))
child_directory =os.path.join(os.path.join(project_root, 'app'),'database')
sys.path.insert(0, child_directory)
from db import DbPostgresManager  

class TestDbPostgresManager(unittest.TestCase):
    def setUp(self):
        self.db_manager = DbPostgresManager(dbps_defult="test_database.ini", dbname='test_db')

    # Perform any necessary cleanup after each test
    def tearDown(self):
        pass

    def test_connection_database(self):
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


