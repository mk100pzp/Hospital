import unittest
from app.authentication import auth
from app.models import models
from app.menu import enter


class TestMenu(unittest.TestCase):
    def test_doctor_registration_action(self):
        self.assertIn(auth.Authentication.doctor_registration, enter[0]['children'][0]['children'][0]['action'])

    def test_patient_registration_action(self):
        self.assertIn(auth.Authentication.patient_registration, enter[0]['children'][0]['children'][1]['action'])

    def test_add_visit_time_function(self):
        self.assertIn(auth.Authentication.login_doctor, enter[0]['children'][1]['children'][0]['function'])
        self.assertIn(models.Visit_Date.create_visit_date, enter[0]['children'][1]['children'][0]['action'])

    def test_remove_visit_time_function(self):
        self.assertIn(auth.Authentication.login_doctor, enter[0]['children'][1]['children'][1]['function'])
        self.assertIn(models.Visit_Date.remove_visit_time, enter[0]['children'][1]['children'][1]['action'])

    def test_get_visit_time_function(self):
        self.assertIn(auth.Authentication.login_patient, enter[0]['children'][1]['children'][2]['function'])
        self.assertIn(models.Paient.get_visit_time, enter[0]['children'][1]['children'][2]['action'])

    # Add more test cases for other functions and actions


if __name__ == '__main__':
    unittest.main()