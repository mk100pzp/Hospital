import unittest
from app.models.models import Admin, Doctor, Patient, Visit_Form, Medical_Record, Patient_Bill
from app.database import db

class TestModels(unittest.TestCase):

    # Initialize a test database connection and create tables
    def setUp(self):
        self.db_manager = db.DbPostgresManager(dbname='test_hospital')
        self.db_manager.creat_table()


    # Clean up the test database and close the connection
    def tearDown(self):
        self.db_manager.drop_database('test_hospital')


    # ---------------------  test all roles  ---------------------
    def test_add_new_admin(self):
        admin = Admin("admin_user", "admin_pass", "admin@example.com", "1234567890")
        Admin.add_new_admin(admin)

    def test_add_new_doctor(self):
        doctor = Doctor("doctor_user", "doctor_pass", "doctor@example.com", "9876543210",
                        "Dr. Smith", "Cardiologist", 10, 100000, "123 Main St", 50)
        Doctor.add_new_doctor(doctor)

    def test_add_new_patient(self):
        patient = Patient("patient_user", "patient_pass", "patient@example.com", "5551234567", "John Doe", "456 Elm St")
        Patient.add_new_patient(patient)


if __name__ == '__main__':
    unittest.main()



# To run code :   python3.11.exe -m unittest tests.test_models