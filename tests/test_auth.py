import unittest
from unittest.mock import patch
from app.authentication import auth


class AuthenticationTestCase(unittest.TestCase):
    def test_hash_password(self):
        password = "password123"
        hashed_password = auth.Authentication.hash_password(password)
        self.assertIsNotNone(hashed_password)
        self.assertNotEqual(password, hashed_password)

    @patch('builtins.input')
    def test_doctor_registration(self, mock_input):
        mock_input.side_effect = ['doc_username', 'password123', 'password123', 'test@example.com', '1234567890',
                                  'Doctor Name', 'Expertise', '5', '5000', 'Address', '50']
        with patch('app.database.db.Database.save_doctor', return_value=True):
            result = auth.Authentication.doctor_registration()
            self.assertTrue(result)

    @patch('builtins.input')
    def test_patient_registration(self, mock_input):
        mock_input.side_effect = ['patient_username', 'password123', 'password123', 'test@example.com', '1234567890',
                                  'Patient Name', 'Address']
        with patch('app.database.db.Database.save_patient', return_value=True):
            result = auth.Authentication.patient_registeration()
            self.assertTrue(result)

    @patch('builtins.input')
    def test_login_patient(self, mock_input):
        mock_input.side_effect = ['patient_username', 'password123']
        with patch('Package.module.Classname/Database.check_exist', return_value=True):
            result = auth.Authentication.login_patient()
            self.assertTrue(result)

    @patch('builtins.input')
    def test_login_doctor(self, mock_input):
        mock_input.side_effect = ['doc_username', 'password123']
        with patch('app.database.db.Database.check_exist', return_value=True):
            result = auth.Authentication.login_doctor()
            self.assertTrue(result)

    @patch('builtins.input')
    def test_login_admin(self, mock_input):
        mock_input.side_effect = ['admin_username', 'password123']
        with patch('app.database.db.Database.check_exist', return_value=True):
            result = auth.Authentication.login_admin()
            self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
