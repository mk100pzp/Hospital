import bcrypt
from app.database import db
from app.models import models


class Authentication:
    def __init__(self):
        pass

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    @classmethod
    def doctor_registration(cls):
        try:
            user_name = input("Enter your username : ")
            user_pass_1 = input("Enter your password : ")
            user_pass_2 = input("re-write your password : ")
            if user_pass_1 != user_pass_2:
                print("Not equal password together !")
                cls.doctor_registration()
            user_pass_1 = cls.hash_password(user_pass_1)
            user_email = input("Enter your email : ")
            user_mobile = int(input("Enter your phone number : "))
            doctor_name = input("Enter your name :")
            experties = input("Enter your experties : ")
            work_experienceit = int(input("Enter your work experienceit (How many years?) : "))
            salary = float(input("Enter your salary ($) : "))
            address = input("Enter your address : ")
            visit_price = float(input("Enter visit price ($) : "))
            doctor_obj = models.Doctor(user_name, user_pass_1, user_email, user_mobile, doctor_name, experties,
                                       work_experienceit, salary, address, visit_price)
            if db.Database.save_doctor(doctor_obj):
                print("Your registration successfull.")
            else:
                print("something went wrong ! please try again.")
                cls.doctor_registration()

        except:
            print("Please enter number for mobile - work experienceit - salary - visit price")
            cls.doctor_registration()

    @classmethod
    def patient_registeration(cls):
        try:
            user_name = input("Enter your username : ")
            user_pass_1 = input("Enter your password : ")
            user_pass_2 = input("re-write your password : ")
            if user_pass_1 != user_pass_2:
                print("Not equal password together !")
                cls.patient_registeration()
            user_pass_1 = cls.hash_password(user_pass_1)
            user_email = input("Enter your email : ")
            user_mobile = int(input("Enter your email : "))
            patient_name = input("Enter your name : ")
            patient_address = int(input("Enter your addrress : "))
            patient_obj = models.Doctor(user_name, user_pass_1, user_email, user_mobile, patient_name, patient_address)
            if db.Database.save_patient(patient_obj):
                print("Your registration successfull.")
            else:
                print("something went wrong ! please try again.")
                cls.patient_registeration()

        except:
            print("Please enter number for mobile - work experienceit - salary - visit price")
            cls.patient_registeration()

    @staticmethod
    def login_patient():
        print("login patient....")
        user_name = input("Enter your username : ")
        input_password = input("Enter your password : ")
        if db.Database.check_exist("patient", user_name, input_password):
            return True
        else:
            return False

    @staticmethod
    def login_doctor():
        print("login doctor....")
        user_name = input("Enter your username : ")
        input_password = input("Enter your password : ")
        if db.Database.check_exist("doctor", user_name, input_password):
            return True
        else:
            return False

    @staticmethod
    def login_admin():
        print("login admin....")
        user_name = input("Enter your username : ")
        input_password = input("Enter your password : ")
        if db.Database.check_exist("admin", user_name, input_password):
            return True
        else:
            return False
