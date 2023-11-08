import bcrypt
import sys
import os
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_folder)
from database.db import DbPostgresManager
from app.models import models


class Authentication:
    db = DbPostgresManager()
    db.create_table()
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

            cls.db.insert_table("users",["user_name","user_pass","user_email","user_mobile"], [ user_name, user_pass_1, user_email, user_mobile])
            user_id = input("Please Enter your id : ")
            cls.db.insert_table("doctors", ["doctor_name", "expertis", "work_experience", "adress", "visit_price", "users_user_id"],
                         [ doctor_obj.doctor_name,doctor_obj.experties,doctor_obj.work_experienceit,doctor_obj.address,doctor_obj.visit_price, user_id])
        except Exception as e:
            print(e)
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
            cls.db.insert_table("users",["user_name","user_pass","user_email","user_mobile"], [ user_name, user_pass_1, user_email, user_mobile])
            user_id = input("Please Enter your id : ")
            cls.db.insert_table("patients", ["name_name", "patient_adress", "users_user_id"],
                         [ patient_obj.patient_name, patient_obj.patient_address , user_id])

        except:
            print("Please enter number for mobile - work experienceit - salary - visit price")
            cls.patient_registeration()

    @classmethod
    def login(cls):
        user_name = input("Enter your username : ")
        input_password = input("Enter your password : ")
        if cls.db.select("users",select_options="user_id",filter_options=[("users.user_name","=", user_name)("users.user_pass", "=",input_password)]):
            return True
        else:
            return False
      

    # @classmethod
    # def login_doctor(cls):
    #     print("login doctor....")
    #     user_name = input("Enter your username : ")
    #     input_password = input("Enter your password : ")
    #     if cls.db.select("users",select_options="user_id",filter_options=[("users.user_name","=", user_name)("users.user_pass", "=",input_password)]):
    #         return True
    #     else:
    #         return False

    # @staticmethod
    # def login_admin():
    #     print("login admin....")
    #     user_name = input("Enter your username : ")
    #     input_password = input("Enter your password : ")
    #     if cls.db.select("users",select_options="user_id",filter_options=[("users.user_name","=", user_name)("users.user_pass", "=",input_password)]):
    #         return True
    #     else:
    #         return False
