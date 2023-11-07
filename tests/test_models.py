import unittest
from unittest.mock import patch, Mock
from app.models.models import Admin, Doctor, Patient
from app.database.db import DbPostgresManager

class TestModels(unittest.TestCase):

    # Initialize a test database connection and create tables
    @patch('app.database.db.DbPostgresManager')
    def setUp(self, MockDbManager):
        self.mock_db_manager = MockDbManager.return_value
        self.db_manager = self.mock_db_manager.return_value
        self.db_manager.create_table.return_value = True
        self.mock_db_manager.return_value.creat_table.return_value = True


    # Clean up the test database and close the connection
    def tearDown(self):
        self.db_manager.drop_database('test_hospital')


    # ---------------------  test all roles  ---------------------
    def test_add_new_admin(self):
        admin = Admin("admin_user", "admin_pass", "admin@example.com", "1234567890")
        with patch.object(Admin, 'add_new_admin', return_value=True):
            result = Admin.add_new_admin(admin, self.db_manager)
            self.assertTrue(result)

    def test_add_new_doctor(self):
        doctor = Doctor("doctor_user", "doctor_pass", "doctor@example.com", "9876543210",
                        "Dr. Smith", "Cardiologist", 10, 100000, "123 Main St", 50)
        with patch.object(Doctor, 'add_new_doctor', return_value=True):
            result = Doctor.add_new_doctor(doctor, self.db_manager)
            self.assertTrue(result)

    def test_add_new_patient(self):
        patient = Patient("patient_user", "patient_pass", "patient@example.com", "5551234567", "John Doe", "456 Elm St")
        with patch.object(Patient, 'add_new_patient', return_value=True):
            result = Patient.add_new_patient(patient, self.db_manager)
            self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()



# To run code :   python3.11.exe -m unittest tests.test_models